from crewai import Crew, Task
from app.agents.data_agents import get_data_agents
from app.agents.acquisition_agents import get_acquisition_agents
from app.agents.client_agent import get_client_agent
from app.tools.mock_llm import MockLLM
from app.tools.data_tools import (
    report_synthesizer, agent_creator_tool, system_fixer_tool,
    evolution_tool, live_data_stream_tool, document_generation_tool
)
import os

def run_agency_mission(client_requirements):
    # Initialize Mock JARVIS LLM
    mock_llm = MockLLM()

    # Get Agents
    ceo, scout = get_acquisition_agents(llm=mock_llm)
    data_team, qa_agent = get_data_agents(llm=mock_llm)
    live_collector = get_client_agent(llm=mock_llm)

    # 1. Hunting & Onboarding
    hunting_task = Task(
        description="Hunt for high-value data jobs and onboard the client using human-like communication.",
        agent=scout,
        expected_output="Onboarded client with initial project brief."
    )

    # 2. Live Data Collection
    collection_task = Task(
        description=f"Collect live data and requirements as the client speaks: {client_requirements}. Sync to Live Server.",
        agent=live_collector,
        tools=[live_data_stream_tool],
        expected_output="Live data stream synced to Friday Live Server."
    )

    # 3. Task Distribution & Workforce Expansion
    distribution_task = Task(
        description="Analyze requirements. Delegate Python tasks to Python Overlord, Excel tasks to Excel Master, and ML/DL tasks to their respective Oracles.",
        agent=ceo,
        tools=[agent_creator_tool],
        expected_output="Task distribution and workforce expansion report."
    )

    # 4. specialized execution
    execution_tasks = [
        Task(
            description=f"Execute {agent.role} specific tasks at humanoid-perfection level.",
            agent=agent,
            expected_output=f"Perfect output from {agent.role}."
        ) for agent in data_team
    ]

    # 5. Human-like Report Generation
    report_task = Task(
        description="Generate the final mission reports (PDF/Word/Excel) with human-like writing and deep insights.",
        agent=ceo, # CEO oversees final human-like touch
        tools=[document_generation_tool, report_synthesizer],
        expected_output="Final Humanoid Report Suite."
    )

    # 6. Self-Evolution
    evolution_task = Task(
        description="Analyze the mission results and perform a system-wide upgrade.",
        agent=ceo,
        tools=[evolution_tool],
        expected_output="System Evolution Report."
    )

    # Create Crew
    friday_crew = Crew(
        agents=[scout, live_collector, ceo] + data_team + [qa_agent],
        tasks=[hunting_task, collection_task, distribution_task] + execution_tasks + [report_task, evolution_task],
        verbose=True
    )

    # Execute Mission
    result = friday_crew.kickoff()
    return result

if __name__ == "__main__":
    mission_result = run_agency_mission("Retail client needs predictive sales analysis and automated monthly reports.")
    print("\n\n########################")
    print("## MISSION ACCOMPLISHED ##")
    print("########################\n")
    print(mission_result)
