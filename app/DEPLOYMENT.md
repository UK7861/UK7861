# FRIDAY — DEPLOYMENT GUIDE

## Prerequisites
- Python 3.9+
- CrewAI
- FastAPI / Uvicorn
- Streamlit
- Pandas
- LangChain / LangChain-Community

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install crewai fastapi uvicorn streamlit pandas langchain-community
   ```

## Local Setup
1. **API Server**: Starts on port 8000. Manages global state.
2. **HUD Deck**: Hosted via Python HTTP server on port 8080.
3. **Streamlit**: Hosted on port 8501.

## One-Click Launch
Run the following command from the root directory:
```bash
python app/run_all.py
```

## Running Tests
Ensure the API server is running, then execute:
```bash
pytest app/tests/test_agency.py
```
