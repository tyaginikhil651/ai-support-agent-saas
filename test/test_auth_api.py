import requests


BASE_URL = "http://127.0.0.1:8000"


login_data = {
    "tenant_slug": "abc-internet",
    "username": "nikhil",
    "password": "ChangeThisPassword123!"
}


login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json=login_data
)

print("LOGIN STATUS:", login_response.status_code)
print("LOGIN BODY:", login_response.json())


if login_response.status_code == 200:
    token = login_response.json()["access_token"]

    me_response = requests.get(
        f"{BASE_URL}/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    print("\nME STATUS:", me_response.status_code)
    print("ME BODY:", me_response.json())

