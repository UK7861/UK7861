from crewai import Crew, Task
from app.agents.data_agents import get_data_agents
from app.agents.acquisition_agents import get_acquisition_agents
from app.agents.client_agent import get_client_agent
from app.tools.mock_llm import MockLLM
from app.tools.data_tools import report_synthesizer
import os

def run_agency_mission(client_requirements):
    # Initialize Mock LLM
    mock_llm = MockLLM()

    # Get Agents
    ceo, scout = get_acquisition_agents(llm=mock_llm)
    data_team, qa_agent = get_data_agents(llm=mock_llm)
    client_liaison = get_client_agent(llm=mock_llm)

    # Define Tasks
    onboarding_task = Task(
        description=f"Onboard client with requirements: {client_requirements}",
        agent=client_liaison,
        expected_output="Detailed client requirement document."
    )

    scouting_task = Task(
        description="Scout for similar high-value projects on freelance platforms.",
        agent=scout,
        expected_output="List of 5 potential leads and proposal templates."
    )

    distribution_task = Task(
        description="Analyze requirements and distribute tasks to the data team.",
        agent=ceo,
        expected_output="Task allocation plan for 10 data agents."
    )

    data_processing_tasks = [
        Task(
            description=f"Perform {agent.role} specific tasks for the project.",
            agent=agent,
            expected_output=f"Output from {agent.role}."
        ) for agent in data_team
    ]

    qa_task = Task(
        description="Audit all outputs from the data team and fix any discrepancies.",
        agent=qa_agent,
        expected_output="Verified and finalized data modules."
    )

    synthesis_task = Task(
        description="Synthesize all verified modules into a final report.",
        agent=ceo,
        tools=[report_synthesizer],
        expected_output="Final mission report in Markdown format."
    )

    # Create Crew
    friday_crew = Crew(
        agents=[client_liaison, scout, ceo] + data_team + [qa_agent],
        tasks=[onboarding_task, scouting_task, distribution_task] + data_processing_tasks + [qa_task, synthesis_task],
        verbose=True
    )

    # Execute Mission
    result = friday_crew.kickoff()
    return result

if __name__ == "__main__":
    mission_result = run_agency_mission("Develop an automated data cleaning and BI dashboard for a retail client.")
    print("\n\n########################")
    print("## MISSION ACCOMPLISHED ##")
    print("########################\n")
    print(mission_result)
