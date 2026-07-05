import re

from tools.appointment import create_appointment
from tools.complaint import create_complaint
from tools.customer import ticket_status
from llm import ask_llm


def extract_ticket_id(message: str):

    match = re.search(
        r"\bTKT-[A-Z0-9]+\b",
        message.upper()
    )

    if match:
        return match.group(0)

    return None


def appointment_node(state):

    user_id = state["user_id"]
    tenant_id = state["tenant_id"]
    message = state["message"]

    service = "General Support"
    date = "To be confirmed"

    message_lower = message.lower()

    if "internet" in message_lower:
        service = "Internet Repair"

    elif "wifi" in message_lower:
        service = "WiFi Support"

    elif "installation" in message_lower:
        service = "New Installation"

    elif "engineer" in message_lower:
        service = "Engineer Visit"

    if "tomorrow" in message_lower:
        date = "Tomorrow"

    elif "today" in message_lower:
        date = "Today"

    response = create_appointment(
        user_id=user_id,
        service=service,
        date=date,
        tenant_id=tenant_id
    )

    return {
        "service": service,
        "date": date,
        "response": response
    }


def complaint_node(state):

    user_id = state["user_id"]
    tenant_id = state["tenant_id"]
    message = state["message"]

    response = create_complaint(
        user_id=user_id,
        issue=message,
        tenant_id=tenant_id
    )

    return {
        "response": response
    }


def ticket_status_node(state):

    tenant_id = state["tenant_id"]
    message = state["message"]

    ticket_id = extract_ticket_id(message)

    if not ticket_id:
        return {
            "response": (
                "Please send your ticket ID in this format:\n"
                "TKT-ABC12345"
            )
        }

    response = ticket_status(
        tenant_id=tenant_id,
        ticket_id=ticket_id
    )

    return {
        "ticket_id": ticket_id,
        "response": response
    }


def chat_node(state):

    message = state["message"]

    response = ask_llm(
                    f"""
            You are a helpful customer support assistant.

            Customer message:
            {message}

            Reply professionally and briefly.
            """
    )

    return {
        "response": response
    }




