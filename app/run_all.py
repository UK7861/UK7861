import subprocess
import time
import os
import sys

def launch_friday():
    print("🚀 FRIDAY DATA CORE — SYSTEM LAUNCH SEQUENCE INITIATED")

    processes = []

    try:
        # 1. Start API Server
        print("Starting API Server...")
        api_process = subprocess.Popen([sys.executable, "app/api_server.py"])
        processes.append(api_process)
        time.sleep(2) # Wait for server to bind

        # 2. Start Scout Service
        print("Starting Scout Service...")
        scout_process = subprocess.Popen([sys.executable, "app/scout_service.py"])
        processes.append(scout_process)

        # 3. Start Streamlit Dashboard
        print("Starting Streamlit Dashboard...")
        streamlit_process = subprocess.Popen(["streamlit", "run", "app/app.py", "--server.port", "8501"])
        processes.append(streamlit_process)

        # 4. Start HUD (Simple HTTP Server for index.html)
        print("Starting HUD Command Deck on port 8080...")
        hud_process = subprocess.Popen([sys.executable, "-m", "http.server", "8080"], cwd="app")
        processes.append(hud_process)

        # 5. Start Autopilot
        print("Starting Autopilot Engine...")
        autopilot_process = subprocess.Popen([sys.executable, "app/autopilot.py"])
        processes.append(autopilot_process)

        print("\n✅ ALL SYSTEMS ONLINE")
        print("HUD Deck: http://localhost:8080")
        print("Management Room: http://localhost:8501")
        print("API Status: http://localhost:8000/state")

        # Keep main process alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 SHUTTING DOWN SYSTEMS...")
        for p in processes:
            p.terminate()
        print("GOODBYE, BOSS.")

if __name__ == "__main__":
    launch_friday()
