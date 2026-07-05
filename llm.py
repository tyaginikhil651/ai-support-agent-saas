from google import genai
from memory import get_history
from config import (
    GEMINI_API_KEY,
    MODEL_NAME,
)

client = genai.Client(api_key=GEMINI_API_KEY)


def ask_llm(
    prompt,
    user_profile=None,
):
    """
    Send prompt to Gemini with personalization.
    """

    try:

        system_prompt = ""

        if user_profile:

            vip_score = user_profile.get(
                "vip_score",
                0,
            )

            complaint_count = user_profile.get(
                "complaint_count",
                0,
            )

            appointment_count = user_profile.get(
                "appointment_count",
                0,
            )

            sentiment_score = user_profile.get(
                "sentiment_score",
                0,
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
                    "Show empathy and apologize where appropriate.\n"
                )

            if sentiment_score < 0:
                system_prompt += (
                    "Customer appears frustrated. "
                    "Use a calm, empathetic and helpful tone.\n"
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

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=final_prompt,
        )

        return response.text

    except Exception as e:
        return f"LLM Error: {e}"


def ask_llm_with_memory(
    user_id,
    user_message,
    user_profile=None,
):
    """
    Generate response using conversation history.
    """

    history = get_history(str(user_id))

    context = ""

    for item in history:

        context += (
            f"{item['role']}: "
            f"{item['text']}\n"
        )

    prompt = f"""
Previous Conversation

{context}

Current User Message

{user_message}

Assistant:
"""

    return ask_llm(
        prompt,
        user_profile=user_profile,
    )


def classify(text):
    """
    Intent classification using Gemini.
    Returns only one intent.
    """

    prompt = f"""
You are an intent classifier.

Possible intents:

appointment
complaint
ticket_status
faq
chat

Rules:

Return ONLY one word.

No punctuation.

No explanation.

No sentence.

Message:

{text}
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        return response.text.strip().lower()

    except Exception:
        return "chat"


        