from fastapi import Request, HTTPException
from auth.jwt_handler import verify_token

def get_current_admin(request: Request):
    """
    Reads JWT from the browser cookie and returns the
    authenticated admin payload.
    """

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload
