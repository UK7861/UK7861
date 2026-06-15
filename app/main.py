from crewai import Crew, Task, Agent
from app.tools.mock_llm import MockLLM
from app.tools.data_tools import (
    report_synthesizer, agent_creator_tool, system_fixer_tool,
    evolution_tool, live_data_stream_tool, document_generation_tool,
    data_cleaning_tool, bi_automation_tool, sql_query_master_tool
)
import requests
import time
import random

API_URL = "http://localhost:8000"

class FridayThinkingEngine:
    def __init__(self):
        self.llm = MockLLM()
        self.core_memory = []

    def interpret_and_execute(self, user_intent: str):
        print(f"FRIDAY CORE: Analyzing intent - '{user_intent}'")
        requests.post(f"{API_URL}/intel_upgrade")

        # 1. Dynamic Task Decomposition (Simulated LLM call)
        # Instead of hardcoding, we simulate fetching the required personas for the intent
        available_tool_map = {
            "Data Engineer": [data_cleaning_tool, sql_query_master_tool],
            "BI Architect": [bi_automation_tool],
            "Executive Document Architect": [document_generation_tool],
            "Strategic Analyst": []
        }

        # Simulated decomposition based on keywords
        required_roles = ["Strategic Analyst"]
        if "data" in user_intent.lower() or "sql" in user_intent.lower(): required_roles.append("Data Engineer")
        if "dashboard" in user_intent.lower() or "bi" in user_intent.lower(): required_roles.append("BI Architect")
        # Trigger Document Architect for reports, invoices, or bills
        if any(kw in user_intent.lower() for kw in ["report", "strategy", "invoice", "bill"]):
            required_roles.append("Executive Document Architect")

        dynamic_agents = []
        crew_tasks = []

        for role in required_roles:
            # 2. Dynamic Agent Synthesis
            agent_id_resp = requests.post(f"{API_URL}/command", json={"command": f"Synthesize {role}"}).json()

            agent = Agent(
                role=role,
                goal=f"Execute {role} operations for: {user_intent}",
                backstory=f"A specialized humanoid intelligence unit synthesized by FRIDAY for {role}.",
                tools=available_tool_map.get(role, []),
                llm=self.llm,
                verbose=True,
                allow_delegation=False
            )
            dynamic_agents.append(agent)

            task = Task(
                description=f"Perform {role} analysis on: {user_intent}",
                agent=agent,
                expected_output=f"Finalized {role} output for the mission."
            )
            crew_tasks.append(task)

        # 3. Autonomous Orchestration
        friday_crew = Crew(
            agents=dynamic_agents,
            tasks=crew_tasks,
            verbose=True,
            process="hierarchical", # FRIDAY manages the workflow
            manager_llm=self.llm
        )

        print("FRIDAY OS: Orchestrating dynamic intelligence...")
        result = friday_crew.kickoff()

        # 4. Evolution & Logging
        requests.post(f"{API_URL}/mission_result", json={
            "intent": user_intent,
            "result": str(result),
            "agents": [a.role for a in dynamic_agents]
        })
        requests.post(f"{API_URL}/upgrade_core")
        return result

def run_agency_mission(intent):
    engine = FridayThinkingEngine()
    return engine.interpret_and_execute(intent)

if __name__ == "__main__":
    run_agency_mission("Synthesize a market entry strategy for autonomous AI agencies in Pakistan.")
