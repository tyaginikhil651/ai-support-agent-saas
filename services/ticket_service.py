import uuid

from database import get_connection


def create_ticket(
    user_id,
    issue
):

    conn = get_connection()

    ticket_id = str(uuid.uuid4())[:8]

    conn.execute(
        """
        INSERT INTO tickets(
            ticket_id,
            user_id,
            issue
        )
        VALUES(?,?,?)
        """,
        (
            ticket_id,
            user_id,
            issue
        )
    )

    conn.commit()
    conn.close()

    return ticket_id

def get_ticket(ticket_id):

    conn = get_connection()

    ticket = conn.execute(
        """
        SELECT *
        FROM tickets
        WHERE ticket_id=?
        """,
        (ticket_id,)
    ).fetchone()

    conn.close()

    return ticket

def update_ticket_status(
    ticket_id,
    status
):

    conn = get_connection()

    conn.execute(
        """
        UPDATE tickets
        SET status=?
        WHERE ticket_id=?
        """,
        (
            status,
            ticket_id
        )
    )

    conn.commit()
    conn.close()

def assign_ticket(
    ticket_id,
    agent
):

    conn = get_connection()

    conn.execute(
        """
        UPDATE tickets
        SET assigned_to=?
        WHERE ticket_id=?
        """,
        (
            agent,
            ticket_id
        )
    )

    conn.commit()
    conn.close()


