from database import get_connection


def get_tenant_ticket_for_reply(
    tenant_id: int,
    ticket_id: str
):
    conn = get_connection()

    ticket = conn.execute(
        """
        SELECT *
        FROM tickets
        WHERE tenant_id = ?
        AND ticket_id = ?
        """,
        (
            tenant_id,
            ticket_id.strip().upper()
        )
    ).fetchone()

    conn.close()

    return ticket


def get_tenant_customer_by_platform_id(
    tenant_id: int,
    platform_user_id: str
):
    conn = get_connection()

    customer = conn.execute(
        """
        SELECT *
        FROM users
        WHERE tenant_id = ?
        AND platform_user_id = ?
        """,
        (
            tenant_id,
            str(platform_user_id)
        )
    ).fetchone()

    conn.close()

    return customer


def save_tenant_reply(
    tenant_id: int,
    ticket_id: str,
    message: str,
    sender: str
):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO replies (
            tenant_id,
            ticket_id,
            message,
            sender
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            tenant_id,
            ticket_id.strip().upper(),
            message.strip(),
            sender
        )
    )

    conn.commit()
    conn.close()


def get_tenant_replies(
    tenant_id: int,
    ticket_id: str
):
    conn = get_connection()

    replies = conn.execute(
        """
        SELECT *
        FROM replies
        WHERE tenant_id = ?
        AND ticket_id = ?
        ORDER BY id ASC
        """,
        (
            tenant_id,
            ticket_id.strip().upper()
        )
    ).fetchall()

    conn.close()

    return replies


def mark_tenant_ticket_in_progress(
    tenant_id: int,
    ticket_id: str
):
    conn = get_connection()

    cursor = conn.execute(
        """
        UPDATE tickets
        SET status = 'In Progress'
        WHERE tenant_id = ?
        AND ticket_id = ?
        """,
        (
            tenant_id,
            ticket_id.strip().upper()
        )
    )

    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()

    return updated
