from whatsapp_service import notify_agent
from services.email_service import send_email_alert

def should_escalate(message: str, intent: str):

    notify_agent(message)
    msg = message.lower()

    urgent_keywords = [
        "urgent", "asap", "not working", "down",
        "refund", "angry", "bad service",
        "complain", "escalate", "manager"
    ]

    if intent in ["complaint", "ticket_status"]:
        return True

    if any(word in msg for word in urgent_keywords):
        return True

    return False

def trigger_alert(user_id, message, intent):

    subject = f"🚨 LIVE ESCALATION - User {user_id}"

    body = f"""
                🔥 NEW SUPPORT ESCALATION

                ━━━━━━━━━━━━━━━━━━━━
                User ID: {user_id}
                Intent: {intent}
                ━━━━━━━━━━━━━━━━━━━━

                💬 Message:
                {message}

                ━━━━━━━━━━━━━━━━━━━━
                Action Required: IMMEDIATE
                ━━━━━━━━━━━━━━━━━━━━
            """

    send_email_alert(subject, body)