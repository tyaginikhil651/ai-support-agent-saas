from database import init_db, get_connection
from auth.auth_service import hash_password


def create_owner(
    company_name: str,
    slug: str,
    company_email: str,
    company_phone: str,
    username: str,
    admin_email: str,
    password: str,
):
    init_db()

    conn = get_connection()

    try:
        # -----------------------------
        # Validate
        # -----------------------------
        if not company_name.strip():
            raise ValueError("Company name is required.")

        if not slug.strip():
            raise ValueError("Slug is required.")

        if not username.strip():
            raise ValueError("Username is required.")

        if not admin_email.strip():
            raise ValueError("Admin email is required.")

        if not password.strip():
            raise ValueError("Password is required.")

        slug = slug.strip().lower()

        # -----------------------------
        # Create / Find Tenant
        # -----------------------------
        tenant = conn.execute(
            """
            SELECT *
            FROM tenants
            WHERE slug = ?
            """,
            (slug,),
        ).fetchone()

        if tenant:

            tenant_id = tenant["id"]

            print(
                f"Using existing tenant: "
                f"{tenant['company_name']} (ID={tenant_id})"
            )

        else:

            cursor = conn.execute(
                """
                INSERT INTO tenants(
                    company_name,
                    slug,
                    email,
                    phone,
                    plan,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    company_name.strip(),
                    slug,
                    company_email.strip().lower(),
                    company_phone.strip(),
                    "starter",
                    "active",
                ),
            )

            tenant_id = cursor.lastrowid

            print(
                f"Created tenant '{company_name}' "
                f"(ID={tenant_id})"
            )

        # -----------------------------
        # Check duplicate username/email
        # -----------------------------
        existing = conn.execute(
            """
            SELECT *
            FROM admins

            WHERE tenant_id = ?

            AND (
                username = ?
                OR email = ?
            )
            """,
            (
                tenant_id,
                username.strip(),
                admin_email.strip().lower(),
            ),
        ).fetchone()

        if existing:

            print()

            print("Owner already exists.")

            print("Username :", existing["username"])
            print("Email    :", existing["email"])

            print()

            return tenant_id

        # -----------------------------
        # Create Owner
        # -----------------------------
        hashed_password = hash_password(password)

        conn.execute(
            """
            INSERT INTO admins(
                tenant_id,
                username,
                email,
                password,
                role,
                active
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                tenant_id,
                username.strip(),
                admin_email.strip().lower(),
                hashed_password,
                "owner",
                1,
            ),
        )

        conn.commit()

        print()
        print("=" * 50)
        print("OWNER CREATED SUCCESSFULLY")
        print("=" * 50)
        print("Tenant ID   :", tenant_id)
        print("Company     :", company_name)
        print("Slug        :", slug)
        print("Username    :", username)
        print("Email       :", admin_email)
        print("Role        : owner")
        print("=" * 50)
        print()

        return tenant_id

    except Exception as e:

        conn.rollback()

        print()

        print("=" * 50)
        print("FAILED TO CREATE OWNER")
        print("=" * 50)
        print(e)
        print("=" * 50)
        print()

        raise

    finally:

        conn.close()


if __name__ == "__main__":

    tenant_id = create_owner(
        company_name="ABC Internet",
        slug="abc-internet",
        company_email="admin@abcinternet.com",
        company_phone="+919999999999",
        username="nikhil",
        admin_email="admin@abcinternet.com",
        password="ChangeThisPassword123!",
    )

    print("Tenant ID:", tenant_id)