from fastapi import APIRouter, WebSocket, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="src/templates")


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

websocket_list = []
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    if websocket not in websocket_list:
        websocket_list.append(websocket)

    while True:
        content = await websocket.receive_text()
        
        for ws in websocket_list:
            await ws.send_text(content)
