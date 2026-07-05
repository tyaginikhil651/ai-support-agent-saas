# from services.tenant_whatsapp_service import connect_whatsapp_number

# connect_whatsapp_number(
#     tenant_id=1,
#     phone_number_id="1294586107066425",
#     display_phone_number="+919670443252",
#     verify_token="Nikhil958$"
# )

# print("WhatsApp number connected successfully.")




from database import get_connection

PHONE_NUMBER_ID = "1294586107066425"

TENANT_ID = 1

DISPLAY_PHONE_NUMBER = "+919670443252"

VERIFY_TOKEN = "Nikhil958$"

conn = get_connection()

try:

    cursor = conn.execute(
        """
        UPDATE tenant_whatsapp_numbers
        SET
            tenant_id = ?,
            display_phone_number = ?,
            verify_token = ?,
            active = 1
        WHERE phone_number_id = ?
        """,
        (
            TENANT_ID,
            DISPLAY_PHONE_NUMBER,
            VERIFY_TOKEN,
            PHONE_NUMBER_ID,
        ),
    )

    conn.commit()

    if cursor.rowcount == 0:
        print("No matching WhatsApp number found.")
    else:
        print("WhatsApp number updated successfully.")

finally:
    conn.close()


