
import requests

from config import (
    WHATSAPP_TOKEN,
    PHONE_NUMBER_ID
)

def send_message(
    phone,
    message
):

    url = (
        f"https://graph.facebook.com/v23.0/"
        f"{PHONE_NUMBER_ID}/messages"
    )

    headers = {
        "Authorization":
        f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type":
        "application/json"
    }

    payload = {
        "messaging_product":
        "whatsapp",

        "to":
        phone,

        "type":
        "text",

        "text": {
            "body": message
        }
    }

    r = requests.post(
        url,
        headers=headers,
        json=payload
    )

    print(r.text)