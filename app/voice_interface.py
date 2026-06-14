import requests
import time

API_URL = "http://localhost:8000"

def simulate_voice_command(command: str):
    print(f"Voice Command Received: {command}")
    requests.post(f"{API_URL}/log", json={"message": f"VOICE COMMAND: {command}", "level": "INFO"})

    # Process common commands
    if "status" in command.lower():
        print("Friday CEO: All systems are operational and agents are on standby.")
    elif "start mission" in command.lower():
        print("Friday CEO: Initiating new mission sequence.")
    else:
        print(f"Friday CEO: Processing command: {command}")

if __name__ == "__main__":
    simulate_voice_command("Friday, status report please.")
    time.sleep(2)
    simulate_voice_command("Start mission: Analyze quarterly sales data.")
