from langgraph.graph import StateGraph

from workflow_state import AgentState


def ask_service(state):

    state["response"] = (
        "Which service do you need?"
    )

    return state


def ask_date(state):

    state["response"] = (
        "What date would you like?"
    )

    return state


def ask_time(state):

    state["response"] = (
        "What time?"
    )

    return state


builder = StateGraph(AgentState)

builder.add_node(
    "service",
    ask_service
)

builder.add_node(
    "date",
    ask_date
)

builder.add_node(
    "time",
    ask_time
)

builder.set_entry_point(
    "service"
)

builder.add_edge(
    "service",
    "date"
)

builder.add_edge(
    "date",
    "time"
)

graph = builder.compile()