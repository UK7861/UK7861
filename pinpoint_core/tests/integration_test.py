import requests
import time

def test_onboarding_and_duplication():
    API_URL = "http://localhost:8000"

    # 1. Successful Signup (Consolidated)
    signup_data = {
        "company_name": "Integration Clinic",
        "branch_name": "Initial Branch",
        "email": "integration@clinic.com",
        "password": "password123",
        "business_number": "+923000000000",
        "business_address": "Islamabad, PK",
        "industry_type": "Clinic",
        "latitude": 33.7294,
        "longitude": 73.0931
    }

    resp = requests.post(f"{API_URL}/auth/signup", json=signup_data)
    assert resp.status_code == 200, f"Signup failed: {resp.text}"

    # Login to get JWT
    login_resp = requests.post(f"{API_URL}/auth/login", json={"email": "integration@clinic.com", "password": "password123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Duplicate Branch Name (Multi-Branch Anti-Duplication Rule)
    duplicate_branch = {
        "branch_name": "Initial Branch",
        "business_address": "Different Address",
        "latitude": 0.0,
        "longitude": 0.0
    }
    resp = requests.post(f"{API_URL}/branches", json=duplicate_branch, headers=headers)
    assert resp.status_code == 400
    assert "already exists" in resp.json()["detail"]

    # 3. Duplicate Coordinates
    duplicate_coords = {
        "branch_name": "Another Branch",
        "business_address": "Different Address",
        "latitude": 33.7294,
        "longitude": 73.0931
    }
    resp = requests.post(f"{API_URL}/branches", json=duplicate_coords, headers=headers)
    assert resp.status_code == 400
    assert "already exists" in resp.json()["detail"]

def test_voice_endpoint():
    API_URL = "http://localhost:8000"
    login_resp = requests.post(f"{API_URL}/auth/login", json={"email": "integration@clinic.com", "password": "password123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(f"{API_URL}/api/v1/voice/test-sample", headers=headers)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "audio/mpeg"

if __name__ == "__main__":
    try:
        test_onboarding_and_duplication()
        test_voice_endpoint()
        print("Integration tests passed!")
    except Exception as e:
        print(f"Test failed: {e}")
        exit(1)
