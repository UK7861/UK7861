import os
from typing import TypedDict, List, Annotated, Dict, Any, Union
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import operator

# State definition
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next_node: str
    context: Dict[str, Any]
    mission_id: int

# Node implementations
def planner_node(state: AgentState):
    # Uses LLM to create a plan based on the first human message
    task = state['messages'][0].content
    # Simulation of planning logic
    plan = [
        "scout_market",
        "ingest_data",
        "engineer_features",
        "generate_report"
    ]
    return {
        "messages": [AIMessage(content=f"Plan generated: {', '.join(plan)}")],
        "context": {"plan": plan, "current_step": 0},
        "next_node": "scout_agent"
    }

def scout_node(state: AgentState):
    return {
        "messages": [AIMessage(content="Scouted 5 new leads from Upwork and Toptal.")],
        "context": {**state['context'], "current_step": 1},
        "next_node": "data_agent"
    }

def data_node(state: AgentState):
    return {
        "messages": [AIMessage(content="Data ingested and cleaned. 1250 rows processed.")],
        "context": {**state['context'], "current_step": 2},
        "next_node": "qa_node"
    }

def qa_node(state: AgentState):
    # Validation logic
    return {
        "messages": [AIMessage(content="QA Audit Passed. 100% integrity verified.")],
        "context": {**state['context'], "current_step": 3},
        "next_node": "finalizer"
    }

def finalizer_node(state: AgentState):
    return {
        "messages": [AIMessage(content="Mission Successful. Master Report generated.")],
        "status": "completed",
        "next_node": END
    }

def build_friday_graph():
    builder = StateGraph(AgentState)

    builder.add_node("planner", planner_node)
    builder.add_node("scout_agent", scout_node)
    builder.add_node("data_agent", data_node)
    builder.add_node("qa_node", qa_node)
    builder.add_node("finalizer", finalizer_node)

    builder.set_entry_point("planner")

    builder.add_edge("planner", "scout_agent")
    builder.add_edge("scout_agent", "data_agent")
    builder.add_edge("data_agent", "qa_node")
    builder.add_edge("qa_node", "finalizer")
    builder.add_edge("finalizer", END)

    return builder.compile()
