from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from auth.auth_service import login_and_get_token
from auth.dependencies import get_current_admin


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class LoginRequest(BaseModel):
    tenant_slug: str
    username: str
    password: str


@router.post("/login")
def login_user(data: LoginRequest):
    result = login_and_get_token(
        tenant_slug=data.tenant_slug,
        username=data.username,
        password=data.password
    )

    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid company, username, or password"
        )

    return {
        "access_token": result["token"],
        "token_type": "bearer",
        "admin": result["admin"]
    }


@router.get("/me")
def get_me(
    admin=Depends(get_current_admin)
):
    return {
        "message": "Authenticated successfully",
        "admin": admin
    }

