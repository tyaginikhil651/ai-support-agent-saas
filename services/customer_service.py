from database import get_connection


def save_or_update_customer(
    tenant_id,
    user_id,
    username=None,
    phone=None
):
    conn = get_connection()

    existing = conn.execute(
        """
        SELECT id
        FROM users
        WHERE tenant_id=?
          AND telegram_id=?
        """,
        (tenant_id, str(user_id))
    ).fetchone()

    if existing:
        conn.execute(
            """
            UPDATE users
            SET username=?,
                phone=?
            WHERE id=?
            """,
            (
                username,
                phone,
                existing["id"]
            )
        )
    else:
        conn.execute(
            """
            INSERT INTO users(
                telegram_id,
                username,
                phone,
                tenant_id
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                str(user_id),
                username,
                phone,
                tenant_id
            )
        )

    conn.commit()
    conn.close()





