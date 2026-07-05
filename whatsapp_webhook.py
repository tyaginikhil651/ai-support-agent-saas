from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import os

from services.tenant_whatsapp_service import get_tenant_by_phone_number_id
from graph.workflow import run_graph
from tools.customer import save_customer

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")


@app.get("/")
async def home():
    return {"status": "running"}


@app.get("/webhook")
async def verify(request: Request):

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse(
        "Verification failed",
        status_code=403
    )


@app.post("/webhook")
async def receive_message(request: Request):

    data = await request.json()

    try:
        value = data["entry"][0]["changes"][0]["value"]

        # Ignore delivery, read, and status events
        if "messages" not in value:
            return {"status": "ignored"}

        metadata = value.get("metadata", {})

        phone_number_id = metadata.get("phone_number_id")

        tenant = get_tenant_by_phone_number_id(phone_number_id)

        if not tenant:
            print("Unknown WhatsApp phone number:", phone_number_id)
            return {"status": "unknown_tenant"}

        whatsapp_message = value["messages"][0]

        sender_phone = whatsapp_message["from"]

        # Ignore non-text messages for now
        if whatsapp_message.get("type") != "text":
            return {"status": "unsupported_message_type"}

        message = whatsapp_message["text"]["body"]

        print("\n========================")
        print("TENANT:", tenant["company_name"])
        print("TENANT ID:", tenant["id"])
        print("SENDER:", sender_phone)
        print("MESSAGE:", message)
        print("========================\n")

        # Save customer under the correct tenant
        save_customer(
            tenant_id=tenant["id"],
            platform_user_id=sender_phone,
            username=sender_phone,
            phone=sender_phone
        )

        # run_graph returns a plain response string
        reply = run_graph(
            user_id=sender_phone,
            tenant_id=tenant["id"],
            message=message
        )

        from whatsapp_service import send_whatsapp_message

        send_whatsapp_message(
            phone_number_id=phone_number_id,
            to=sender_phone,
            text=reply
        )

        return {
            "status": "ok",
            "tenant_id": tenant["id"]
        }

    except Exception as e:
        print("Webhook error:", str(e))

        return {
            "status": "error",
            "message": str(e)
        }