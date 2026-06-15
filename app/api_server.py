from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from app.db.postgres import init_db, get_session
from app.core.ws_manager import ws_manager
from app.core.logging_config import setup_logging, logger
from app.models.persistence import User, Mission
import time

app = FastAPI(title="FRIDAY OS - Production Core")
setup_logging()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()
    logger.info("FRIDAY OS Started", status="ONLINE")

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.websocket("/ws/hud")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming WS messages if needed
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

# API Routes for Missions, Auth, etc. will go here
