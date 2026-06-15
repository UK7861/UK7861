# FRIDAY OS - Production Deployment Guide

## Architecture
- **Backend**: FastAPI with LangGraph Orchestration.
- **Frontend**: Next.js 15 with Three.js (HUD) and D3.js (Neural Graph).
- **Persistence**: PostgreSQL (Structured), Neo4j (Graph Memory), Redis (State/Cache).
- **LLM**: Supports OpenAI, Gemini, and Ollama.

## One-Click Start (Docker)
Ensure you have Docker and Docker Compose installed.

1. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Launch Ecosystem**:
   ```bash
   docker-compose up --build
   ```

3. **Access Interfaces**:
   - **HUD Command Deck**: `http://localhost:3000`
   - **API Brain**: `http://localhost:8000`
   - **Postgres**: `localhost:5432`
   - **Neo4j Browser**: `http://localhost:7474`
   - **Redis**: `localhost:6379`

## Manual Development Setup
1. **Backend**:
   ```bash
   pip install -r requirements.txt
   export PYTHONPATH=.
   python app/api_server.py
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Production Scaling
- **Kubernetes**: Recommended for orchestration of individual agents.
- **gVisor**: Recommended for the Python Code Sandbox isolation.
- **ELK Stack**: Recommended for advanced observability.
