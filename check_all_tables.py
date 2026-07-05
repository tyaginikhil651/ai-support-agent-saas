# check_all_tables.py

import sqlite3

conn = sqlite3.connect("support.db")

tables = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""").fetchall()

print("\n===== TABLES =====\n")

for table in tables:
    print(table[0])

conn.close()