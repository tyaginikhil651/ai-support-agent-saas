from workflow_state import AgentState


def collect_service(state: AgentState):

    if not state.get("service"):

        state["response"] = (
            "Which service do you need?"
        )

    return state


def collect_date(state: AgentState):

    if not state.get("date"):

        state["response"] = (
            "What date would you like?"
        )

    return state


def confirm_booking(state: AgentState):

    state["response"] = (
        f"Appointment booked for "
        f"{state['service']} on "
        f"{state['date']}"
    )

    return state