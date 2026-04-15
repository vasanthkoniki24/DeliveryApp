from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.ws_manager import manager

router = APIRouter()

@router.websocket("/ws/orders/{order_id}")
async def order_ws(websocket: WebSocket, order_id: int):
    await manager.connect(order_id, websocket)

    try:
        while True:
            await websocket.receive_text()  # keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(order_id, websocket)