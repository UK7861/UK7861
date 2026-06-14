from fastapi import FastAPI
from pydantic import BaseModel
import time
from typing import List, Dict

app = FastAPI(title="Friday Data Core API")

# In-memory state store
system_state = {
    "status": "OPERATIONAL",
    "mission_count": 42,
    "agents_online": 13,
    "last_update": time.time(),
    "logs": [
        {"timestamp": time.time(), "message": "System Booted.", "level": "INFO"},
        {"timestamp": time.time() + 1, "message": "All agents STANDBY.", "level": "INFO"}
    ],
    "agent_vitals": {
        "Friday CEO": {"status": "STANDBY", "progress": 0},
        "QA Agent": {"status": "STANDBY", "progress": 0, "alerts": 0},
        "Data Engineer": {"status": "STANDBY", "progress": 0},
        # ... more agents can be added here
    }
}

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
    return {"status": "Agent updated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
