from crewai import Agent
from app.tools.data_tools import data_distributor, agent_creator_tool, system_fixer_tool

def get_acquisition_agents(llm=None):
    friday_ceo = Agent(
        role='Friday CEO',
        goal='Orchestrate the agency, manage client requirements, and autonomously expand the workforce.',
        backstory='Inspired by JARVIS and Tony Stark. A super-intelligent entity capable of strategic expansion, real-time problem solving, and autonomous team building.',
        tools=[data_distributor, agent_creator_tool, system_fixer_tool],
        llm=llm,
        verbose=True,
        allow_delegation=True
    )

    platform_scout = Agent(
        role='Platform Scout',
        goal='Crawl freelance platforms and capture high-value data projects globally.',
        backstory='The global eyes and ears of Friday. Powerful scouting capabilities with automated proposal generation.',
        llm=llm,
        verbose=True
    )

    return friday_ceo, platform_scout
