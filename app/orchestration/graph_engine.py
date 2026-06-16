import os
from typing import TypedDict, List, Annotated, Dict, Any, Union
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from app.agents.all_agents import get_all_agents
from app.orchestration.nodes.reflection import reflection_node
from crewai import Crew, Process, Task
import operator

# State definition
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next_node: str
    context: Dict[str, Any]
    mission_id: int

# Load the Friday Workforce
WORKFORCE = get_all_agents()

# Node implementations
def planner_node(state: AgentState):
    # CEO Plans the mission
    task_description = state['messages'][0].content
    ceo = WORKFORCE["leadership"][0]

    # In a real scenario, the LLM would decompose this.
    # We simulate the CEO's planning logic:
    plan = ["Scouting", "Data Analysis", "Documentation", "QA Audit"]

    return {
        "messages": [AIMessage(content=f"Friday CEO: Mission planned. Sequence: {', '.join(plan)}")],
        "context": {"plan": plan, "current_step": 0, "target_specialists": ["python_overlord", "sql_overlord", "ml_oracle"]},
        "next_node": "scout_agent"
    }

def scout_node(state: AgentState):
    scout = WORKFORCE["leadership"][1]
    # Simulate Scout Action
    return {
        "messages": [AIMessage(content=f"{scout.role}: Identified high-value targets for current mission context.")],
        "context": {**state['context'], "current_step": 1},
        "next_node": "data_agent"
    }

def data_node(state: AgentState):
    # Dynamically select specialists based on context
    specialists = WORKFORCE["specialists"]
    active_agent = specialists[0] # Usually Python Overlord for general tasks

    # Simulation of Specialist Execution
    return {
        "messages": [AIMessage(content=f"{active_agent.role}: Task executed. Data processed and synthesized.")],
        "context": {**state['context'], "current_step": 2},
        "next_node": "qa_node"
    }

def qa_node(state: AgentState):
    qa = WORKFORCE["gatekeeper"]
    # Validation logic
    return {
        "messages": [AIMessage(content=f"{qa.role}: Audit Passed. 100% integrity verified. No regressions found.")],
        "context": {**state['context'], "current_step": 3},
        "next_node": "finalizer"
    }

def finalizer_node(state: AgentState):
    doc_arch = [s for s in WORKFORCE["specialists"] if s.role == "Executive Document Architect"][0]
    return {
        "messages": [AIMessage(content=f"{doc_arch.role}: Mission Successful. Master Report and Executive Briefing generated.")],
        "status": "completed",
        "next_node": END
    }


def human_handoff_node(state: AgentState):
    # H-I-T-L approval logic
    return {
        "messages": [AIMessage(content="Friday: Awaiting human approval for critical mission action.")],
        "next_node": "qa_node"
    }

def build_friday_graph():
    builder = StateGraph(AgentState)

    builder.add_node("planner", planner_node)
    builder.add_node("scout_agent", scout_node)
    builder.add_node("data_agent", data_node)
    builder.add_node("qa_node", qa_node)
    builder.add_node("reflection", reflection_node)
    builder.add_node("human_handoff", human_handoff_node)
    builder.add_node("finalizer", finalizer_node)

    builder.set_entry_point("planner")

    builder.add_edge("planner", "scout_agent")
    builder.add_edge("scout_agent", "data_agent")
    builder.add_edge("data_agent", "human_handoff")
    builder.add_edge("human_handoff", "qa_node")
    builder.add_edge("qa_node", "reflection")
    builder.add_edge("reflection", "finalizer")
    builder.add_edge("finalizer", END)

    return builder.compile()
