from typing import TypedDict, List, Annotated, Dict, Any
from langgraph.graph import StateGraph, END
import operator

class AgentState(TypedDict):
    task: str
    plan: List[str]
    results: Annotated[List[str], operator.add]
    current_agent: str
    history: List[Dict[str, str]]
    status: str

def friday_orchestrator(state: AgentState):
    # Logic to decide next agent or finish
    if not state.get("plan"):
        return {"status": "planning"}
    if len(state["results"]) >= len(state["plan"]):
        return {"status": "finished"}
    return {"status": "executing"}

def build_friday_graph():
    workflow = StateGraph(AgentState)

    # Define Nodes (to be implemented in next step)
    # workflow.add_node("planner", planner_node)
    # workflow.add_node("executor", executor_node)
    # workflow.add_node("qa", qa_node)

    # workflow.set_entry_point("planner")
    # ...

    return workflow
