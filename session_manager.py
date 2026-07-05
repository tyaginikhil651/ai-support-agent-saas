import json

from database import get_connection


def get_session(user_id):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM sessions
        WHERE user_id=?
        """,
        (str(user_id),)
    ).fetchone()

    conn.close()

    if row:

        return {
            "flow": row["flow"],
            "step": row["step"],
            **json.loads(row["data"])
        }

    return {
        "flow": None,
        "step": None
    }


def save_session(
    user_id,
    session
):

    conn = get_connection()

    flow = session.get("flow")
    step = session.get("step")

    data = dict(session)

    data.pop("flow", None)
    data.pop("step", None)

    conn.execute(
        """
        INSERT OR REPLACE INTO sessions(
            user_id,
            flow,
            step,
            data
        )
        VALUES(
            ?, ?, ?, ?
        )
        """,
        (
            str(user_id),
            flow,
            step,
            json.dumps(data)
        )
    )

    conn.commit()
    conn.close()


def clear_session(user_id):

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM sessions
        WHERE user_id=?
        """,
        (str(user_id),)
    )

    conn.commit()
    conn.close()