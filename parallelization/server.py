import socket
import threading
import pickle
import pandas as pd
import sqlite3
from datetime import datetime
import json
import numpy as np

# === Configuration ===
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5000
DB_PATH = 'results.db'

# Update this to the correct CSV path
CSV_PATH = '/home/codespace/.cache/kagglehub/datasets/weitat/sample-sales/versions/1/sales_5000000.csv'

# Number of workers expected
NUM_WORKERS = 4

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop the table if it already exists (removes old data)
    cursor.execute('DROP TABLE IF EXISTS worker_stats')

    # Recreate the table
    cursor.execute('''
        CREATE TABLE worker_stats (
            worker_id TEXT PRIMARY KEY,
            rows_processed INTEGER,
            total_sales REAL,
            min_price REAL,
            max_price REAL,
            avg_price REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def upsert_worker_stats(conn, stats):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO worker_stats (worker_id, rows_processed, total_sales, min_price, max_price, avg_price, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(worker_id) DO UPDATE SET
            rows_processed=excluded.rows_processed,
            total_sales=excluded.total_sales,
            min_price=excluded.min_price,
            max_price=excluded.max_price,
            avg_price=excluded.avg_price,
            timestamp=excluded.timestamp
    ''', (
        stats['worker_id'],
        stats['rows_processed'],
        stats['total_sales'],
        stats['min_price'],
        stats['max_price'],
        stats['avg_price'],
        datetime.now().isoformat()
    ))
    conn.commit()

def aggregate_results():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            SUM(rows_processed),
            SUM(total_sales),
            MIN(min_price),
            MAX(max_price),
            AVG(avg_price)
        FROM worker_stats
    ''')
    result = cursor.fetchone()
    conn.close()
    return result

# === Networking ===
def handle_worker(conn, addr, df_chunk, worker_id):
    print(f"[{worker_id}] Connected from {addr}")
    db_conn = sqlite3.connect(DB_PATH)  # Open new connection per thread

    try:
        # Serialize and send the DataFrame chunk
        data_bytes = pickle.dumps(df_chunk)
        conn.sendall(len(data_bytes).to_bytes(8, 'big'))
        conn.sendall(data_bytes)

        # Receive result size
        size_data = conn.recv(8)
        if not size_data:
            print(f"[{worker_id}] No data size received from worker.")
            return
        size = int.from_bytes(size_data, 'big')

        # Receive full result
        result_bytes = b''
        while len(result_bytes) < size:
            packet = conn.recv(size - len(result_bytes))
            if not packet:
                break
            result_bytes += packet

        result_json = result_bytes.decode('utf-8')
        partial_results = json.loads(result_json)
        print(f"[{worker_id}] Received partial results: {partial_results}")

        # Save to DB
        upsert_worker_stats(db_conn, partial_results)

    except Exception as e:
        print(f"[{worker_id}] Error: {e}")
    finally:
        db_conn.close()
        conn.close()
        print(f"[{worker_id}] Connection closed")

def main():
    print("Loading dataset...")
    df = pd.read_csv(CSV_PATH)

    # Updated column names to match your CSV
    required_columns = {'Unit Price', 'Units Sold', 'Total Revenue'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Dataset missing required columns: {required_columns - set(df.columns)}")

    print(f"Dataset loaded with {len(df)} rows.")

    # Split dataset into chunks
    chunks = np.array_split(df, NUM_WORKERS)

    # Initialize DB
    init_db()

    # Start server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(NUM_WORKERS)
    print(f"Server listening on {HOST}:{PORT}")

    threads = []

    for i in range(NUM_WORKERS):
        print(f"Waiting for worker {i+1} to connect...")
        conn, addr = server.accept()
        thread = threading.Thread(
            target=handle_worker,
            args=(conn, addr, chunks[i], f'worker_{i+1}')
        )
        thread.start()
        threads.append(thread)

    # Wait for all workers to finish
    for t in threads:
        t.join()

    print("\nAll workers finished. Aggregating results...")
    total_rows, total_sales, min_price, max_price, avg_price = aggregate_results()

    print("\n===== Final Aggregated Results =====")
    print(f"Total rows processed: {total_rows}")
    print(f"Total sales amount: ${total_sales:,.2f}")
    print(f"Minimum price: ${min_price:.2f}")
    print(f"Maximum price: ${max_price:.2f}")
    print(f"Average price: ${avg_price:.2f}")
    print("====================================\n")

    server.close()

if __name__ == "__main__":
    main()
