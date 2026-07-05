from services.customer_service import save_or_update_customer
from graph.workflow import run_graph


def route_tenant_message(
    tenant_id,
    user_id,
    username,
    message
):
    save_or_update_customer(
        tenant_id=tenant_id,
        user_id=user_id,
        username=username,
        phone=user_id
    )

    result = run_graph(
        tenant_id=tenant_id,
        user_id=user_id,
        message=message
    )

    if isinstance(result, dict):
        return result.get(
            "response",
            "Your request has been received."
        )

    return str(result)




