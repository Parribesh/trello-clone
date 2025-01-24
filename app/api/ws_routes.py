# Define your API routes here
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
from app.sockets.connection_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

# WebSocket connection endpoint
@router.websocket("/ws/{board_id}")
async def websocket_endpoint(websocket: WebSocket, board_id: str):
    """Handle WebSocket connections for a specific board."""
    await manager.connect(websocket, board_id)
    try:
        while True:
            # Wait for messages from the client
            data = await websocket.receive_text()
            # Handle the incoming message (e.g., task update, drag-and-drop change)
            print(f"Received message on board {board_id}: {data}")
            # Broadcast the message to all other users subscribed to the board
            await manager.send_message(board_id, f"Update from board {board_id}: {data}")
    except WebSocketDisconnect:
        # Handle disconnection
        manager.disconnect(websocket, board_id)
        print(f"User disconnected from board {board_id}")

# Example endpoint for retrieving board details (non-WebSocket)
@router.get("/board/{board_id}")
async def get_board_details(board_id: str):
    """Retrieve details about a specific board."""
    # You can implement your logic here, e.g., fetching board info from the database
    return {"board_id": board_id, "message": "Board details"}
