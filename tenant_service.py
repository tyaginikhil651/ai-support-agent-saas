from database import get_connection


def get_tenant_by_whatsapp_phone_number_id(phone_number_id):
    conn = get_connection()

    tenant = conn.execute(
        """
        SELECT *
        FROM tenants
        WHERE whatsapp_phone_number_id=?
        AND status='active'
        """,
        (str(phone_number_id),)
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
        AND status='active'
        """,
        (slug,)
    ).fetchone()

    conn.close()

    return tenant


def connect_whatsapp_to_tenant(
    tenant_id,
    phone_number_id,
    business_account_id=None
):
    conn = get_connection()

    conn.execute(
        """
        UPDATE tenants
        SET
            whatsapp_phone_number_id=?,
            whatsapp_business_account_id=?
        WHERE id=?
        """,
        (
            str(phone_number_id),
            str(business_account_id)
            if business_account_id
            else None,
            tenant_id
        )
    )

    conn.commit()
    conn.close()