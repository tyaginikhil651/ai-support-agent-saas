from tenants import create_tenant

tenant = create_tenant(
    company_name="ABC Internet",
    slug="abc-internet",
    email="admin@abcinternet.com",
    phone="+919999999999"
)

print("Tenant created:")
print(dict(tenant))