from services.tenant_whatsapp_service import get_tenant_by_phone_number_id

PHONE_NUMBER_ID = "1294586107066425"

tenant = get_tenant_by_phone_number_id(PHONE_NUMBER_ID)

if tenant:
    print("Tenant found:")
    print(dict(tenant))
else:
    print("No tenant found")