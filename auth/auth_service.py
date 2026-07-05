import sqlite3

from database import get_connection
from auth.password_service import (
    hash_password,
    verify_password
)
from auth.jwt_service import create_token


VALID_ROLES = {
    "owner",
    "manager",
    "agent"
}


def create_owner(
    tenant_id: int,
    username: str,
    email: str,
    password: str
):
    username = username.strip()
    email = email.strip().lower()

    if not username:
        raise ValueError("Username is required")

    if not email:
        raise ValueError("Email is required")

    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO admins(
                tenant_id,
                username,
                email,
                password,
                role
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                tenant_id,
                username,
                email,
                hash_password(password),
                "owner"
            )
        )

        conn.commit()

        admin_id = cursor.lastrowid

        admin = conn.execute(
            """
            SELECT
                id,
                tenant_id,
                username,
                email,
                role,
                active,
                created_at
            FROM admins
            WHERE id=?
            """,
            (admin_id,)
        ).fetchone()

        return dict(admin)

    except sqlite3.IntegrityError:
        raise ValueError(
            "This username or email is already used in this company"
        )

    finally:
        conn.close()


def create_admin(
    tenant_id: int,
    username: str,
    email: str,
    password: str,
    role: str = "agent"
):
    role = role.lower().strip()

    if role not in VALID_ROLES:
        raise ValueError(
            "Role must be owner, manager, or agent"
        )

    if role == "owner":
        return create_owner(
            tenant_id,
            username,
            email,
            password
        )

    username = username.strip()
    email = email.strip().lower()

    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO admins(
                tenant_id,
                username,
                email,
                password,
                role
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                tenant_id,
                username,
                email,
                hash_password(password),
                role
            )
        )

        conn.commit()

        admin_id = cursor.lastrowid

        admin = conn.execute(
            """
            SELECT
                id,
                tenant_id,
                username,
                email,
                role,
                active,
                created_at
            FROM admins
            WHERE id=?
            """,
            (admin_id,)
        ).fetchone()

        return dict(admin)

    except sqlite3.IntegrityError:
        raise ValueError(
            "This username or email is already used in this company"
        )

    finally:
        conn.close()


def login(
    tenant_slug: str,
    username: str,
    password: str
):
    """
    Login requires the company slug.
    This prevents username collisions between companies.
    """

    conn = get_connection()

    admin = conn.execute(
        """
        SELECT
            admins.id,
            admins.tenant_id,
            admins.username,
            admins.email,
            admins.password,
            admins.role,
            admins.active,
            tenants.company_name,
            tenants.slug,
            tenants.status AS tenant_status
        FROM admins
        JOIN tenants
            ON admins.tenant_id = tenants.id
        WHERE tenants.slug=?
          AND admins.username=?
        """,
        (
            tenant_slug.strip().lower(),
            username.strip()
        )
    ).fetchone()

    conn.close()

    if not admin:
        return None

    admin = dict(admin)

    if admin["active"] != 1:
        return None

    if admin["tenant_status"] != "active":
        return None

    if not verify_password(
        password,
        admin["password"]
    ):
        return None

    # Never return password hash outside auth service
    admin.pop("password", None)

    return admin


def login_and_get_token(
    tenant_slug: str,
    username: str,
    password: str
):
    admin = login(
        tenant_slug,
        username,
        password
    )

    if not admin:
        return None

    token = create_token(
        {
            "admin_id": admin["id"],
            "tenant_id": admin["tenant_id"],
            "tenant_slug": admin["slug"],
            "role": admin["role"],
            "username": admin["username"]
        }
    )

    return {
        "token": token,
        "admin": admin
    }








