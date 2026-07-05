from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

from graph.nodes import (
    appointment_node,
    complaint_node,
    ticket_status_node,
    chat_node
)


class AgentState(TypedDict):
    user_id: str
    tenant_id: int
    message: str
    intent: str

    service: Optional[str]
    date: Optional[str]
    ticket_id: Optional[str]

    response: Optional[str]


def route_intent(state: AgentState):

    intent = state.get("intent", "chat")

    if intent == "appointment":
        return "appointment"

    if intent == "complaint":
        return "complaint"

    if intent == "ticket_status":
        return "ticket_status"

    return "chat"


builder = StateGraph(AgentState)

builder.add_node("appointment", appointment_node)
builder.add_node("complaint", complaint_node)
builder.add_node("ticket_status", ticket_status_node)
builder.add_node("chat", chat_node)

builder.set_conditional_entry_point(
    route_intent,
    {
        "appointment": "appointment",
        "complaint": "complaint",
        "ticket_status": "ticket_status",
        "chat": "chat"
    }
)

builder.add_edge("appointment", END)
builder.add_edge("complaint", END)
builder.add_edge("ticket_status", END)
builder.add_edge("chat", END)

graph = builder.compile()


