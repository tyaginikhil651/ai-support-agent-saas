from ticket_service import (
    create_ticket,
    get_ticket,
    update_ticket
)

ticket_id = create_ticket(
    "123",
    "Internet not working"
)

print("Created:", ticket_id)

ticket = get_ticket(ticket_id)

print(ticket)

update_ticket(
    ticket_id,
    "IN_PROGRESS"
)

ticket = get_ticket(ticket_id)

print(ticket)