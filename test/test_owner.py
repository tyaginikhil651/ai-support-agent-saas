from auth.auth_service import create_owner


owner = create_owner(
    tenant_id=1,
    username="nikhil",
    email="admin@abcinternet.com",
    password="ChangeThisPassword123!"
)

print(owner)