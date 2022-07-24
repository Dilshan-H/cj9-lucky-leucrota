from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from routes import chat

app = FastAPI()

app.include_router(chat.router)
