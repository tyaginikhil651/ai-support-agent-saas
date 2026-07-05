from fastapi import WebSocket
from jose import JWTError, jwt

from auth.jwt_service import SECRET_KEY, ALGORITHM


async def get_websocket_admin(
    websocket: WebSocket
):
    token = websocket.cookies.get("access_token")

    if not token:
        await websocket.close(code=1008)
        return None

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        admin_id = payload.get("admin_id")
        tenant_id = payload.get("tenant_id")
        role = payload.get("role")

        if not admin_id or not tenant_id or not role:
            await websocket.close(code=1008)
            return None

        return {
            "admin_id": admin_id,
            "tenant_id": tenant_id,
            "role": role
        }

    except JWTError:
        await websocket.close(code=1008)
        return None






    