import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
META_GRAPH_VERSION = "v23.0"


def send_whatsapp_message(
    phone_number_id: str,
    to: str,
    text: str
):
    if not ACCESS_TOKEN:
        raise RuntimeError(
            "META_ACCESS_TOKEN is missing. Add it to your .env file."
        )

    url = (
        f"https://graph.facebook.com/"
        f"{META_GRAPH_VERSION}/"
        f"{phone_number_id}/messages"
    )

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": str(to),
        "type": "text",
        "text": {
            "body": str(text)
        }
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=20
        )

        print("WhatsApp status:", response.status_code)
        print("WhatsApp response:", response.text)

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:
        print("WhatsApp send error:", str(error))

        return {
            "success": False,
            "error": str(error)
        }