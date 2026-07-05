from database import get_connection


def select_agent(skill):

    conn = get_connection()

    agent = conn.execute("""
    SELECT *
    FROM agents

    WHERE skill=?
    AND status='online'

    ORDER BY active_tickets ASC

    LIMIT 1
    """, (skill,)).fetchone()

    conn.close()

    return agent