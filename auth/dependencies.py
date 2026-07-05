from fastapi import (
    Header,
    Request,
    HTTPException
)

from auth.jwt_service import decode_token


def _get_token_from_request(
    request: Request,
    authorization: str = Header(default=None)
):
    """
    Priority:
    1. Authorization: Bearer <token> header
    2. access_token browser cookie
    """

    if authorization:
        parts = authorization.split(" ", 1)

        if len(parts) == 2:
            scheme, token = parts

            if scheme.lower() == "bearer" and token.strip():
                return token.strip()

    cookie_token = request.cookies.get(
        "access_token"
    )

    if cookie_token:
        return cookie_token

    return None


def get_current_admin(
    request: Request,
    authorization: str = Header(default=None)
):
    token = _get_token_from_request(
        request,
        authorization
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Login required"
        )

    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired login"
        )

    required_fields = [
        "admin_id",
        "tenant_id",
        "role",
        "username"
    ]

    missing = [
        field
        for field in required_fields
        if field not in payload
    ]

    if missing:
        raise HTTPException(
            status_code=401,
            detail="Invalid login token"
        )

    return payload


def require_roles(*allowed_roles):
    def role_guard(
        request: Request,
        authorization: str = Header(default=None)
    ):
        admin = get_current_admin(
            request,
            authorization
        )

        if admin["role"] not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission for this action"
            )

        return admin

    return role_guard




