from database import get_connection


def save_reply(
    ticket_id,
    sender,
    message
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO replies
        (
            ticket_id,
            sender,
            message
        )
        VALUES (?, ?, ?)
        """,
        (
            ticket_id,
            sender,
            message
        )
    )

    conn.commit()
    conn.close()