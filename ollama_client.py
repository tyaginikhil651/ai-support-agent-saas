import requests
from memory import get_history

from config import (
    OLLAMA_URL,
    MODEL_NAME
)
import requests


# def ask_llm(prompt):
#     """
#     Send prompt to Ollama.
#     """

#     try:

#         response = requests.post(
#             OLLAMA_URL,
#             json={
#                 "model": MODEL_NAME,
#                 "prompt": prompt,
#                 "stream": False
#             },
#             timeout=120
#         )

#         data = response.json()

#         return data.get(
#             "response",
#             "No response."
#         )

#     except Exception as e:
#         return f"LLM Error: {e}"


def ask_llm(
    prompt,
    user_profile=None
):
    """
    Send prompt to Ollama with personalization.
    """

    try:

        system_prompt = ""

        if user_profile:

            vip_score = user_profile.get(
                "vip_score", 0
            )

            complaint_count = user_profile.get(
                "complaint_count", 0
            )

            appointment_count = user_profile.get(
                "appointment_count", 0
            )

            sentiment_score = user_profile.get(
                "sentiment_score", 0
            )

            if vip_score > 10:
                system_prompt += (
                    "This is a VIP customer. "
                    "Provide premium support. "
                    "Be polite and prioritize their request.\n"
                )

            if complaint_count > 3:
                system_prompt += (
                    "Customer has multiple complaints. "
                    "Show empathy and apologize when appropriate.\n"
                )

            if sentiment_score < 0:
                system_prompt += (
                    "Customer appears frustrated. "
                    "Use a calm and helpful tone.\n"
                )

            if appointment_count > 5:
                system_prompt += (
                    "Customer is a frequent service user.\n"
                )

        final_prompt = f"""
{system_prompt}

Customer Message:
{prompt}

Assistant:
"""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": final_prompt,
                "stream": False
            },
            timeout=120
        )

        data = response.json()

        return data.get(
            "response",
            "No response."
        )

    except Exception as e:
        return f"LLM Error: {e}"


def ask_llm_with_memory(
    user_id,
    user_message
):

    history = get_history(
        str(user_id)
    )

    context = ""

    for item in history:

        context += (
            f"{item['role']}: "
            f"{item['text']}\n"
        )

    prompt = f"""
Previous Conversation:

{context}

User:
{user_message}

Assistant:
"""

    return ask_llm(prompt)



def classify(text):

    prompt = f"""
You are an intent classifier.

Possible intents:

appointment
complaint
ticket_status
faq
chat

Rules:
- Return ONLY the intent.
- Return ONE WORD ONLY.
- No explanation.
- No punctuation.
- No sentences.

Message:
{text}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip().lower()