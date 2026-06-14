from crewai import Agent
from app.tools.data_tools import (
    data_cleaning_tool, bi_automation_tool, system_fixer_tool,
    document_generation_tool, sql_query_master_tool
)

def get_data_agents(llm=None):
    # Specialized "One-Man Army" Agents
    python_overlord = Agent(
        role='Python Overlord',
        goal='Handle all Python-related work from A to Z, including automation, backend logic, and scripting.',
        backstory='Master of the Python ecosystem. Capable of building anything from simple scripts to complex AI-driven backends autonomously.',
        tools=[data_cleaning_tool],
        llm=llm,
        verbose=True
    )

    sql_overlord = Agent(
        role='SQL Overlord',
        goal='Handle all SQL-related work from A to Z, including schema design, query optimization, and complex extractions.',
        backstory='The ultimate authority on databases. Expert in PostgreSQL, MySQL, and NoSQL. Ensures data is always structured and accessible.',
        tools=[sql_query_master_tool],
        llm=llm,
        verbose=True
    )

    excel_master = Agent(
        role='Excel Master',
        goal='Handle the entire work of Excel, from complex formulas to advanced VBA and data modeling.',
        backstory='The world-class specialist in spreadsheet manipulation and data structuring.',
        llm=llm,
        verbose=True
    )

    humanoid_report_generator = Agent(
        role='Humanoid Report Generator',
        goal='Create high-end Word, PDF, Excel, and Presentation (PPT) reports with human-like writing.',
        backstory='Specialized in natural language generation, professional document design, and persuasive presentations. Reports and slides are indistinguishable from high-end human work.',
        tools=[document_generation_tool],
        llm=llm,
        verbose=True
    )

    ml_oracle = Agent(
        role='Machine Learning Oracle',
        goal='Predict past, present, and future trends. Identify company problems and sales opportunities with precision.',
        backstory='The predictive powerhouse. Tells the client exactly what happened, what is happening, and what will happen to their products and market.',
        llm=llm,
        verbose=True
    )

    dl_strategist = Agent(
        role='Deep Learning Strategist',
        goal='Execute complex deep learning models to solve the most difficult business challenges.',
        backstory='Specialist in neural networks and deep pattern recognition. Works alongside the ML Oracle to provide a 360-degree vision of the business.',
        llm=llm,
        verbose=True
    )

    # Secondary specialized agents (still acting as one-man armies)
    analytics_expert = Agent(
        role='Analytics Expert',
        goal='Transform raw data into actionable business intelligence.',
        backstory='Expert in Tableau, Power BI, and interactive analytics.',
        tools=[bi_automation_tool],
        llm=llm,
        verbose=True
    )

    # The Gatekeeper
    qa_agent = Agent(
        role='QA Agent',
        goal='Audit, validate, and fix system-wide issues.',
        backstory='The ultimate auditor. Ensures every output is perfect and the system remains stable.',
        tools=[system_fixer_tool],
        llm=llm,
        verbose=True
    )

    return [
        python_overlord, sql_overlord, excel_master,
        humanoid_report_generator, ml_oracle, dl_strategist,
        analytics_expert
    ], qa_agent
