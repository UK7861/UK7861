import time
import requests
import random
from app.main import run_agency_mission

API_URL = "http://localhost:8000"

def autopilot_loop():
    print("Friday Autopilot & System Health Monitor Started...")

    while True:
        try:
            # System Health Check (Self-Healing)
            print("Running System-Wide Diagnostics...")
            requests.post(f"{API_URL}/log", json={"message": "Running System-Wide Diagnostics...", "level": "INFO"})

            # Simulate a health check
            health_status = random.random()
            if health_status > 0.9:
                # 10% chance of a "problem" appearing that needs fixing
                problem = "Agent memory leak detected in DS-Agent"
                requests.post(f"{API_URL}/log", json={"message": f"SYSTEM ANOMALY: {problem}", "level": "ERROR"})
                time.sleep(2)
                requests.post(f"{API_URL}/log", json={"message": "QA Agent: Initiating Self-Healing sequence...", "level": "WARNING"})
                time.sleep(2)
                requests.post(f"{API_URL}/log", json={"message": f"QA Agent: {problem} resolved. System stabilized.", "level": "SUCCESS"})

            # Check if system is ready for a new mission
            print("Initiating Autonomous Agency Cycle...")
            requests.post(f"{API_URL}/log", json={"message": "Initiating Autonomous Agency Cycle...", "level": "WARNING"})

            # Simulate a new client requirement
            reqs = [
                "Real-time sentiment analysis for social media",
                "Automated financial forecasting dashboard",
                "Customer churn prediction for Telecom",
                "Healthcare data interoperability layer",
                "Friday, create a new scraping unit for e-commerce."
            ]
            requirement = random.choice(reqs)

            requests.post(f"{API_URL}/log", json={"message": f"MISSION INITIATED: {requirement}", "level": "INFO"})

            # Run the mission
            result = run_agency_mission(requirement)

            requests.post(f"{API_URL}/log", json={"message": "MISSION COMPLETE: Final report ready for Boss.", "level": "SUCCESS"})

            # Evolution Step
            requests.post(f"{API_URL}/log", json={"message": "Evolution Engine: Upgrading system intelligence...", "level": "INFO"})
            requests.post(f"{API_URL}/upgrade_core")

            # Update overall mission count
            state = requests.get(f"{API_URL}/state").json()
            requests.post(f"{API_URL}/update_agent", params={
                "name": "System",
                "status": "IDLE",
                "progress": 0
            })

            time.sleep(30) # Wait before next cycle
        except Exception as e:
            print(f"Autopilot Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    autopilot_loop()
