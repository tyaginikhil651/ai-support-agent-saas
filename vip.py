# vip.py

def get_customer_segment(user):

    if not user:
        return "Unknown"

    vip_score = user["vip_score"]
    complaints = user["complaint_count"]
    sentiment = user["sentiment_score"]

    # VIP Customers
    if vip_score >= 10:
        return "VIP"

    # Risk Customers
    if complaints >= 3:
        return "At Risk"

    if sentiment < -2:
        return "At Risk"

    # Regular Customers
    return "Normal"


def is_vip(user):

    if not user:
        return False

    return user["vip_score"] >= 10


def is_at_risk(user):

    if not user:
        return False

    return (
        user["complaint_count"] >= 3
        or user["sentiment_score"] < -2
    )