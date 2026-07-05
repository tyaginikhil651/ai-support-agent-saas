import uuid

from database import get_connection
from services.escalation import (
    should_escalate,
    escalate_ticket,
    assign_agent
)
from services.live_notifications import send_live_notification



def create_complaint(
    user_id,
    issue,
    tenant_id=None
):

    ticket_id = "TKT-" + uuid.uuid4().hex[:8].upper()

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO tickets
        (
            ticket_id,
            user_id,
            issue,
            tenant_id
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            ticket_id,
            str(user_id),
            issue,
            tenant_id
        )
    )

    conn.commit()
    conn.close()

    if tenant_id is not None:
        send_live_notification(
            tenant_id=tenant_id,
            event_type="new_ticket",
            title="New support ticket",
            message=f"New complaint received: {ticket_id}",
            data={
                "ticket_id": ticket_id,
                "user_id": str(user_id),
                "issue": issue,
                "status": "Open"
            }
        )

    return (
        f"Your complaint has been registered.\n\n"
        f"Ticket ID: {ticket_id}\n"
        f"Status: Open"
    )





