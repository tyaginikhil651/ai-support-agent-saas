from database import get_connection

conn = get_connection()

TENANT_ID = 1

for i in range(1, 6):

    ticket_id = f"TKT{i:03}"

    # Skip if ticket already exists for this tenant
    existing = conn.execute(
        """
        SELECT id
        FROM tickets
        WHERE tenant_id = ?
          AND ticket_id = ?
        """,
        (
            TENANT_ID,
            ticket_id,
        )
    ).fetchone()

    if existing:
        print(f"{ticket_id} already exists.")
        continue

    conn.execute(
        """
        INSERT INTO tickets(
            tenant_id,
            ticket_id,
            user_id,
            issue,
            status,
            priority
        )
        VALUES(
            ?, ?, ?, ?, ?, ?
        )
        """,
        (
            TENANT_ID,
            ticket_id,
            "12345",
            f"Demo Issue {i}",
            "Open",
            "Medium",
        )
    )

    print(f"Inserted {ticket_id}")

conn.commit()
conn.close()

print("Demo tickets inserted successfully.")