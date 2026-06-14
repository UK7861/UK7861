import pytest
from app.agents.data_agents import get_data_agents
from app.agents.acquisition_agents import get_acquisition_agents
from app.agents.client_agent import get_client_agent
from app.tools.data_tools import data_cleaning_tool
import json

def test_agent_counts():
    data_team, qa = get_data_agents()
    ceo, scout = get_acquisition_agents()
    client_liaison = get_client_agent()

    # Updated for v6.0 Roster (BI specialized agents added)
    assert len(data_team) == 8
    assert qa.role == 'QA Agent'
    assert ceo.role == 'Friday CEO'
    assert scout.role == 'JARVIS Scout & Liaison'
    assert client_liaison.role == 'Live Data Collector'

def test_data_cleaning_tool():
    raw_data = json.dumps([
        {"id": 1, "name": "Alice"},
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": None}
    ])
    cleaned_json = data_cleaning_tool.run(raw_data)
    cleaned_data = json.loads(cleaned_json)

    assert len(cleaned_data) == 1
    assert cleaned_data[0]["name"] == "Alice"

def test_api_server_endpoints():
    from fastapi.testclient import TestClient
    from app.api_server import app

    client = TestClient(app)
    response = client.get("/state")
    assert response.status_code == 200
    assert "status" in response.json()
