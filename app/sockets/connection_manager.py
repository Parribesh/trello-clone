from typing import List, Dict
from fastapi import WebSocket, WebSocketDisconnect
from collections import defaultdict

class ConnectionManager:
    def __init__(self):
        # Dictionary to hold WebSocket connections by topic (e.g., board_id)
        self.active_connections: Dict[str, List[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, board_id: str):
        """Add a WebSocket connection to a specific board."""
        await websocket.accept()
        self.active_connections[board_id].append(websocket)
        print(f"User connected to board {board_id}")

    def disconnect(self, websocket: WebSocket, board_id: str):
        """Remove a WebSocket connection from a specific board."""
        self.active_connections[board_id].remove(websocket)
        print(f"User disconnected from board {board_id}")

    async def send_message(self, board_id: str, message: str):
        """Send a message to all connected WebSockets for a specific board."""
        for connection in self.active_connections[board_id]:
            await connection.send_text(message)

    async def broadcast(self, message: str):
        """Send a message to all connected WebSockets for all boards."""
        for connections in self.active_connections.values():
            for connection in connections:
                await connection.send_text(message)
    
    def get_connections(self, board_id: str) -> List[WebSocket]:
        """Get all WebSocket connections for a specific board."""
        return self.active_connections[board_id]

    def get_all_connections(self) -> Dict[str, List[WebSocket]]:
        """Get all WebSocket connections for all boards."""
        return self.active_connections
