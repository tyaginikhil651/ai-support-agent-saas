import os

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt


SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "development-only-change-this-before-production"
)

ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24


def create_token(data: dict) -> str:
    payload = data.copy()

    payload["exp"] = (
        datetime.now(timezone.utc)
        + timedelta(hours=TOKEN_EXPIRE_HOURS)
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_token(token: str):
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except JWTError:
        return None