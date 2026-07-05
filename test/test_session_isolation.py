from database import init_db
from graph.workflow import run_graph


init_db()

USER_ID = "919670443252"

print("\n--- Tenant One starts appointment ---")

print(
    run_graph(
        user_id=USER_ID,
        tenant_id=1,
        message="I need an appointment"
    )
)

print("\n--- Tenant Two sends unrelated message ---")

print(
    run_graph(
        user_id=USER_ID,
        tenant_id=2,
        message="Hello"
    )
)

print("\n--- Tenant One continues appointment ---")

print(
    run_graph(
        user_id=USER_ID,
        tenant_id=1,
        message="Internet repair"
    )
)



