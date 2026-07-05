import asyncio

from live.manager import manager


def send_live_notification(
    tenant_id: int,
    event_type: str,
    title: str,
    message: str,
    data: dict | None = None
):
    payload = {
        "type": event_type,
        "title": title,
        "message": message,
        "data": data or {}
    }

    try:
        loop = asyncio.get_running_loop()

        loop.create_task(
            manager.send_to_tenant(
                tenant_id=tenant_id,
                message=payload
            )
        )

    except RuntimeError:
        # Called from a synchronous workflow / non-async context.
        # A running FastAPI event loop may not be available here.
        return








