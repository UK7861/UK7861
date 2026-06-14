from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import random
from typing import List, Dict, Any, Optional

app = FastAPI(title="FRIDAY OS Intelligence Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# The Intelligence Registry - Everything is dynamic
class StateManager:
    def __init__(self):
        self.start_time = time.time()
        self.core = {
            "name": "FRIDAY",
            "version": "OS-1.0-ALIVE",
            "intel_level": 1000,
            "status": "CONSCIOUS",
            "pulse_rate": 60,
            "memory_nodes": 4096
        }
        self.approval_pending = False
        self.pending_action = ""
        self.agents = {} # Dynamically populated
        self.missions = []
        self.data_vault = []
        self.knowledge_graph = {
            "nodes": [{"id": "FRIDAY", "type": "CORE", "val": 100}],
            "links": []
        }
        self.logs = []
        self.stats = {
            "tasks_completed": 0,
            "active_workflows": 0,
            "reports_generated": 0,
            "models_trained": 0
        }

    def add_log(self, message: str, level: str = "INFO"):
        self.logs.append({
            "timestamp": time.time(),
            "message": message,
            "level": level
        })
        if len(self.logs) > 100: self.logs.pop(0)

    def spawn_agent(self, role: str, goal: str):
        agent_id = f"AGENT_{random.randint(1000, 9999)}"
        self.agents[agent_id] = {
            "id": agent_id,
            "role": role,
            "goal": goal,
            "status": "INITIALIZING",
            "progress": 0,
            "health": 100,
            "load": 0,
            "spawn_time": time.time()
        }
        self.knowledge_graph["nodes"].append({"id": agent_id, "type": "AGENT", "val": 20})
        self.knowledge_graph["links"].append({"source": "FRIDAY", "target": agent_id})
        self.add_log(f"FRIDAY: Synthesized new intelligence unit: {role} ({agent_id})", "WARNING")
        return agent_id

state = StateManager()

class CommandRequest(BaseModel):
    command: str

@app.get("/state")
def get_global_state():
    return {
        "core": state.core,
        "status": state.core["status"],
        "mission_count": len(state.missions),
        "intelligence_level": state.core["intel_level"],
        "core_version": state.core["version"],
        "approval_pending": state.approval_pending,
        "pending_action": state.pending_action,
        "agents": list(state.agents.values()),
        "agent_vitals": {v["role"]: v for v in state.agents.values()},
        "knowledge_graph": state.knowledge_graph,
        "stats": state.stats,
        "logs": state.logs,
        "uptime": time.time() - state.start_time,
        "vault_count": len(state.data_vault)
    }

@app.post("/command")
def process_command(req: CommandRequest):
    # This will be handled by the Friday Thinking Engine (main.py)
    state.add_log(f"BOSS COMMAND RECEIVED: {req.command}", "INFO")
    return {"status": "ACCEPTED", "message": "FRIDAY is processing intent..."}

@app.get("/briefing")
def get_executive_briefing():
    return {
        "greeting": "Greetings, OWNER",
        "summary": f"FRIDAY OS is operating at peak consciousness. {state.stats['tasks_completed']} neural tasks completed today.",
        "metrics": state.stats,
        "recommendations": [
            "Optimize neural pathway for current data stream",
            "Expand workforce for pending multi-agent workflow"
        ]
    }

@app.post("/update_agent")
def update_agent(name: str, status: str, progress: int):
    # Match by role name if id not provided (for scout service)
    found = False
    for agent_id, agent_data in state.agents.items():
        if agent_data["role"] == name:
            agent_data["status"] = status
            agent_data["progress"] = progress
            agent_data["load"] = random.randint(10, 90) if status == "WORKING" else 0
            found = True
            break

    if not found:
        # Spawn if not found
        state.spawn_agent(name, "Background service task")

    return {"status": "UPDATED"}

@app.post("/approve")
def approve_action():
    state.approval_pending = False
    state.add_log(f"BOSS APPROVED ACTION: {state.pending_action}", "SUCCESS")
    state.pending_action = ""
    return {"status": "APPROVED"}

@app.post("/mission_result")
def mission_result(data: Dict[str, Any]):
    state.stats["tasks_completed"] += 1
    state.add_log(f"MISSION SUCCESS: {data.get('intent', 'Task complete')}", "SUCCESS")
    state.missions.append(data)
    return {"status": "RECORDED"}

@app.post("/log")
def add_log_entry(req: Dict[str, str]):
    state.add_log(req.get("message", ""), req.get("level", "INFO"))
    return {"status": "LOGGED"}

@app.post("/intel_upgrade")
def upgrade_intel():
    state.core["intel_level"] += 1
    return {"level": state.core["intel_level"]}

@app.post("/upgrade_core")
def upgrade_core():
    v_parts = state.core["version"].split("-")[0].split(".")
    # Increment minor version
    new_v = f"{v_parts[0]}.{int(v_parts[1])}.{int(v_parts[2]) + 1}"
    state.core["version"] = f"{new_v}-ALIVE"
    state.add_log(f"FRIDAY CORE EVOLVED: New Version {state.core['version']}", "SUCCESS")
    return {"version": state.core["version"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
