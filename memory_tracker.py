from database import get_connection
from datetime import datetime


def update_profile(user_id, intent, sentiment_score=0):

    conn = get_connection()

    user = conn.execute(
        "SELECT * FROM customer_profile WHERE user_id=?",
        (user_id,)
    ).fetchone()

    if not user:

        conn.execute("""
        INSERT INTO customer_profile (user_id, total_messages)
        VALUES (?, 1)
        """, (user_id,))

        conn.commit()
        conn.close()
        return


    # Update counters
    total_messages = user["total_messages"] + 1

    complaint_count = user["complaint_count"]
    appointment_count = user["appointment_count"]

    if intent == "complaint":
        complaint_count += 1

    if intent == "appointment":
        appointment_count += 1

    # Sentiment update (simple rolling average)
    new_sentiment = (
        (user["sentiment_score"] + sentiment_score) / 2
    )

    # VIP scoring logic
    vip_score = (
        appointment_count * 5
        + total_messages * 0.5
        - complaint_count * 4
        + sentiment_score * 2
        + (total_messages * 0.1)
    )

    conn.execute("""
    UPDATE customer_profile
    SET total_messages=?,
        complaint_count=?,
        appointment_count=?,
        sentiment_score=?,
        last_intent=?,
        last_active=?,
        vip_score=?
    WHERE user_id=?
    """, (
        total_messages,
        complaint_count,
        appointment_count,
        new_sentiment,
        intent,
        datetime.now(),
        vip_score,
        user_id
    ))

    conn.commit()
    conn.close()