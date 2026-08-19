from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/')
async def home_page():
    return

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"message received by user was {data}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,
                host="0.0.0.0",
                port=8000)