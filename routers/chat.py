from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from core.websocket_manager import ConnectionManager
from services.jwt import verify_jwt

manager = ConnectionManager()
app = APIRouter()

@app.websocket("/ws/chat")
async def chat_ws(websocket: WebSocket, token: str = Query(...)):
    user_id = verify_jwt(token)
    if not user_id:
        await websocket.close(code=1000)
        return
    
    await manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast({
                "sender": user_id,
                "text": data["text"]
            })
    except:
        manager.disconnect(user_id)