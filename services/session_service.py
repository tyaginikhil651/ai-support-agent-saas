import json
from database import get_connection


def get_session(
    tenant_id: int,
    user_id: str
):
    conn = get_connection()

    row = conn.execute(
        """
        SELECT flow, step, data
        FROM sessions
        WHERE tenant_id = ?
        AND user_id = ?
        """,
        (
            tenant_id,
            str(user_id)
        )
    ).fetchone()

    conn.close()

    if row is None:
        return None

    try:
        data = json.loads(row["data"] or "{}")
    except json.JSONDecodeError:
        data = {}

    return {
        "flow": row["flow"],
        "step": row["step"],
        "data": data
    }


def save_session(
    tenant_id: int,
    user_id: str,
    flow: str,
    step: str,
    data: dict | None = None
):
    if data is None:
        data = {}

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO sessions (
            tenant_id,
            user_id,
            flow,
            step,
            data,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)

        ON CONFLICT(tenant_id, user_id)
        DO UPDATE SET
            flow = excluded.flow,
            step = excluded.step,
            data = excluded.data,
            updated_at = CURRENT_TIMESTAMP
        """,
        (
            tenant_id,
            str(user_id),
            flow,
            step,
            json.dumps(data)
        )
    )

    conn.commit()
    conn.close()


def clear_session(
    tenant_id: int,
    user_id: str
):
    conn = get_connection()

    conn.execute(
        """
        DELETE FROM sessions
        WHERE tenant_id = ?
        AND user_id = ?
        """,
        (
            tenant_id,
            str(user_id)
        )
    )

    conn.commit()
    conn.close()


