from database import get_connection


# ----------------------------------
# CUSTOMER MANAGEMENT
# ----------------------------------

def save_customer(
    tenant_id: int,
    platform_user_id: str,
    username: str | None = None,
    phone: str | None = None
):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO users (
            tenant_id,
            platform_user_id,
            username,
            phone
        )
        VALUES (?, ?, ?, ?)

        ON CONFLICT(tenant_id, platform_user_id)
        DO UPDATE SET
            username = COALESCE(excluded.username, users.username),
            phone = COALESCE(excluded.phone, users.phone)
        """,
        (
            tenant_id,
            str(platform_user_id),
            username,
            phone
        )
    )

    conn.commit()
    conn.close()


def get_customer(
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


# ----------------------------------
# TICKET STATUS
# ----------------------------------

def ticket_status(
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

    if ticket is None:
        return "❌ Ticket not found. Please check the ticket ID and try again."

    assigned_to = ticket["assigned_to"] or "Not assigned yet"
    priority = ticket["priority"] or "Medium"
    estimated_resolution = (
        ticket["estimated_resolution"]
        or "Not available yet"
    )

    return (
        f"🎫 Ticket ID: {ticket['ticket_id']}\n"
        f"📌 Status: {ticket['status']}\n"
        f"⚡ Priority: {priority}\n"
        f"👤 Assigned to: {assigned_to}\n"
        f"📝 Issue: {ticket['issue']}\n"
        f"⏳ Estimated resolution: {estimated_resolution}\n"
        f"📅 Created: {ticket['created_at']}"
    )



