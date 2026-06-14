import time
import requests
import random
from app.main import run_agency_mission

API_URL = "http://localhost:8000"

def autopilot_loop():
    print("Autopilot Cycle Executor Started...")

    while True:
        try:
            # Check if system is ready for a new mission
            print("Starting Autonomous Agency Cycle...")
            requests.post(f"{API_URL}/log", json={"message": "Initiating Autonomous Agency Cycle...", "level": "WARNING"})

            # Simulate a new client requirement
            reqs = [
                "Real-time sentiment analysis for social media",
                "Automated financial forecasting dashboard",
                "Customer churn prediction for Telecom",
                "Healthcare data interoperability layer"
            ]
            requirement = random.choice(reqs)

            requests.post(f"{API_URL}/log", json={"message": f"New Mission Received: {requirement}", "level": "INFO"})

            # This would normally block until mission is done
            # For simulation, we'll just run it
            result = run_agency_mission(requirement)

            requests.post(f"{API_URL}/log", json={"message": "Mission Accomplished. Final Report Generated.", "level": "SUCCESS"})

            time.sleep(60) # Wait before next cycle
        except Exception as e:
            print(f"Autopilot Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    autopilot_loop()
