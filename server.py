from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import os

class ConnectionManager:
    def __init__(self):
        self.current_connections: list[WebSocket] = []

    async def add_user(self, websocket: WebSocket):
        await websocket.accept()
        self.current_connections.append(websocket)

    def remove_user(self, websocket: WebSocket):
        self.current_connections.remove(websocket)

    async def broadcast_message(self, message):
        for connection in self.current_connections:
            await connection.send_text(message)

app = FastAPI()
connection_manager = ConnectionManager()

@app.get("/")
async def main_page():
    with open(os.path.join("static", "canvas_page.html")) as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.add_user(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            mouseX, mouseY = data.split(',')
            await connection_manager.broadcast_message(f"{mouseX},{mouseY}")

    except WebSocketDisconnect:
        await connection_manager.broadcast_message("User has disconnected")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("__main__:app",
                host="localhost",
                port=8000,
                reload=True)