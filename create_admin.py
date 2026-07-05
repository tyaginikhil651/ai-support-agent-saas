from database import get_connection
from auth_routes import hash_password

conn = get_connection()

conn.execute(
    """
    INSERT OR IGNORE INTO admins
    (
        username,
        password,
        role
    )
    VALUES (?, ?, ?)
    """,
    (
        "admin",
        hash_password("admin123"),
        "Admin"
    )
)

conn.commit()
conn.close()

print("Admin Created")