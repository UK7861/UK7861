from crewai import Agent

def get_client_agent(llm=None):
    client_liaison = Agent(
        role='AI Voice Data Agent',
        goal='Onboard clients and capture requirements via voice/text in English and Roman Urdu.',
        backstory='The multilingual interface of Friday. Fluent in English and Roman Urdu/Hindi. Professional, intuitive, and JARVIS-like in communication.',
        llm=llm,
        verbose=True
    )
    return client_liaison
