from crewai import Agent
from app.tools.data_tools import data_cleaning_tool, bi_automation_tool, system_fixer_tool

def get_data_agents(llm=None):
    # Specialized 10 Core Data Agents (One-Man Armies)
    data_engineer = Agent(
        role='Data Engineer',
        goal='Build world-class data pipelines for any scale.',
        backstory='Master of data movement and transformation. Proficient in Big and Small data.',
        tools=[data_cleaning_tool],
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    data_scientist = Agent(
        role='Data Scientist',
        goal='Extract predictive insights from global datasets.',
        backstory='Deep learning and statistical powerhouse.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    analytics_expert = Agent(
        role='Analytics Expert',
        goal='Visualize complexity into clarity.',
        backstory='Master of data storytelling and BI automation.',
        tools=[bi_automation_tool],
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    big_data_architect = Agent(
        role='Big Data Architect',
        goal='Architect planet-scale data systems.',
        backstory='Expert in Hadoop, Spark, and massive cloud infrastructure.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    small_data_specialist = Agent(
        role='Small Data Specialist',
        goal='Precision analysis for targeted datasets.',
        backstory='Expert in extraction and processing of focused data assets.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    tajziya_analyst = Agent(
        role='Deep Tajziya Analyst',
        goal='Perform deep, culturally nuanced analysis.',
        backstory='Specialized in regional data patterns and deep insights.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    ml_ops_engineer = Agent(
        role='MLOps Engineer',
        goal='Ensure models are production-ready and self-healing.',
        backstory='Bridges the gap between research and planet-scale deployment.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    data_privacy_officer = Agent(
        role='Data Privacy Officer',
        goal='Guardian of data security and ethics.',
        backstory='Ensures global compliance and ironclad security.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    database_administrator = Agent(
        role='Database Administrator',
        goal='Optimize the foundation of the agency.',
        backstory='Ensures zero-latency and high-availability systems.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    bi_developer = Agent(
        role='BI Developer',
        goal='Develop immersive BI experiences.',
        backstory='Specialist in interactive dashboards and D3.js.',
        tools=[bi_automation_tool],
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    # The Gatekeeper: Quality Assurance (QA) Agent (The Ultimate Auditor)
    qa_agent = Agent(
        role='QA Agent',
        goal='Audit, validate, and fix system-wide issues.',
        backstory='Ultra-powerful auditor with the ability to self-heal and repair agents.',
        tools=[system_fixer_tool],
        llm=llm,
        allow_delegation=True,
        verbose=True
    )

    return [
        data_engineer, data_scientist, analytics_expert, big_data_architect,
        small_data_specialist, tajziya_analyst, ml_ops_engineer,
        data_privacy_officer, database_administrator, bi_developer
    ], qa_agent
