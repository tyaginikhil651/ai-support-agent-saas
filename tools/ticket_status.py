from services.ticket_service import get_ticket


def ticket_status(ticket_id):

    ticket = get_ticket(ticket_id)

    if not ticket:
        return "Ticket not found."

    return f"""
            Ticket ID: {ticket['ticket_id']}

            Status: {ticket['status']}

            Priority: {ticket['priority']}

            Assigned To: {ticket['assigned_to']}

            Issue: {ticket['issue']}
            """