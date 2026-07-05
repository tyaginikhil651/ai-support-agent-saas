from workflow_state import AgentState


def collect_complaint(state: AgentState):

    if not state.get("complaint"):

        state["response"] = (
            "Please describe your issue."
        )

    return state


def create_ticket(state: AgentState):

    state["response"] = (
        "Complaint registered."
    )

    return state