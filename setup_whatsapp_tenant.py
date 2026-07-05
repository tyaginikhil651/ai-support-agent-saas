from tenant_service import connect_whatsapp_to_tenant


TENANT_ID = 1

PHONE_NUMBER_ID = "REPLACE_WITH_META_PHONE_NUMBER_ID"

WHATSAPP_BUSINESS_ACCOUNT_ID = None


connect_whatsapp_to_tenant(
    tenant_id=TENANT_ID,
    phone_number_id=PHONE_NUMBER_ID,
    business_account_id=WHATSAPP_BUSINESS_ACCOUNT_ID
)

print("WhatsApp number connected to tenant successfully")