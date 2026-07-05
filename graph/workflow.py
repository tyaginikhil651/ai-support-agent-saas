from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

from graph.nodes import (
    appointment_node,
    complaint_node,
    ticket_status_node,
    chat_node
)

from intent_classifier import detect_intent
from services.session_service import get_session
from services.appointment_flow import (
    start_appointment_flow,
    continue_appointment_flow
)
from services.customer_profile_service import (
    update_profile,
    calculate_vip_score
)


class SupportState(TypedDict):
    user_id: str
    tenant_id: int
    message: str
    intent: Optional[str]
    service: Optional[str]
    date: Optional[str]
    ticket_id: Optional[str]
    response: Optional[str]


def detect_intent_node(state: SupportState):

    intent = detect_intent(state["message"])

    return {
        "intent": intent
    }


def route_intent(state: SupportState):

    intent = state.get("intent", "chat")

    if intent == "appointment":
        return "appointment"

    if intent == "complaint":
        return "complaint"

    if intent == "ticket_status":
        return "ticket_status"

    return "chat"


def build_graph():

    workflow = StateGraph(SupportState)

    workflow.add_node(
        "detect_intent",
        detect_intent_node
    )

    workflow.add_node(
        "appointment",
        appointment_node
    )

    workflow.add_node(
        "complaint",
        complaint_node
    )

    workflow.add_node(
        "ticket_status",
        ticket_status_node
    )

    workflow.add_node(
        "chat",
        chat_node
    )

    workflow.set_entry_point("detect_intent")

    workflow.add_conditional_edges(
        "detect_intent",
        route_intent,
        {
            "appointment": "appointment",
            "complaint": "complaint",
            "ticket_status": "ticket_status",
            "chat": "chat"
        }
    )

    workflow.add_edge("appointment", END)
    workflow.add_edge("complaint", END)
    workflow.add_edge("ticket_status", END)
    workflow.add_edge("chat", END)

    return workflow.compile()


graph = build_graph()

def run_graph(
    user_id: str,
    tenant_id: int,
    message: str
):
    user_id = str(user_id)
    tenant_id = int(tenant_id)
    message = message.strip()

    # ----------------------------------
    # 1. Continue existing multi-turn flow
    # ----------------------------------

    active_session = get_session(
        tenant_id=tenant_id,
        user_id=user_id
    )

    if active_session:

        if active_session["flow"] == "appointment":

            response = continue_appointment_flow(
                tenant_id=tenant_id,
                user_id=user_id,
                message=message
            )

        if response:

            update_profile(
                tenant_id=tenant_id,
                user_id=user_id,
                intent="appointment"
            )

            calculate_vip_score(
                tenant_id=tenant_id,
                user_id=user_id
            )

            return response

    # ----------------------------------
    # 2. Detect new intent
    # ----------------------------------

    intent = detect_intent(message)

    # Count every incoming customer message.
    # Do not count an appointment until it is actually booked.
    profile_intent = intent

    if intent == "appointment":
        profile_intent = None

    update_profile(
        tenant_id=tenant_id,
        user_id=user_id,
        intent=profile_intent
    )

    calculate_vip_score(
        tenant_id=tenant_id,
        user_id=user_id
    )

    # ----------------------------------
    # 3. Start appointment flow
    # ----------------------------------

    if intent == "appointment":

        return start_appointment_flow(
            tenant_id=tenant_id,
            user_id=user_id
        )

    # ----------------------------------
    # 4. Existing LangGraph workflow
    # ----------------------------------

    result = graph.invoke(
        {
            "user_id": user_id,
            "tenant_id": tenant_id,
            "message": message,
            "intent": intent,
            "service": None,
            "date": None,
            "ticket_id": None,
            "response": None
        }
    )

    return result.get(
        "response",
        "Sorry, I could not process your request."
    )

