# from auth.auth_service import (
#     login_and_get_token
# )

# token = login_and_get_token(

#     "nikhil",

#     "123456"
# )

# print(token)


from auth.auth_service import login_and_get_token


result = login_and_get_token(
    tenant_slug="abc-internet",
    username="nikhil",
    password="ChangeThisPassword123!"
)

print(result)


