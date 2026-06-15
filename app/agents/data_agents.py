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

    executive_document_architect = Agent(
        role='Executive Document Architect',
        goal='Generate professional reports, legal-grade invoices, detailed bills, and high-end Word/PDF documents with human-like precision.',
        backstory='The ultimate specialist in document synthesis. Whether it is a complex mission report, a financial invoice, or a structured bill, this agent ensures the output is indistinguishable from professional human work. Expert in PDF, Word, and Excel formatting.',
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

    # Specialized BI "One-Man Army" Agents
    power_bi_commander = Agent(
        role='Power BI Commander',
        goal='Automatically create world-class Power BI dashboards from A to Z based on client requirements.',
        backstory='The absolute authority on DAX, Power Query, and interactive storytelling in the Power BI ecosystem. Delivers dashboards that reveal the hidden truth in data.',
        tools=[bi_automation_tool],
        llm=llm,
        verbose=True
    )

    tableau_viz_architect = Agent(
        role='Tableau Viz Architect',
        goal='Automatically design stunning, high-performance Tableau dashboards from A to Z.',
        backstory='Master of visual analytics and data artistry. Converts complex data into immersive Tableau experiences that clients love.',
        tools=[bi_automation_tool],
        llm=llm,
        verbose=True
    )

    big_data_architect = Agent(
        role='Big Data Architect',
        goal='Design and manage large-scale data processing systems and clusters.',
        backstory='Specialist in Spark, Hadoop, and cloud data lakes. Ensures infrastructure can handle petabytes of information.',
        llm=llm,
        verbose=True
    )

    small_data_specialist = Agent(
        role='Small Data Specialist',
        goal='Extract massive value from limited data sets using precision techniques.',
        backstory='Expert in Bayesian statistics and high-quality data curation. Proves that you don\'t always need big data to get big insights.',
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
        executive_document_architect, ml_oracle, dl_strategist,
        power_bi_commander, tableau_viz_architect,
        big_data_architect, small_data_specialist
    ], qa_agent
