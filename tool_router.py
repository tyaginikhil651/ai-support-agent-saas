from tool_selector import choose_tool

from tools.appointment import create_appointment
from tools.complaint import create_complaint
from tools.faq import search_faq
from tools.ticket import track_ticket

from llm import ask_llm

from memory import ( get_history, add_message )
from tools.ticket_status import ticket_status
import re

from tools.ticket import ( get_ticket_status )
from appointment_flow import ( handle_appointment )
from complaint_flow import ( handle_complaint )
from tools.rag_tool import ( answer_from_docs )
from rag.qa import answer_question
from escalation import should_escalate, trigger_alert
from live.manager import manager
import asyncio
from memory_tracker import update_profile
from sentiment import detect_sentiment
from profile_service import get_profile
from vip import get_customer_segment




from intent_classifier import detect_intent
from graph.workflow import run_graph
from llm import ask_llm


def route_message(
    user_id,
    message,
    tenant_id
):
    intent = detect_intent(message)

    result = run_graph(
        user_id=str(user_id),
        message=message,
        tenant_id=int(tenant_id),
        intent=intent
    )

    response = result.get("response")

    if response:
        return response

    return ask_llm(message)





# def route_message(user_id, message):

#     profile = get_profile(user_id)

#     segment = get_customer_segment(profile)

#     print("Customer Segment:", segment)

#     sentiment_score = detect_sentiment(message)

#     update_profile(
#         user_id,
#         tool,
#         sentiment_score
#     )

#     if should_escalate(message, tool):

#         trigger_alert(user_id, message, tool)

#         asyncio.create_task(
#             manager.send(
#             f"🚨 LIVE ESCALATION\nUser: {user_id}\nMessage: {message}"
#             )
#         )

#         # return "⚠️ Your request has been escalated to a human agent."

#     if should_escalate(message, tool):

#         asyncio.create_task(
#             manager.send(
#                 f"🚨 LIVE ESCALATION\nUser: {user_id}\nMessage: {message}"
#             )
#         )

#         return (
#             "⚠️ Your request is important. "
#             "A human agent will join shortly."
#         )

#     if message.lower().startswith("track"):

#         ticket_id = (
#             message.replace(
#                 "track",
#                 ""
#             ).strip()
#         )

#         return track_ticket(
#             ticket_id
#         )

#     add_message(
#         user_id,
#         "user",
#         message
#     )

#     tool_data = choose_tool(message)

#     tool = tool_data.get("tool")
#     user_input = tool_data.get("input")

#     match = re.search(
#         r"TKT[A-Z0-9]+",
#         message.upper()
#     )

#     doc_answer = answer_from_docs(
#         message
#     )

#     if doc_answer:

#         return (
#             "📚 Knowledge Base\n\n"
#             + doc_answer
#         )

#     if match:

#         return get_ticket_status(
#             match.group()
#         )

#     if "ticket" in message.lower():

#         parts = message.split()

#         if len(parts) >= 2:

#             return ticket_status(parts[-1])

#     if tool == "appointment":

#         return handle_appointment(
#             user_id,
#             message
#         )

#     elif tool == "complaint":

#         return handle_complaint(
#             user_id,
#             message
#         )

#     elif tool == "faq":
        
#         return answer_question(
#             user_input
#         )

#     else:

#         history = get_history(user_id)

#         prompt = ""

#         for msg in history:
#             prompt += (
#                 f"{msg['role']}: "
#                 f"{msg['content']}\n"
#             )

#         prompt += "assistant:"

#         reply = ask_llm(prompt)

#     add_message(
#         user_id,
#         "assistant",
#         reply
#     )

#     return reply






