import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from tool_router import route_message
from whatsapp_service import send_whatsapp_message
from tools.customer import save_customer

app = FastAPI()

# ----------------------------------
# Meta Verify Token
# ----------------------------------

VERIFY_TOKEN = "Nikhil958$"

# ----------------------------------
# Home
# ----------------------------------

@app.get("/")
async def home():

    return {
        "status": "running",
        "service": "AI Support Agent"
    }

# ----------------------------------
# Meta Verification
# ----------------------------------

@app.get("/webhook")
async def verify(request: Request):

    print("\n========================")
    print("META VERIFICATION")
    print("========================")

    params = dict(request.query_params)

    print(params)

    mode = request.query_params.get(
        "hub.mode"
    )

    token = request.query_params.get(
        "hub.verify_token"
    )

    challenge = request.query_params.get(
        "hub.challenge"
    )

    save_customer(
        sender,
        "WhatsApp User",
        sender
    )

    if (
        mode == "subscribe"
        and token == VERIFY_TOKEN
    ):

        print("Webhook Verified")

        return PlainTextResponse(
            challenge
        )

    return PlainTextResponse(
        "Verification failed",
        status_code=403
    )

# ----------------------------------
# Receive WhatsApp Messages
# ----------------------------------

@app.post("/webhook")
async def receive_message(request: Request):

    data = await request.json()

    print("\n========================")
    print("WHATSAPP WEBHOOK")
    print("========================")
    print(data)

    try:

        value = (
            data["entry"][0]
            ["changes"][0]
            ["value"]
        )

        if "messages" not in value:

            return {
                "status": "ignored"
            }

        message_data = value["messages"][0]

        sender = message_data["from"]

        message_type = message_data["type"]

        if message_type != "text":

            send_whatsapp_message(
                sender,
                "Currently I only support text messages."
            )

            return {
                "status": "unsupported_message"
            }

        message = (
            message_data["text"]["body"]
        )

        print(
            f"\nSender: {sender}"
        )

        print(
            f"Message: {message}"
        )

        # ----------------------------------
        # Route Message
        # ----------------------------------

        reply = route_message(
            sender,
            message
        )

        print(
            f"Reply: {reply}"
        )

        # ----------------------------------
        # Send Response
        # ----------------------------------

        send_whatsapp_message(
            sender,
            reply
        )

    except Exception as e:

        print(
            "\nWebhook Error:"
        )

        print(e)

    return {
        "status": "ok"
    }

# ----------------------------------
# Run Locally
# ----------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "webhook:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )