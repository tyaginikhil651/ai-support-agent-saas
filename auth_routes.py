from passlib.context import CryptContext
from fastapi.responses import RedirectResponse

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# -------------------------
# Password Functions
# -------------------------

def hash_password(password):

    return pwd_context.hash(password)


def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# -------------------------
# Session Protection
# -------------------------

def require_login(request):

    if "user" not in request.session:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    return None


def require_role(
    request,
    roles
):

    if "user" not in request.session:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    if request.session.get("role") not in roles:

        return RedirectResponse(
            "/",
            status_code=303
        )

    return None


def require_role(
    request,
    allowed_roles
):
    role = request.session.get(
        "role"
    )

    if role not in allowed_roles:

        return RedirectResponse(
            "/login",
            status_code=303
        )

    return None


# use cases:
# role_check = require_role(
#     request,
#     ["Admin", "Manager"]
# )

# if role_check:
#     return role_check


# role_check = require_role(
#     request,
#     [
#         "Admin",
#         "Manager",
#         "Agent"
#     ]
# )


