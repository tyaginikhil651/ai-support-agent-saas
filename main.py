from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from llm import ask_llm
from whatsapp_service import send_whatsapp_message
from state_manager import process_message
from dotenv import load_dotenv
import os

load_dotenv()

WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

app = FastAPI()


@app.get("/")
async def home():
    return {"status": "running"}


@app.get("/webhook")
async def verify(request: Request):

    print("\n====================")
    print("META VERIFICATION")
    print("====================")
    print(dict(request.query_params))

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    print("MODE:", mode)
    print("TOKEN:", token)
    print("CHALLENGE:", challenge)

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("VERIFIED")
        return PlainTextResponse(challenge)

    print("FAILED")

    return PlainTextResponse(
        "Verification failed",
        status_code=403
    )

# @app.post("/webhook")
# async def receive_message(request: Request):

#     data = await request.json()

#     print("\n====================")
#     print("WHATSAPP MESSAGE")
#     print("====================")
#     print(data)

#     return {"status": "ok"}

@app.post("/webhook")
async def receive_message(request: Request):

    data = await request.json()

    try:
        message = (
            data["entry"][0]
            ["changes"][0]
            ["value"]
            ["messages"][0]
            ["text"]
            ["body"]
        )

        sender = (
            data["entry"][0]
            ["changes"][0]
            ["value"]
            ["messages"][0]
            ["from"]
        )

        print("Sender:", sender)
        print("Message:", message)

        reply = process_message(sender,message)

        if not reply:
            reply = ask_llm(message)
        
        send_whatsapp_message(sender, reply)

    except Exception as e:
        print("Webhook Event:", e)

    return {"status": "ok"}