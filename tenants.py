from database import get_connection


def create_tenant(
    company_name,
    slug,
    email=None,
    phone=None,
    plan="starter"
):
    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tenants (
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
            company_name,
            slug,
            email,
            phone,
            plan,
            "active"
        )
    )

    tenant_id = cur.lastrowid

    conn.commit()

    tenant = conn.execute(
        """
        SELECT *
        FROM tenants
        WHERE id=?
        """,
        (tenant_id,)
    ).fetchone()

    conn.close()

    return tenant


def get_tenant_by_id(tenant_id):
    conn = get_connection()

    tenant = conn.execute(
        """
        SELECT *
        FROM tenants
        WHERE id=?
        """,
        (tenant_id,)
    ).fetchone()

    conn.close()

    return tenant


def get_tenant_by_slug(slug):
    conn = get_connection()

    tenant = conn.execute(
        """
        SELECT *
        FROM tenants
        WHERE slug=?
        """,
        (slug,)
    ).fetchone()

    conn.close()

    return tenant