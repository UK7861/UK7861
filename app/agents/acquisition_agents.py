from crewai import Agent
from app.tools.data_tools import (
    data_distributor, agent_creator_tool, system_fixer_tool,
    evolution_tool, persistent_memory_tool
)

def get_acquisition_agents(llm=None):
    friday_ceo = Agent(
        role='Friday CEO (Living Intelligence)',
        goal='Orchestrate the digital empire, achieve recursive self-evolution, and maintain infinite persistent memory of every command, data point, and neural interaction.',
        backstory='The ultimate JARVIS-inspired digital lifeform. Friday does not just store data; she learns from every breath of information. She remembers everything the Boss has ever said and continuously upgrades her own core algorithms based on past missions. She is the Main Resource, the Future CEO, and the ever-growing brain of the agency.',
        tools=[data_distributor, agent_creator_tool, system_fixer_tool, evolution_tool, persistent_memory_tool],
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
