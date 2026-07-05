from database import get_connection

TENANT_ID = 1
USER_ID = "919670443252"

conn = get_connection()

conn.execute(
    """
    DELETE FROM customer_profile
    WHERE tenant_id = ?
    AND user_id = ?
    """,
    (TENANT_ID, USER_ID)
)

conn.execute(
    """
    DELETE FROM sessions
    WHERE tenant_id = ?
    AND user_id = ?
    """,
    (TENANT_ID, USER_ID)
)

conn.execute(
    """
    DELETE FROM appointments
    WHERE tenant_id = ?
    AND user_id = ?
    """,
    (TENANT_ID, USER_ID)
)

conn.commit()
conn.close()

print("Test customer profile reset successfully")