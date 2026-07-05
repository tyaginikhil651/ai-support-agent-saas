from database import init_db, get_connection
from tenant_operations import (
    get_tenant_analytics,
    get_tenant_escalated_tickets,
    get_tenant_vip_customers
)


init_db()

conn = get_connection()

conn.execute(
    """
    INSERT OR IGNORE INTO tenants (
        id,
        company_name,
        slug
    )
    VALUES (1, 'Tenant One', 'tenant-one')
    """
)

conn.execute(
    """
    INSERT OR IGNORE INTO tenants (
        id,
        company_name,
        slug
    )
    VALUES (2, 'Tenant Two', 'tenant-two')
    """
)

conn.execute(
    """
    INSERT INTO tickets (
        tenant_id,
        ticket_id,
        user_id,
        issue,
        escalated
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        1,
        "TKT-TENANT-ONE",
        "user-one",
        "Internet down",
        1
    )
)

conn.execute(
    """
    INSERT INTO tickets (
        tenant_id,
        ticket_id,
        user_id,
        issue,
        escalated
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        2,
        "TKT-TENANT-TWO",
        "user-two",
        "Router issue",
        1
    )
)

conn.execute(
    """
    INSERT OR REPLACE INTO customer_profile (
        tenant_id,
        user_id,
        vip_score
    )
    VALUES (?, ?, ?)
    """,
    (
        1,
        "user-one",
        15
    )
)

conn.execute(
    """
    INSERT OR REPLACE INTO customer_profile (
        tenant_id,
        user_id,
        vip_score
    )
    VALUES (?, ?, ?)
    """,
    (
        2,
        "user-two",
        20
    )
)

conn.commit()
conn.close()

print("\nTENANT ONE ANALYTICS")
print(get_tenant_analytics(1))

print("\nTENANT TWO ANALYTICS")
print(get_tenant_analytics(2))

print("\nTENANT ONE ESCALATIONS")
for ticket in get_tenant_escalated_tickets(1):
    print(dict(ticket))

print("\nTENANT TWO ESCALATIONS")
for ticket in get_tenant_escalated_tickets(2):
    print(dict(ticket))

print("\nTENANT ONE VIP CUSTOMERS")
for customer in get_tenant_vip_customers(1):
    print(dict(customer))

print("\nTENANT TWO VIP CUSTOMERS")
for customer in get_tenant_vip_customers(2):
    print(dict(customer))





