# FRIDAY CEO OPERATIONAL GUIDE

## Overview
Friday is an autonomous data agency. You interact with the system via the HUD Command Deck or the Streamlit Management Room.

## Agent Architecture
- **CEO**: Orchestrates and delegates.
- **QA**: Audits and verifies outputs.
- **Scout**: Finds leads on Upwork/Freelancer.
- **Client Agent**: Multilingual onboarding interface.

## Voice Commands (Simulated)
You can use `voice_interface.py` to simulate voice commands:
- "Friday, status report."
- "Launch mission for [Client Name]."

## Mission Lifecycle
1. Scout finds a lead.
2. Client Agent onboards.
3. CEO plans tasks.
4. 10 Core Agents execute.
5. QA verifies.
6. Report synthesized.

## Troubleshooting
- Check `api_server.py` logs if HUD is not updating.
- Ensure all dependencies are in the virtual environment.
