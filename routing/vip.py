def is_vip(profile):

    return (
        profile["vip_score"] > 10
    )

# if is_vip(profile):

#     agent = conn.execute("""
#     SELECT *
#     FROM agents

#     WHERE status='online'

#     ORDER BY active_tickets

#     LIMIT 1
#     """).fetchone()