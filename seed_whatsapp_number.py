from services.tenant_whatsapp_service import connect_whatsapp_number

TENANT_ID = 1

PHONE_NUMBER_ID = "1294586107066425"

connect_whatsapp_number(
    tenant_id=TENANT_ID,
    phone_number_id=PHONE_NUMBER_ID,
    display_phone_number="Your WhatsApp Business Number",
    verify_token="Nikhil958$"
)

print("WhatsApp number connected to tenant successfully")


