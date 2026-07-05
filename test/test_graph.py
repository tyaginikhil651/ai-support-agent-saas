from graph.workflow import run_graph


result = run_graph(
    user_id="919999999999",
    tenant_id=1,
    message="My internet is not working"
)

print(result)