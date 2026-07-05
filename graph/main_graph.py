from langgraph.graph import StateGraph

from workflow_state import AgentState

from graph.appointment_graph import (
    collect_service,
    collect_date,
    confirm_booking
)

builder = StateGraph(AgentState)

builder.add_node(
    "service",
    collect_service
)

builder.add_node(
    "date",
    collect_date
)

builder.add_node(
    "confirm",
    confirm_booking
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
    "confirm"
)

graph = builder.compile()