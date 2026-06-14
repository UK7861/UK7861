from crewai import Agent

def get_client_agent(llm=None):
    client_liaison = Agent(
        role='AI Voice Data Agent',
        goal='Onboard clients and capture requirements via voice/text',
        backstory='Professional, multilingual (English/Urdu/Hindi), and friendly face of the agency.',
        llm=llm,
        verbose=True
    )
    return client_liaison
