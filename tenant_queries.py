from database import get_connection


def get_dashboard_metrics(tenant_id):
    conn = get_connection()

    customers = conn.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE tenant_id=?
        """,
        (tenant_id,)
    ).fetchone()[0]

    open_tickets = conn.execute(
        """
        SELECT COUNT(*)
        FROM tickets
        WHERE tenant_id=?
        AND status NOT IN ('Resolved', 'Closed')
        """,
        (tenant_id,)
    ).fetchone()[0]

    appointments = conn.execute(
        """
        SELECT COUNT(*)
        FROM appointments
        WHERE tenant_id=?
        """,
        (tenant_id,)
    ).fetchone()[0]

    live_tickets = conn.execute(
        """
        SELECT COUNT(*)
        FROM tickets
        WHERE tenant_id=?
        AND status='Live'
        """,
        (tenant_id,)
    ).fetchone()[0]

    high_priority = conn.execute(
        """
        SELECT COUNT(*)
        FROM tickets
        WHERE tenant_id=?
        AND priority='High'
        AND status NOT IN ('Resolved', 'Closed')
        """,
        (tenant_id,)
    ).fetchone()[0]

    conn.close()

    return {
        "customers": customers,
        "open_tickets": open_tickets,
        "appointments": appointments,
        "live_tickets": live_tickets,
        "high_priority": high_priority
    }


def get_tenant_customers(tenant_id):
    conn = get_connection()

    users = conn.execute(
        """
        SELECT *
        FROM users
        WHERE tenant_id=?
        ORDER BY id DESC
        """,
        (tenant_id,)
    ).fetchall()

    conn.close()

    return users


def get_tenant_tickets(tenant_id):
    conn = get_connection()

    tickets = conn.execute(
        """
        SELECT *
        FROM tickets
        WHERE tenant_id=?
        ORDER BY id DESC
        """,
        (tenant_id,)
    ).fetchall()

    conn.close()

    return tickets


def get_tenant_appointments(tenant_id):
    conn = get_connection()

    appointments = conn.execute(
        """
        SELECT *
        FROM appointments
        WHERE tenant_id=?
        ORDER BY id DESC
        """,
        (tenant_id,)
    ).fetchall()

    conn.close()

    return appointments


# def get_tenant_ticket_by_id(
#     tenant_id,
#     ticket_id
# ):
#     conn = get_connection()

#     ticket = conn.execute(
#         """
#         SELECT *
#         FROM tickets
#         WHERE tenant_id=?
#         AND ticket_id=?
#         """,
#         (
#             tenant_id,
#             ticket_id
#         )
#     ).fetchone()

#     conn.close()

#     return ticket


def get_tenant_ticket_by_id(
    tenant_id: int,
    ticket_id: str
):
    from database import get_connection

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

def update_tenant_ticket_status(
    tenant_id,
    ticket_id,
    status
):
    conn = get_connection()

    cursor = conn.execute(
        """
        UPDATE tickets
        SET status=?
        WHERE tenant_id=?
        AND ticket_id=?
        """,
        (
            status,
            tenant_id,
            ticket_id
        )
    )

    conn.commit()

    updated_rows = cursor.rowcount

    conn.close()

    return updated_rows > 0




