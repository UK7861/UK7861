from fastapi import FastAPI
from pydantic import BaseModel
import time
from typing import List, Dict

app = FastAPI(title="Friday Data Core API")

# Initialize all 13 agents in state
agents = [
    "Friday CEO", "QA Agent", "Platform Scout", "AI Voice Data Agent",
    "Data Engineer", "Data Scientist", "Analytics Expert", "Big Data Architect",
    "Small Data Specialist", "Deep Tajziya Analyst", "MLOps Engineer",
    "Data Privacy Officer", "Database Administrator", "BI Developer"
]

system_state = {
    "status": "OPERATIONAL",
    "mission_count": 42,
    "agents_online": len(agents),
    "last_update": time.time(),
    "logs": [
        {"timestamp": time.time(), "message": "System Booted. JARVIS-Core Initialized.", "level": "INFO"},
        {"timestamp": time.time() + 1, "message": "All 14 specialized units standing by.", "level": "INFO"}
    ],
    "agent_vitals": {name: {"status": "STANDBY", "progress": 0} for name in agents}
}

# QA Agent gets special alert counter for self-healing
system_state["agent_vitals"]["QA Agent"]["alerts"] = 0

class LogEntry(BaseModel):
    message: str
    level: str = "INFO"

@app.get("/state")
def get_state():
    system_state["last_update"] = time.time()
    return system_state

@app.post("/log")
def add_log(entry: LogEntry):
    log = {"timestamp": time.time(), "message": entry.message, "level": entry.level}
    system_state["logs"].append(log)
    if len(system_state["logs"]) > 50:
        system_state["logs"].pop(0)
    return {"status": "Log added"}

@app.post("/update_agent")
def update_agent(name: str, status: str, progress: int):
    if name in system_state["agent_vitals"]:
        system_state["agent_vitals"][name]["status"] = status
        system_state["agent_vitals"][name]["progress"] = progress
    else:
        system_state["agent_vitals"][name] = {"status": status, "progress": progress}

    # Increment mission count if a mission completed message is logged
    return {"status": "Agent updated"}

@app.post("/increment_missions")
def increment_missions():
    system_state["mission_count"] += 1
    return {"status": "Mission count incremented"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
