from fastapi import WebSocket


class TenantConnectionManager:
    def __init__(self):
        # {tenant_id: [WebSocket, WebSocket, ...]}
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(
        self,
        tenant_id: int,
        websocket: WebSocket
    ):
        await websocket.accept()

        if tenant_id not in self.active_connections:
            self.active_connections[tenant_id] = []

        self.active_connections[tenant_id].append(websocket)

    def disconnect(
        self,
        tenant_id: int,
        websocket: WebSocket
    ):
        connections = self.active_connections.get(
            tenant_id,
            []
        )

        if websocket in connections:
            connections.remove(websocket)

        if not connections and tenant_id in self.active_connections:
            del self.active_connections[tenant_id]

    async def send_to_tenant(
        self,
        tenant_id: int,
        message: dict
    ):
        connections = self.active_connections.get(
            tenant_id,
            []
        )

        disconnected_connections = []

        for websocket in connections:
            try:
                await websocket.send_json(message)
            except Exception:
                disconnected_connections.append(websocket)

        for websocket in disconnected_connections:
            self.disconnect(tenant_id, websocket)


manager = TenantConnectionManager()



