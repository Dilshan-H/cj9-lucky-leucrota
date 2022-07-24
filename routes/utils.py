from fastapi import WebSocket
from typing import List


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, client_name: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

        for connection in self.active_connections:
            if connection != websocket:
                await connection.send_text(f"{client_name} join the chat room.")

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def broadcast(
        self,
        client_name: str,
        websocket: WebSocket,
        message: str = "",
        disconnected: bool = False,
    ) -> None:
        if disconnected:
            for connection in self.active_connections:
                if connection != websocket:
                    await connection.send_text(f"{client_name} left the chat room.")

        else:
            for connection in self.active_connections:
                if connection != websocket:
                    await connection.send_text(f"{client_name}: {message}")
                else:
                    await connection.send_text(f"You: {message}")
