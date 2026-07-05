from database import get_connection


def total_tickets():

    conn = get_connection()

    count = conn.execute(
        """
        SELECT COUNT(*)
        FROM tickets
        """
    ).fetchone()[0]

    conn.close()

    return count


def open_tickets():

    conn = get_connection()

    count = conn.execute(
        """
        SELECT COUNT(*)
        FROM tickets
        WHERE status='Open'
        """
    ).fetchone()[0]

    conn.close()

    return count


def closed_tickets():

    conn = get_connection()

    count = conn.execute(
        """
        SELECT COUNT(*)
        FROM tickets
        WHERE status='Closed'
        """
    ).fetchone()[0]

    conn.close()

    return count


def total_customers():

    conn = get_connection()

    count = conn.execute(
        """
        SELECT COUNT(*)
        FROM users
        """
    ).fetchone()[0]

    conn.close()

    return count


def ticket_status_breakdown():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            status,
            COUNT(*) as total
        FROM tickets
        GROUP BY status
        """
    ).fetchall()

    conn.close()

    return rows



def priority_breakdown():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            priority,
            COUNT(*) as total
        FROM tickets
        GROUP BY priority
        """
    ).fetchall()

    conn.close()

    return rows


def agent_performance():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            assigned_to,
            COUNT(*) as total
        FROM tickets
        GROUP BY assigned_to
        """
    ).fetchall()

    conn.close()

    return rows


def monthly_tickets():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            strftime('%Y-%m', created_at) month,
            COUNT(*) total
        FROM tickets
        GROUP BY month
        ORDER BY month
        """
    ).fetchall()

    conn.close()

    return rows


