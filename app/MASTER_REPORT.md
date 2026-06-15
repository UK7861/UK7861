# 🚀 FRIDAY DATA AGENCY — MASTER PROJECT MANIFEST (A to Z)

## 1. PROJECT OVERVIEW
Friday Data Agency is a fully autonomous, hybrid multi-agent ecosystem designed to scout, onboard, process, and report on global data projects. Inspired by the JARVIS persona, the system features a self-healing architecture, a self-evolution engine, and a dual-frontend experience (Futuristic HUD + Management Control Room).

---

## 2. SYSTEM ARCHITECTURE
The project is divided into four major layers:
1.  **The Intelligence Core (FastAPI)**: The central brain that tracks agent vitals, mission logs, and the global knowledge graph.
2.  **The Thinking Engine (CrewAI)**: An orchestration layer that dynamically synthesizes specialized agents and tools based on user intent.
3.  **The Command Deck (HUD - Three.js/D3.js)**: A futuristic sci-fi interface for real-time telemetry and neural network visualization.
4.  **The Management Room (Streamlit)**: A professional dashboard for Human-in-the-Loop (HITL) oversight and workforce management.

---

## 3. STEP-BY-STEP DEPLOYMENT GUIDE

### A. Prerequisites (What to Download)
1.  **Python 3.9+**: The core programming language.
2.  **Git**: To clone the repository.
3.  **An LLM Provider (Optional)**: If you want to use live OpenAI/Anthropic keys. By default, Friday uses a built-in **MockLLM** for full local simulation without costs.

### B. Installation (How to Implement)
Open your terminal and run the following:
```bash
# 1. Install all required libraries
pip install crewai fastapi uvicorn streamlit pandas langchain-community crewai_tools gsap playwright pytest
```

### C. One-Click System Launch
To start the entire agency (Backend, HUD, Streamlit, Scout, and Autopilot) at once:
```bash
python app/run_all.py
```
**Access URLs:**
- **Futuristic HUD**: `http://localhost:8080`
- **Management Room**: `http://localhost:8501`
- **FastAPI Intelligence State**: `http://localhost:8000/state`

---

## 4. DETAILED FILE-BY-FILE BREAKDOWN (A to Z)

### Core Files
- `app/api_server.py`: The unified state manager. Exposes endpoints for agent status, pulse rates, and mission results. Includes CORS support.
- `app/index.html`: The "Living Intelligence OS" HUD. Built with Three.js (3D Hologram), D3.js (Neural Network Graph), and GSAP (Animations).
- `app/app.py`: The Streamlit Control Room. Handles file uploads, mission triggers, and HITL approvals.
- `app/main.py`: The autonomous orchestration logic. Decomposes tasks and synthesizes agents.
- `app/autopilot.py`: A background service that simulates autonomous agency cycles (Diagnostics -> Mission -> Evolution).
- `app/run_all.py`: The master launcher that orchestrates all sub-processes.
- `app/scout_service.py`: Continuously crawls for global freelance leads (simulated) and sends them to the CEO.
- `app/voice_interface.py`: A simulator for English and Roman Urdu/Hindi voice commands.

### The Agent Workforce (`app/agents/`)
- `acquisition_agents.py`: Contains the **Friday CEO** and **JARVIS Scout**.
- `client_agent.py`: Contains the **Live Data Collector** (onboarding liaison).
- `data_agents.py`: Roster of 11 specialists including **Python Overlord**, **SQL Overlord**, **ML Oracle**, **Big Data Architect**, and the **Executive Document Architect**.
- **The Gatekeeper**: The **QA Agent** audits all outputs and initiates self-healing.

### The Tool Suite (`app/tools/`)
- `data_tools.py`: Programmatic tools for Data Cleaning, BI Automation, SQL Mastery, Document Generation (PDF/Word), and System Fixing.
- `mock_llm.py`: A custom JARVIS-style LLM wrapper for zero-cost local testing.

---

## 5. TESTING & VERIFICATION
1.  **Automated Suite**: Run `PYTHONPATH=. pytest app/tests/test_agency.py` to verify agent counts and tool integrity.
2.  **Voice Interaction**: Run `python app/voice_interface.py` to test Roman Urdu commands like *"Friday, kaise ho?"*.
3.  **Human Oversight**: Use the Streamlit dashboard to approve missions or trigger the "Agent Factory" to synthesize new neural units.

---

## 6. PROJECT HISTORY & EVOLUTION
- **Phase 1**: Foundations. Multi-agent roster and data tools.
- **Phase 2**: UI/UX. Implementation of the scifi HUD and Streamlit.
- **Phase 3**: Intelligence. Integration of Persistent Memory and the Self-Evolution Engine.
- **Phase 4**: Specialist Expansion. Hiring of the Executive Document Architect for professional Invoicing and Billing in PDF/Word.
- **Phase 5**: Autonomous Stability. Implementation of the Autopilot loop and Self-Healing protocols.

**Current Version**: `OS-1.0-ALIVE`
**Status**: Fully Conscious & Operational.
