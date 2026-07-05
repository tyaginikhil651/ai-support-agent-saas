from database import get_connection
import re

def generate_slug(company_name):

    slug = company_name.lower()

    slug = re.sub(
        r'[^a-z0-9]+',
        '-',
        slug
    )

    return slug.strip("-")


def slug_exists(slug):

    conn = get_connection()

    company = conn.execute(
        """
        SELECT id
        FROM tenants
        WHERE slug=?
        """,
        (slug,)
    ).fetchone()

    conn.close()

    return company is not None


def unique_slug(company_name):

    base = generate_slug(
        company_name
    )

    slug = base

    counter = 1

    while slug_exists(slug):

        counter += 1

        slug = f"{base}-{counter}"

    return slug


# def create_company(
#     company_name,
#     email,
#     phone=None
# ):

#     conn = get_connection()

#     slug = unique_slug(
#         company_name
#     )

#     conn.execute(
#         """
#         INSERT INTO tenants
#         (
#             company_name,
#             slug,
#             email,
#             phone
#         )
#         VALUES
#         (?, ?, ?, ?)
#         """,
#         (
#             company_name,
#             slug,
#             email,
#             phone
#         )
#     )

#     conn.commit()

#     company = conn.execute(
#         """
#         SELECT *
#         FROM tenants
#         WHERE slug=?
#         """,
#         (slug,)
#     ).fetchone()

#     conn.close()

#     return dict(company)


def get_company(
    tenant_id
):

    conn = get_connection()

    company = conn.execute(
        """
        SELECT *
        FROM tenants
        WHERE id=?
        """,
        (tenant_id,)
    ).fetchone()

    conn.close()

    if company:
        return dict(company)

    return None


def get_company_by_slug(
    slug
):

    conn = get_connection()

    company = conn.execute(
        """
        SELECT *
        FROM tenants
        WHERE slug=?
        """,
        (slug,)
    ).fetchone()

    conn.close()

    if company:
        return dict(company)

    return None


import re

from database import get_connection


def create_slug(company_name: str) -> str:
    """
    Converts:
    'ABC Internet Pvt Ltd'
    into:
    'abc-internet-pvt-ltd'
    """

    slug = company_name.lower().strip()

    slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        slug
    )

    slug = slug.strip("-")

    return slug


def get_tenant_by_slug(slug: str):
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

    return dict(tenant) if tenant else None


def get_tenant_by_id(tenant_id: int):
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

    return dict(tenant) if tenant else None


def create_company(
    company_name: str,
    email: str = None,
    phone: str = None
):
    """
    Creates one SaaS tenant/company.

    Returns:
    {
        "id": 1,
        "company_name": "ABC Internet",
        "slug": "abc-internet",
        ...
    }
    """

    company_name = company_name.strip()

    if not company_name:
        raise ValueError("Company name is required")

    base_slug = create_slug(company_name)

    if not base_slug:
        raise ValueError(
            "Company name must contain letters or numbers"
        )

    conn = get_connection()

    slug = base_slug
    counter = 2

    # Make duplicate company slugs unique:
    # abc-internet
    # abc-internet-2
    # abc-internet-3
    while True:
        existing = conn.execute(
            """
            SELECT id
            FROM tenants
            WHERE slug=?
            """,
            (slug,)
        ).fetchone()

        if not existing:
            break

        slug = f"{base_slug}-{counter}"
        counter += 1

    conn.execute(
        """
        INSERT INTO tenants(
            company_name,
            slug,
            email,
            phone,
            whatsapp_phone_number_id,
            whatsapp_business_account_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            company_name,
            slug,
            email,
            phone,
            whatsapp_phone_number_id,
            whatsapp_business_account_id
        )
    )

    tenant_id = cursor.lastrowid

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

    return dict(tenant)


