import sqlite3

conn = sqlite3.connect('results.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM worker_stats")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
