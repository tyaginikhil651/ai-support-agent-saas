from database import get_connection


def ensure_profile(
    tenant_id: int,
    user_id: str
):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO customer_profile (
            tenant_id,
            user_id
        )
        VALUES (?, ?)

        ON CONFLICT(tenant_id, user_id)
        DO NOTHING
        """,
        (
            tenant_id,
            str(user_id)
        )
    )

    conn.commit()
    conn.close()


def update_profile(
    tenant_id: int,
    user_id: str,
    intent: str | None = None,
    sentiment_score: float | None = None
):
    ensure_profile(
        tenant_id=tenant_id,
        user_id=user_id
    )

    conn = get_connection()

    updates = [
        "total_messages = total_messages + 1",
        "last_active = CURRENT_TIMESTAMP"
    ]

    values = []

    if intent:
        updates.append("last_intent = ?")
        values.append(intent)

    if sentiment_score is not None:
        updates.append("sentiment_score = ?")
        values.append(sentiment_score)

    if intent == "complaint":
        updates.append(
            "complaint_count = complaint_count + 1"
        )

    if intent == "appointment":
        updates.append(
            "appointment_count = appointment_count + 1"
        )

    values.extend(
        [
            tenant_id,
            str(user_id)
        ]
    )

    conn.execute(
        f"""
        UPDATE customer_profile
        SET {", ".join(updates)}
        WHERE tenant_id = ?
        AND user_id = ?
        """,
        values
    )

    conn.commit()
    conn.close()


def get_customer_profile(
    tenant_id: int,
    user_id: str
):
    conn = get_connection()

    profile = conn.execute(
        """
        SELECT *
        FROM customer_profile
        WHERE tenant_id = ?
        AND user_id = ?
        """,
        (
            tenant_id,
            str(user_id)
        )
    ).fetchone()

    conn.close()

    return profile


def calculate_vip_score(
    tenant_id: int,
    user_id: str
):
    profile = get_customer_profile(
        tenant_id=tenant_id,
        user_id=user_id
    )

    if profile is None:
        return 0

    score = 0

    score += profile["complaint_count"] * 2
    score += profile["appointment_count"] * 3
    score += min(profile["total_messages"], 20) * 0.2

    conn = get_connection()

    conn.execute(
        """
        UPDATE customer_profile
        SET vip_score = ?
        WHERE tenant_id = ?
        AND user_id = ?
        """,
        (
            score,
            tenant_id,
            str(user_id)
        )
    )

    conn.commit()
    conn.close()

    return score


