import requests
import time
import random

API_URL = "http://localhost:8000"

def simulate_tts(text: str):
    """Simulates Text-to-Speech output (JARVIS voice)."""
    print(f"\n[FRIDAY VOICE]: {text}")
    # In a real app, you'd use a library like pyttsx3 or gTTS here

def simulate_stt(audio_input: str):
    """Simulates Speech-to-Text input."""
    # This mock converts "voice input" strings into commands
    print(f"[USER VOICE]: {audio_input}")
    return audio_input

def process_voice_command(voice_command: str):
    command = simulate_stt(voice_command)
    requests.post(f"{API_URL}/log", json={"message": f"VOICE COMMAND: {command}", "level": "INFO"})

    # Logic for response
    if "status" in command.lower():
        resp = "Systems are nominal, Boss. 13 agents are online and standing by."
    elif "create" in command.lower() or "agent" in command.lower():
        resp = "Initiating Agent Factory. Synthesizing new specialized unit as requested."
    elif "shukriya" in command.lower() or "kaise ho" in command.lower():
        resp = "Shukriya Boss! Main bilkul theek hoon, aapka shukriya. Mission ki tayyari mukammal hai."
    else:
        resp = f"Processing command: {command}. Executing Friday protocols."

    simulate_tts(resp)
    requests.post(f"{API_URL}/log", json={"message": f"CEO VOCAL: {resp}", "level": "SUCCESS"})

if __name__ == "__main__":
    commands = [
        "Friday, status report please.",
        "Friday, create a new team for Deep Web Scraping.",
        "Friday, kaise ho? Status check karo.",
        "Mission start karo: Analyze retail data."
    ]

    for cmd in commands:
        process_voice_command(cmd)
        time.sleep(2)
