from crewai import Agent
from app.tools.data_tools import data_cleaning_tool, bi_automation_tool

def get_data_agents(llm=None):
    # Specialized 10 Core Data Agents
    data_engineer = Agent(
        role='Data Engineer',
        goal='Build and maintain data pipelines',
        backstory='Expert in SQL, Python, and ETL processes.',
        tools=[data_cleaning_tool],
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    data_scientist = Agent(
        role='Data Scientist',
        goal='Develop predictive models and perform advanced analysis',
        backstory='Specialized in machine learning and statistical modeling.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    analytics_expert = Agent(
        role='Analytics Expert',
        goal='Transform data into actionable insights',
        backstory='Master of data visualization and business intelligence.',
        tools=[bi_automation_tool],
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    big_data_architect = Agent(
        role='Big Data Architect',
        goal='Design scalable big data infrastructures',
        backstory='Deep knowledge of Hadoop, Spark, and cloud data warehouses.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    small_data_specialist = Agent(
        role='Small Data Specialist',
        goal='Extract value from smaller, highly focused datasets',
        backstory='Expert in Excel, Google Sheets, and lightweight database solutions.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    tajziya_analyst = Agent(
        role='Deep Tajziya Analyst',
        goal='Perform deep, culturally nuanced data analysis',
        backstory='Expert in deep analysis with a focus on regional data patterns.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    ml_ops_engineer = Agent(
        role='MLOps Engineer',
        goal='Deploy and monitor machine learning models in production',
        backstory='Specialist in CI/CD for ML and model performance tracking.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    data_privacy_officer = Agent(
        role='Data Privacy Officer',
        goal='Ensure data compliance and security',
        backstory='Expert in GDPR, CCPA, and data encryption techniques.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    database_administrator = Agent(
        role='Database Administrator',
        goal='Optimize and secure database performance',
        backstory='Master of indexing, query optimization, and backups.',
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    bi_developer = Agent(
        role='BI Developer',
        goal='Create interactive dashboards and reports',
        backstory='Specialist in Tableau, Power BI, and D3.js integrations.',
        tools=[bi_automation_tool],
        llm=llm,
        allow_delegation=False,
        verbose=True
    )

    # The Gatekeeper: Quality Assurance (QA) Agent
    qa_agent = Agent(
        role='QA Agent',
        goal='Audit and validate all outputs from the data team',
        backstory='Ultra-powerful auditor trained to catch mistakes and ensure 100% accuracy.',
        llm=llm,
        allow_delegation=True,
        verbose=True
    )

    return [
        data_engineer, data_scientist, analytics_expert, big_data_architect,
        small_data_specialist, tajziya_analyst, ml_ops_engineer,
        data_privacy_officer, database_administrator, bi_developer
    ], qa_agent
