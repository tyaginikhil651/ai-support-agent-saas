from ticket_service import ( create_ticket, get_ticket )
from services.ticket_service import create_ticket
from database import get_connection
from database import get_connection
from routing.skill_mapper import get_required_skill
from routing.agent_selector import select_agent
from routing.assign import assign_ticket


def get_ticket_status(ticket_id):

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

    if not ticket:
        return "❌ Ticket not found"

    return f"""
🎫 Ticket: {ticket['ticket_id']}

Status: {ticket['status']}

Priority: {ticket['priority']}

Assigned To:
{ticket['assigned_to']}
"""


def create_complaint(
    user_id,
    issue
):

    ticket_id = create_ticket(
        user_id,
        issue
    )

    skill = get_required_skill( issue )

    agent = select_agent(skill)

    if agent:

        assign_ticket(
            ticket_id,
            agent["id"]
        )

    return f"""
Complaint Registered

Ticket ID:
{ticket_id}

Issue:
{issue}

Status:
OPEN
"""

def register_complaint(user_id, text):

    ticket_id = create_ticket(
        user_id,
        text
    )

    return f"""
            ✅ Complaint Registered

            Ticket ID:
            {ticket_id}

            Status:
            OPEN
            """





def track_ticket(ticket_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM tickets
        WHERE ticket_id=?
        """,
        (ticket_id,)
    )

    row = cur.fetchone()

    conn.close()

    if not row:
        return "Ticket not found."

    return (
        f"Ticket: {row['ticket_id']}\n"
        f"Status: {row['status']}"
    )

