from fastapi import APIRouter, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

router = APIRouter()

templates = Jinja2Templates(directory="src/templates")


@router.get("/")
async def index(request: Request):
    """Index Route"""
    return templates.TemplateResponse("index.html", {"request": request})

websocket_list = []

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Web-Socket Route"""
    await websocket.accept()

    if websocket not in websocket_list:
        websocket_list.append(websocket)

    while True:
        content = await websocket.receive_text()
        
        for ws in websocket_list:
            await ws.send_text(content)

@router.websocket_route("/ws/test")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()
