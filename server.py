from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

@app.get('/')
async def home_page():
    return HTMLResponse(os.path.join("static", "home-page.html"))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        print(data)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("__main__:app",
                host="localhost",
                port=8000,
                reload=True)