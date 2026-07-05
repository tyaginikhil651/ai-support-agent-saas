from database import get_connection


def get_profile(user_id):

    conn = get_connection()

    profile = conn.execute(
        """
        SELECT *
        FROM customer_profile
        WHERE user_id=?
        """,
        (str(user_id),)
    ).fetchone()

    conn.close()

    if profile:
        return dict(profile)

    return None