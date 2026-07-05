from services.session_service import (
    get_session,
    save_session,
    clear_session
)

from tools.appointment import create_appointment


def start_appointment_flow(
    tenant_id: int,
    user_id: str
):
    save_session(
        tenant_id=tenant_id,
        user_id=user_id,
        flow="appointment",
        step="waiting_service",
        data={}
    )

    return (
        "Sure. What service do you need?\n\n"
        "Examples:\n"
        "• Internet repair\n"
        "• WiFi issue\n"
        "• New installation\n"
        "• Engineer visit"
    )


def continue_appointment_flow(
    tenant_id: int,
    user_id: str,
    message: str
):
    session = get_session(
        tenant_id=tenant_id,
        user_id=user_id
    )

    if session is None:
        return None

    if session["flow"] != "appointment":
        return None

    step = session["step"]
    data = session["data"]

    if step == "waiting_service":

        data["service"] = message.strip()

        save_session(
            tenant_id=tenant_id,
            user_id=user_id,
            flow="appointment",
            step="waiting_date",
            data=data
        )

        return (
            f"Service selected: {data['service']}\n\n"
            "What date do you prefer?"
        )

    if step == "waiting_date":

        data["date"] = message.strip()

        response = create_appointment(
            user_id=user_id,
            service=data["service"],
            date=data["date"],
            tenant_id=tenant_id
        )

        clear_session(
            tenant_id=tenant_id,
            user_id=user_id
        )

        return response

    return None



