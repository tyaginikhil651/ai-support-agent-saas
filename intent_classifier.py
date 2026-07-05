from llm import ask_llm
from llm import classify


FAQ_KEYWORDS = [
    "timing",
    "timings",
    "hours",
    "price",
    "pricing",
    "address",
    "location",
    "policy",
    "refund",
    "support",
    "services"
]


VALID_INTENTS = [
    "appointment",
    "complaint",
    "ticket_status",
    "faq",
    "chat"
]


def detect_valid_intent(message):

    prompt = f"""
Classify this customer message into ONE category:

appointment
complaint
ticket_status
faq
chat

Message:
{message}

Return only category name.
"""

    try:

        intent = classify(prompt)

        intent = intent.strip().lower()

        if intent in VALID_INTENTS:
            return intent

    except Exception as e:
        print("Intent Error:", e)

    return "chat"

def detect_intent(message):

    text = message.lower()

    # Fast keyword detection

    if any(word in text for word in FAQ_KEYWORDS):
        return "faq"

    intent = classify(message)

    intent = intent.lower().strip()

    if "appointment" in intent:
        return "appointment"

    if "complaint" in intent:
        return "complaint"

    if "ticket" in intent:
        return "ticket_status"

    if "faq" in intent:
        return "faq"

    return "chat"