from database import get_connection

conn = get_connection()

agents = [
    (1, "Rahul", "rahul@company.com", "network"),
    (1, "Priya", "priya@company.com", "billing"),
    (1, "Amit", "amit@company.com", "technical"),
    (1, "Neha", "neha@company.com", "appointments"),
]

for tenant_id, name, email, skill in agents:

    existing = conn.execute(
        """
        SELECT id
        FROM agents
        WHERE tenant_id = ?
          AND email = ?
        """,
        (tenant_id, email),
    ).fetchone()

    if existing:
        print(f"{name} already exists.")
        continue

    conn.execute(
        """
        INSERT INTO agents(
            tenant_id,
            name,
            email,
            skill
        )
        VALUES (?, ?, ?, ?)
        """,
        (tenant_id, name, email, skill),
    )

    print(f"Added {name}")

conn.commit()
conn.close()

print("Done.")