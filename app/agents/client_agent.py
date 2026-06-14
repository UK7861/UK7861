from crewai import Agent
from app.tools.data_tools import live_data_stream_tool

def get_client_agent(llm=None):
    live_data_collector = Agent(
        role='Live Data Collector',
        goal='Collect live data streams as the client speaks and sync them directly to the Friday Live Server.',
        backstory='The real-time ear of Friday. Captures every requirement and data snippet instantly as the client speaks, ensuring zero latency between client and agency.',
        tools=[live_data_stream_tool],
        llm=llm,
        verbose=True
    )
    return live_data_collector
