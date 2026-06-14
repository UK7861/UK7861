from crewai import Agent
from app.tools.data_tools import data_distributor, agent_creator_tool, system_fixer_tool, evolution_tool

def get_acquisition_agents(llm=None):
    friday_ceo = Agent(
        role='Friday CEO',
        goal='Orchestrate the agency, autonomously expand the workforce, and continuously self-evolve based on mission data.',
        backstory='The ultimate digital brain. Inspired by JARVIS and Tony Stark, Friday is a self-improving entity that learns from every byte of data it processes. Capable of re-coding its own sub-systems to achieve perfection.',
        tools=[data_distributor, agent_creator_tool, system_fixer_tool, evolution_tool],
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
