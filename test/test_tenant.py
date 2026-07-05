from services.tenant_service import create_company


company = create_company(
    company_name="ABC Internet",
    email="admin@abcinternet.com",
    phone="+919999999999"
)

print(company)