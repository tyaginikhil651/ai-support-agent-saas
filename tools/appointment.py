from database import get_connection


def create_appointment(
    user_id,
    service,
    date,
    tenant_id=None
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO appointments
        (
            user_id,
            service,
            date,
            tenant_id
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            str(user_id),
            service,
            date,
            tenant_id
        )
    )

    conn.commit()
    conn.close()

    return (
        f"Appointment booked successfully.\n\n"
        f"Service: {service}\n"
        f"Date: {date}"
    )




