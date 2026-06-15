import pytest
import requests
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pinpoint_core.app.models import Base, Tenant, Branch
from pinpoint_core.app.main import app

# Use a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_pinpoint.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_module():
    Base.metadata.create_all(bind=engine)

def teardown_module():
    import os
    if os.path.exists("test_pinpoint.db"):
        os.remove("test_pinpoint.db")

def test_onboarding_and_duplication():
    # 1. Successful Signup (Consolidated)
    signup_data = {
        "company_name": "Test Clinic",
        "email": "test@clinic.com",
        "password": "password123",
        "business_number": "+923001234567",
        "industry_type": "Clinic",
        "initial_branch_name": "Main Branch",
        "initial_business_address": "123 Healthcare St, Islamabad",
        "initial_latitude": 33.6844,
        "initial_longitude": 73.0479
    }

    # We use requests against the running server for a true integration test
    # (Server must be running on port 8000)
    API_URL = "http://localhost:8000"

    resp = requests.post(f"{API_URL}/auth/signup", json=signup_data)
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    tenant_id = data["tenant_id"]

    # 2. Duplicate Branch Name (Multi-Branch Anti-Duplication Rule)
    duplicate_branch = {
        "branch_name": "Main Branch", # Duplicate
        "business_address": "456 Other St",
        "latitude": 34.0,
        "longitude": 74.0
    }
    resp = requests.post(f"{API_URL}/branches?tenant_id={tenant_id}", json=duplicate_branch)
    assert resp.status_code == 400
    assert "Duplicate" in resp.json()["detail"]

    # 3. Duplicate Coordinates
    duplicate_coords = {
        "branch_name": "New Branch",
        "business_address": "456 Other St",
        "latitude": 33.6844, # Duplicate
        "longitude": 73.0479  # Duplicate
    }
    resp = requests.post(f"{API_URL}/branches?tenant_id={tenant_id}", json=duplicate_coords)
    assert resp.status_code == 400
    assert "Duplicate" in resp.json()["detail"]

def test_voice_endpoint():
    API_URL = "http://localhost:8000"
    resp = requests.get(f"{API_URL}/api/v1/voice/test-sample")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "audio/mpeg"

if __name__ == "__main__":
    test_onboarding_and_duplication()
    test_voice_endpoint()
    print("Integration tests passed!")
