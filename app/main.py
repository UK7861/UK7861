from crewai import Crew, Task
from app.agents.data_agents import get_data_agents
from app.agents.acquisition_agents import get_acquisition_agents
from app.agents.client_agent import get_client_agent
from app.tools.mock_llm import MockLLM
from app.tools.data_tools import report_synthesizer, agent_creator_tool, system_fixer_tool
import os

def run_agency_mission(client_requirements):
    # Initialize Mock JARVIS LLM
    mock_llm = MockLLM()

    # Get Agents
    ceo, scout = get_acquisition_agents(llm=mock_llm)
    data_team, qa_agent = get_data_agents(llm=mock_llm)
    client_liaison = get_client_agent(llm=mock_llm)

    # Define Tasks
    onboarding_task = Task(
        description=f"Onboard client with requirements: {client_requirements}. Handle interaction in English or Roman Urdu as needed.",
        agent=client_liaison,
        expected_output="Detailed client requirement document and initial feedback."
    )

    scouting_task = Task(
        description="Scout for similar high-value projects on freelance platforms globally.",
        agent=scout,
        expected_output="Lead report and automated proposals."
    )

    # Autonomous Team Expansion Task
    expansion_task = Task(
        description="Evaluate requirements. If a new specialized unit is needed, use the agent_creator_tool to deploy it.",
        agent=ceo,
        tools=[agent_creator_tool],
        expected_output="Workforce expansion status report."
    )

    distribution_task = Task(
        description="Analyze requirements and distribute tasks to the data team (One-Man Armies).",
        agent=ceo,
        expected_output="Mission allocation plan."
    )

    data_processing_tasks = [
        Task(
            description=f"Execute {agent.role} specific tasks at peak performance.",
            agent=agent,
            expected_output=f"Validated module from {agent.role}."
        ) for agent in data_team
    ]

    # Self-Healing / QA Task
    qa_task = Task(
        description="Audit all outputs. Use system_fixer_tool to resolve any agent anomalies or data errors.",
        agent=qa_agent,
        tools=[system_fixer_tool],
        expected_output="Pristine, verified mission data modules."
    )

    synthesis_task = Task(
        description="Synthesize all verified modules into a final report. Communicate completion JARVIS-style.",
        agent=ceo,
        tools=[report_synthesizer],
        expected_output="Final mission report in Markdown format."
    )

    # Create Crew with Advanced Orchestration
    friday_crew = Crew(
        agents=[client_liaison, scout, ceo] + data_team + [qa_agent],
        tasks=[onboarding_task, scouting_task, expansion_task, distribution_task] + data_processing_tasks + [qa_task, synthesis_task],
        verbose=True,
        process="sequential" # Can be switched to hierarchical for more JARVIS-like behavior
    )

    # Execute Mission
    result = friday_crew.kickoff()
    return result

if __name__ == "__main__":
    mission_result = run_agency_mission("Create an autonomous agent team for deep-web data mining and BI visualization.")
    print("\n\n########################")
    print("## MISSION ACCOMPLISHED ##")
    print("########################\n")
    print(mission_result)
