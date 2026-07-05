from database import get_connection


def connect_whatsapp_number(
    tenant_id,
    phone_number_id,
    display_phone_number=None,
    verify_token=None
):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO tenant_whatsapp_numbers(
            tenant_id,
            phone_number_id,
            display_phone_number,
            verify_token
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            tenant_id,
            phone_number_id,
            display_phone_number,
            verify_token
        )
    )

    conn.commit()
    conn.close()


def get_tenant_by_phone_number_id(phone_number_id):
    conn = get_connection()

    tenant = conn.execute(
        """
        SELECT
            t.*,
            w.phone_number_id,
            w.display_phone_number,
            w.verify_token
        FROM tenant_whatsapp_numbers w
        JOIN tenants t
            ON t.id = w.tenant_id
        WHERE w.phone_number_id=?
          AND w.active=1
          AND t.status='active'
        """,
        (str(phone_number_id),)
    ).fetchone()

    conn.close()

    return tenant


