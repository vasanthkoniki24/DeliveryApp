from fastapi import WebSocket
from typing import Dict, List


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, order_id: int, websocket: WebSocket):
        await websocket.accept()

        if order_id not in self.active_connections:
            self.active_connections[order_id] = []

        self.active_connections[order_id].append(websocket)

    def disconnect(self, order_id: int, websocket: WebSocket):
        self.active_connections[order_id].remove(websocket)

    async def send_update(self, order_id: int, message: dict):
        if order_id in self.active_connections:
            for connection in self.active_connections[order_id]:
                await connection.send_json(message)


manager = ConnectionManager()