from session_manager import get_session

from tools.complaint import create_complaint


def handle_complaint(
    user_id,
    message
):
    session = get_session(user_id)

    # Start Flow

    if session.get("step") is None:

        session["flow"] = "complaint"
        session["step"] = "issue"

        return (
            "Please describe your issue."
        )

    # Collect Issue

    if session["step"] == "issue":

        session["issue"] = message

        session["step"] = "priority"

        return (
            "What is the priority?\n\n"
            "Low\n"
            "Medium\n"
            "High\n"
            "Critical"
        )

    # Collect Priority

    if session["step"] == "priority":

        session["priority"] = message

        session["step"] = "phone"

        return (
            "Please provide your contact number."
        )

    # Collect Phone

    if session["step"] == "phone":

        session["phone"] = message

        issue_text = (
            f"Issue: {session['issue']}\n"
            f"Priority: {session['priority']}\n"
            f"Phone: {session['phone']}"
        )

        result = create_complaint(
            user_id,
            session["issue"],
            session["priority"]
        )

        session.clear()

        return result

    return (
        "Please continue describing your issue."
    )