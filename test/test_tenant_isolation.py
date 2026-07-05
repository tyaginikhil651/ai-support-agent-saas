from database import init_db, get_connection
from tools.complaint import create_complaint
from tools.customer import ticket_status


init_db()

conn = get_connection()

conn.execute("""
INSERT OR IGNORE INTO tenants
(company_name, slug, email)
VALUES (?, ?, ?)
""", (
    "Company One",
    "company-one",
    "one@example.com"
))

conn.execute("""
INSERT OR IGNORE INTO tenants
(company_name, slug, email)
VALUES (?, ?, ?)
""", (
    "Company Two",
    "company-two",
    "two@example.com"
))

conn.commit()

tenant_one = conn.execute(
    "SELECT id FROM tenants WHERE slug=?",
    ("company-one",)
).fetchone()["id"]

tenant_two = conn.execute(
    "SELECT id FROM tenants WHERE slug=?",
    ("company-two",)
).fetchone()["id"]

conn.close()

result = create_complaint(
    user_id="919670443252",
    issue="Internet is not working",
    tenant_id=tenant_one
)

print(result)

ticket_id = result.split("Ticket ID: ")[1].split("\n")[0]

print("\nTenant One checks ticket:")
print(
    ticket_status(
        tenant_id=tenant_one,
        ticket_id=ticket_id
    )
)

print("\nTenant Two checks same ticket:")
print(
    ticket_status(
        tenant_id=tenant_two,
        ticket_id=ticket_id
    )
)



