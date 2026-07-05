from database import init_db
from graph.workflow import run_graph


init_db()

TENANT_ID = 1
USER_ID = "919670443252"

print("\nSTEP 1")
print(
    run_graph(
        user_id=USER_ID,
        tenant_id=TENANT_ID,
        message="I need an appointment"
    )
)

print("\nSTEP 2")
print(
    run_graph(
        user_id=USER_ID,
        tenant_id=TENANT_ID,
        message="Internet repair"
    )
)

print("\nSTEP 3")
print(
    run_graph(
        user_id=USER_ID,
        tenant_id=TENANT_ID,
        message="Tomorrow"
    )
)