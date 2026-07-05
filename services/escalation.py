from database import get_connection


ESCALATION_KEYWORDS = [

    "angry",

    "refund",

    "cancel",

    "lawyer",

    "not working",

    "service down",

    "internet down",

    "manager",

    "human",

    "agent"
]


def should_escalate(message):

    message = message.lower()

    for word in ESCALATION_KEYWORDS:

        if word in message:

            return True

    return False

def escalate_ticket(ticket_id):

    conn = get_connection()

    conn.execute(
        """
        UPDATE tickets
        SET escalated=1,
            status='Escalated'
        WHERE ticket_id=?
        """,
        (ticket_id,)
    )

    conn.commit()

    conn.close()


def assign_agent(ticket_id):

    conn = get_connection()

    conn.execute(
        """
        UPDATE tickets
        SET assigned_to='Support Team'
        WHERE ticket_id=?
        """,
        (ticket_id,)
    )

    conn.commit()

    conn.close()



