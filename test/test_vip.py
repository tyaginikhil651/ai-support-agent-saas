# test_vip.py

from profile_service import get_profile
from vip import (
    is_vip,
    is_at_risk,
    get_customer_segment
)

user_id = "1"

profile = get_profile(user_id)

print(profile)

print(
    "VIP:",
    is_vip(profile)
)

print(
    "Risk:",
    is_at_risk(profile)
)

print(
    "Segment:",
    get_customer_segment(profile)
)