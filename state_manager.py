import json

from database import get_connection
from state_store import (
    get_state,
    save_state,
    clear_state
)

from graph.workflow import run_graph

from intent_classifier import detect_valid_intent


def process_message(
    user_id,
    message
):

    state = get_state(user_id)

    # --------------------------
    # No active workflow
    # --------------------------

    if not state:

        intent = detect_valid_intent(message)

        print("Detected Intent:", intent)

        # Appointment Flow

        if intent == "appointment":

            save_state(
                user_id,
                "waiting_service"
            )

            return (
                "What service do you need?"
            )

        # Complaint Flow

        if intent == "complaint":

            save_state(
                user_id,
                "waiting_issue"
            )

            return (
                "Please describe your issue."
            )

        return None

    # --------------------------
    # Appointment Flow
    # --------------------------

    if state["state"] == "waiting_service":

        save_state(
            user_id,
            "waiting_date",
            {
                "service": message
            }
        )

        return (
            "What date would you like?"
        )

    if state["state"] == "waiting_date":

        service = state["data"]["service"]

        result = run_graph(
            {
                "user_id": user_id,
                "intent": "appointment",
                "service": service,
                "date": message
            }
        )

        clear_state(user_id)

        return result["response"]

    # --------------------------
    # Complaint Flow
    # --------------------------

    if state["state"] == "waiting_issue":

        result = run_graph(
            {
                "user_id": user_id,
                "intent": "complaint",
                "issue": message
            }
        )

        clear_state(user_id)

        return result["response"]

    return None


def save_state(
    user_id,
    state,
    data=None
):

    conn = get_connection()

    conn.execute(
        """
        INSERT OR REPLACE INTO conversation_state(
            user_id,
            state,
            data
        )
        VALUES (?, ?, ?)
        """,
        (
            str(user_id),
            state,
            json.dumps(data or {})
        )
    )

    conn.commit()
    conn.close()


def get_state(user_id):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM conversation_state
        WHERE user_id=?
        """,
        (str(user_id),)
    ).fetchone()

    conn.close()

    if not row:
        return None

    return {
        "state": row["state"],
        "data": json.loads(row["data"] or "{}")
    }


def clear_state(user_id):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM conversation_state
        WHERE user_id=?
        """,
        (str(user_id),)
    )

    conn.commit()
    conn.close()