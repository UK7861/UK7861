from crewai import Agent
from app.tools.data_tools import data_distributor

def get_acquisition_agents(llm=None):
    friday_ceo = Agent(
        role='Friday CEO',
        goal='Orchestrate the agency and manage client requirements',
        backstory='The central brain of Friday Data Agency. Strategic, decisive, and efficient.',
        tools=[data_distributor],
        llm=llm,
        verbose=True
    )

    platform_scout = Agent(
        role='Platform Scout',
        goal='Crawl freelance platforms for high-value data projects',
        backstory='Expert in navigating Upwork, Freelancer, and Fiverr to find leads.',
        llm=llm,
        verbose=True
    )

    return friday_ceo, platform_scout
