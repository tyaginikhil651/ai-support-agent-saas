from session_manager import (
    get_session,
    save_session,
    clear_session
)

from tools.appointment import (
    create_appointment
)


def handle_appointment(
    user_id,
    message
):

    session = get_session(user_id)

    if session["step"] is None:

        session["flow"] = "appointment"
        session["step"] = "service"

        save_session(
            user_id,
            session
        )

        return "Which service do you need?"


    if session["step"] == "service":

        session["service"] = message

        session["step"] = "date"

        save_session(
            user_id,
            session
        )

        return "What date would you like?"


    if session["step"] == "date":

        session["date"] = message

        session["step"] = "time"

        save_session(
            user_id,
            session
        )

        return "What time?"


    if session["step"] == "time":

        service = session["service"]

        date = session["date"]

        appointment = create_appointment(
            user_id,
            f"{service} | {date} | {message}"
        )

        clear_session(user_id)

        return appointment