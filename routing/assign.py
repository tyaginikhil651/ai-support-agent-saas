from database import get_connection


def assign_ticket(
    ticket_id,
    agent_id
):

    conn = get_connection()

    conn.execute("""
    UPDATE tickets

    SET assigned_to=?

    WHERE ticket_id=?
    """,
    (
        agent_id,
        ticket_id
    ))

    conn.execute("""
    UPDATE agents

    SET active_tickets=
    active_tickets+1

    WHERE id=?
    """,
    (agent_id,)
    )

    conn.commit()
    conn.close()