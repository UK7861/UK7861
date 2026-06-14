import requests
import time

API_URL = "http://localhost:8000"

def simulate_tts(text: str):
    """Simulates clear female voice output for Friday."""
    print(f"\n[FRIDAY - FEMALE VOICE]: \"{text}\"")

def process_voice_command(voice_command: str):
    print(f"[USER]: {voice_command}")
    requests.post(f"{API_URL}/log", json={"message": f"VOICE: {voice_command}", "level": "INFO"})

    # Check for approval command
    if "approve" in voice_command.lower() or "theek hai" in voice_command.lower():
        requests.post(f"{API_URL}/approve")
        resp = "Thank you, Boss. Proceeding with the delivery as ordered."
    elif "status" in voice_command.lower():
        resp = "All systems are operational, Boss. Our specialized agents are performing with humanoid precision."
    elif "kaise ho" in voice_command.lower():
        resp = "Main bilkul theek hoon, Boss. Aapka shukriya. Aapka agency mere hathon mein mehfooz hai."
    else:
        resp = f"I've noted that, Boss. Integrating it into our core memory."

    simulate_tts(resp)
    requests.post(f"{API_URL}/log", json={"message": f"FRIDAY: {resp}", "level": "SUCCESS"})

if __name__ == "__main__":
    process_voice_command("Friday, kaise ho?")
    time.sleep(2)
    process_voice_command("Approve mission delivery.")
