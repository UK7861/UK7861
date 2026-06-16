from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta
from typing import List

from app.db.postgres import init_db, get_session, engine
from app.db.redis_bus import redis_cache
from app.memory.graph import graph_memory
from app.core.ws_manager import ws_manager
from app.core.logging_config import setup_logging, logger
from app.core.security import verify_password, get_password_hash, create_access_token, ALGORITHM, SECRET_KEY
from app.models.persistence import User, Mission, AgentState, SystemLog
from app.orchestration.graph_engine import build_friday_graph
from jose import JWTError, jwt

app = FastAPI(title="FRIDAY OS - Production Intelligence Core")
setup_logging()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- AUTHENTICATION ---
async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None: raise credentials_exception
    except JWTError: raise credentials_exception

    user = session.exec(select(User).where(User.username == username)).first()
    if user is None: raise credentials_exception
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/register")
def register_user(user: User, session: Session = Depends(get_session)):
    user.hashed_password = get_password_hash(user.hashed_password)
    session.add(user)
    session.commit()
    return {"status": "User created"}

# --- MISSION CONTROL ---
from app.main import run_production_mission
import asyncio

@app.post("/missions/execute")
async def execute_mission(intent: str, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    mission = Mission(intent=intent, user_id=user.id, status="working")
    session.add(mission)
    session.commit()
    session.refresh(mission)

    # Trigger LangGraph
    logger.info("Mission Started", mission_id=mission.id, intent=intent)
    # We use create_task to run it in background for the API response
    asyncio.create_task(run_production_mission(intent))

    return {"mission_id": mission.id, "status": "running"}

@app.get("/state")
async def get_system_state(session: Session = Depends(get_session)):
    agents = session.exec(select(AgentState)).all()
    logs = session.exec(select(SystemLog).order_by(SystemLog.timestamp.desc()).limit(20)).all()
    missions = session.exec(select(Mission).order_by(Mission.created_at.desc()).limit(10)).all()
    graph = graph_memory.get_graph()

    total_cost = sum(m.cost for m in missions if m.cost)

    return {
        "agents": agents,
        "logs": logs,
        "missions": missions,
        "total_cost": total_cost,
        "knowledge_graph": graph,
        "intel_level": redis_cache.get_state("intel_level") or 1000,
        "uptime": 3600 # Placeholder
    }

# --- REAL-TIME UPDATES ---
@app.websocket("/ws/hud")
async def hud_websocket(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            # Broadcast state every 2 seconds or on event
            data = await websocket.receive_text()
            # Echo or process commands
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

@app.on_event("startup")
def startup():
    init_db()

    # Seed Agents if table is empty
    from app.agents.all_agents import get_all_agents
    from app.db.postgres import Session

    with Session(engine) as session:
        existing = session.exec(select(AgentState)).first()
        if not existing:
            workforce = get_all_agents()
            for agent in workforce["all_list"]:
                state = AgentState(
                    id=agent.role.replace(" ", "_").lower(),
                    role=agent.role,
                    status="STANDBY",
                    progress=0,
                    energy=100.0,
                    stamina=100.0
                )
                session.add(state)
            session.commit()
            logger.info(f"Seeded {len(workforce['all_list'])} agents into state manager.")

    logger.info("FRIDAY Production OS Initialized")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
