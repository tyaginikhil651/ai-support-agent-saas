from database import init_db
from graph.workflow import run_graph
from services.customer_profile_service import get_customer_profile


init_db()

TENANT_ID = 1
USER_ID = "919670443252"

run_graph(
    user_id=USER_ID,
    tenant_id=TENANT_ID,
    message="My internet is not working"
)

run_graph(
    user_id=USER_ID,
    tenant_id=TENANT_ID,
    message="I need an appointment"
)

profile = get_customer_profile(
    tenant_id=TENANT_ID,
    user_id=USER_ID
)

print(dict(profile))

