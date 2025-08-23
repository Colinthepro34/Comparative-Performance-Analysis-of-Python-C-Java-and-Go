import socket
import pickle
import pandas as pd
import json
import os

# === Configuration ===
SERVER_HOST = '127.0.0.1'  # Change if server is on a different machine
SERVER_PORT = 5000

def main():
    # Connect to server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, SERVER_PORT))

    # Receive DataFrame chunk size (8 bytes)
    size_bytes = s.recv(8)
    if not size_bytes:
        print("Failed to receive data size.")
        s.close()
        return
    size = int.from_bytes(size_bytes, 'big')

    # Receive DataFrame chunk bytes
    data_bytes = b''
    while len(data_bytes) < size:
        packet = s.recv(size - len(data_bytes))
        if not packet:
            break
        data_bytes += packet

    # Deserialize DataFrame chunk
    df_chunk = pickle.loads(data_bytes)

    # Compute partial stats based on your CSV columns
    rows_processed = len(df_chunk)

    # Calculate total sales amount (sum of 'Total Revenue' column)
    total_sales = df_chunk['Total Revenue'].sum()

    # Price statistics based on 'Unit Price'
    min_price = df_chunk['Unit Price'].min()
    max_price = df_chunk['Unit Price'].max()
    avg_price = df_chunk['Unit Price'].mean()

    # Prepare results
    worker_id = os.getenv('HOSTNAME', 'worker_unknown')
    partial_results = {
        'worker_id': worker_id,
        'rows_processed': rows_processed,
        'total_sales': total_sales,
        'min_price': min_price,
        'max_price': max_price,
        'avg_price': avg_price
    }

    # Serialize partial results to JSON
    result_json = json.dumps(partial_results).encode('utf-8')

    # Send result size and result JSON back to server
    s.sendall(len(result_json).to_bytes(8, 'big'))
    s.sendall(result_json)

    print(f"[{worker_id}] Sent partial result to server.")
    s.close()

if __name__ == "__main__":
    main()
