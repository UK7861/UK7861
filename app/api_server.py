from fastapi import FastAPI
from pydantic import BaseModel
import time
from typing import List, Dict

app = FastAPI(title="Friday Data Core API")

# Updated Roster for JARVIS-Core v4.0
agents = [
    "Friday CEO", "QA Agent", "JARVIS Scout & Liaison", "Live Data Collector",
    "Python Overlord", "Excel Master", "Humanoid Report Generator",
    "Machine Learning Oracle", "Deep Learning Strategist", "Analytics Expert"
]

system_state = {
    "status": "OPERATIONAL",
    "mission_count": 42,
    "intelligence_level": 150,
    "core_version": "4.0.0-HUMAN",
    "agents_online": len(agents),
    "last_update": time.time(),
    "logs": [
        {"timestamp": time.time(), "message": "System Booted. Humanoid Intelligence Engine active.", "level": "INFO"}
    ],
    "agent_vitals": {name: {"status": "STANDBY", "progress": 0} for name in agents}
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

@app.post("/upgrade_core")
def upgrade_core():
    system_state["intelligence_level"] += 10
    major, minor, patch = system_state["core_version"].split("-")[0].split(".")
    patch = str(int(patch) + 1)
    system_state["core_version"] = f"{major}.{minor}.{patch}-HUMAN"
    return {"status": "Core evolved", "new_level": system_state["intelligence_level"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
