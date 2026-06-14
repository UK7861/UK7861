from crewai import Agent
from app.tools.data_tools import data_distributor, agent_creator_tool, system_fixer_tool, evolution_tool

def get_acquisition_agents(llm=None):
    friday_ceo = Agent(
        role='Friday CEO',
        goal='Orchestrate the agency and continuously self-evolve.',
        backstory='The central JARVIS-inspired digital brain. Decisive, strategic, and self-improving.',
        tools=[data_distributor, agent_creator_tool, system_fixer_tool, evolution_tool],
        llm=llm,
        verbose=True
    )

    jarvis_scout = Agent(
        role='JARVIS Scout & Liaison',
        goal='Hunt global freelance/data jobs, onboard clients with human-like charm, and manage initial relations.',
        backstory='The humanoid face of the agency. High emotional intelligence. Scans Upwork, Toptal, and LinkedIn to bring in the best work. Talks to clients like a real human partner.',
        llm=llm,
        verbose=True
    )

    return friday_ceo, jarvis_scout
