from fastapi import WebSocket

class ConnectionManager:
    
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}


    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket


    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)

    async def send_personal(self, user_id: str, message: dict):
        ws = self.active_connections.get(user_id)
        if ws:
            await ws.send_json(message)

    async def broadcast(self, message: dict):
        for ws in self.active_connections.values():
            await ws.send_json(message)