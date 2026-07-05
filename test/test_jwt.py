from auth.jwt_service import (
    decode_token
)

token = input("Token: ")

print(
    decode_token(token)
)