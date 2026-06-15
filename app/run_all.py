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

        # 3. Start Next.js Frontend
        print("Starting Next.js Production HUD...")
        # (Assuming 'npm install' and 'npm run build' are done in Docker)
        # In a local sandbox, we can simulate with dev mode if node is present
        frontend_process = subprocess.Popen(["npm", "run", "dev"], cwd="frontend")
        processes.append(frontend_process)

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
