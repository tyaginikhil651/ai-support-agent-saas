from database import get_connection


def get_tenant_sessions(tenant_id: int):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM sessions
        WHERE tenant_id = ?
        ORDER BY updated_at DESC
        """,
        (tenant_id,)
    ).fetchall()

    conn.close()
    return rows


def get_tenant_escalated_tickets(tenant_id: int):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM tickets
        WHERE tenant_id = ?
        AND escalated = 1
        ORDER BY created_at DESC
        """,
        (tenant_id,)
    ).fetchall()

    conn.close()
    return rows


def get_tenant_vip_customers(
    tenant_id: int,
    minimum_vip_score: float = 10
):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            customer_profile.*,
            users.username,
            users.phone
        FROM customer_profile
        LEFT JOIN users
            ON users.tenant_id = customer_profile.tenant_id
            AND users.platform_user_id = customer_profile.user_id
        WHERE customer_profile.tenant_id = ?
        AND customer_profile.vip_score >= ?
        ORDER BY customer_profile.vip_score DESC,
                 customer_profile.last_active DESC
        """,
        (
            tenant_id,
            minimum_vip_score
        )
    ).fetchall()

    conn.close()
    return rows


def get_tenant_customer_profile(
    tenant_id: int,
    user_id: str
):
    conn = get_connection()

    profile = conn.execute(
        """
        SELECT
            customer_profile.*,
            users.username,
            users.phone
        FROM customer_profile
        LEFT JOIN users
            ON users.tenant_id = customer_profile.tenant_id
            AND users.platform_user_id = customer_profile.user_id
        WHERE customer_profile.tenant_id = ?
        AND customer_profile.user_id = ?
        """,
        (
            tenant_id,
            str(user_id)
        )
    ).fetchone()

    conn.close()
    return profile


def get_tenant_analytics(tenant_id: int):
    conn = get_connection()

    total_tickets = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE tenant_id = ?
        """,
        (tenant_id,)
    ).fetchone()["count"]

    open_tickets = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE tenant_id = ?
        AND status = 'Open'
        """,
        (tenant_id,)
    ).fetchone()["count"]

    in_progress_tickets = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE tenant_id = ?
        AND status = 'In Progress'
        """,
        (tenant_id,)
    ).fetchone()["count"]

    resolved_tickets = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE tenant_id = ?
        AND status = 'Resolved'
        """,
        (tenant_id,)
    ).fetchone()["count"]

    escalated_tickets = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM tickets
        WHERE tenant_id = ?
        AND escalated = 1
        """,
        (tenant_id,)
    ).fetchone()["count"]

    total_customers = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM users
        WHERE tenant_id = ?
        """,
        (tenant_id,)
    ).fetchone()["count"]

    total_appointments = conn.execute(
        """
        SELECT COUNT(*) AS count
        FROM appointments
        WHERE tenant_id = ?
        """,
        (tenant_id,)
    ).fetchone()["count"]

    priority_breakdown = conn.execute(
        """
        SELECT
            priority,
            COUNT(*) AS count
        FROM tickets
        WHERE tenant_id = ?
        GROUP BY priority
        ORDER BY count DESC
        """,
        (tenant_id,)
    ).fetchall()

    monthly_tickets = conn.execute(
        """
        SELECT
            strftime('%Y-%m', created_at) AS month,
            COUNT(*) AS count
        FROM tickets
        WHERE tenant_id = ?
        GROUP BY strftime('%Y-%m', created_at)
        ORDER BY month DESC
        LIMIT 12
        """,
        (tenant_id,)
    ).fetchall()

    conn.close()

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress_tickets,
        "resolved_tickets": resolved_tickets,
        "escalated_tickets": escalated_tickets,
        "total_customers": total_customers,
        "total_appointments": total_appointments,
        "priority_breakdown": priority_breakdown,
        "monthly_tickets": monthly_tickets
    }