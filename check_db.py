from database import get_connection

conn = get_connection()

print("\n===== TICKETS TABLE =====")

rows = conn.execute(
    "PRAGMA table_info(tickets)"
).fetchall()

for row in rows:
    print(dict(row))

print("\n===== APPOINTMENTS TABLE =====")

rows = conn.execute(
    "PRAGMA table_info(appointments)"
).fetchall()

for row in rows:
    print(dict(row))

conn.close()