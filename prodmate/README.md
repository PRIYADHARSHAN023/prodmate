# ProdMate - AI-Powered Personal Productivity Multi-Agent Assistant (Prototype)

## Overview
ProdMate is a prototype multi-agent system that demonstrates:
- Agent tools & MCP-like `/tool/run` contract
- Sessions & long-term memory
- Long-running operations (pending + user approval)
- Simple A2A via coordinator router
- Observability (logs + basic Prometheus metrics)

This repo is a runnable local prototype using FastAPI services for the coordinator and agents.

## Run locally (quick)
1. Create virtualenv and install:
   ```
   python -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Start services (examples):
   - Coordinator:
     ```
     uvicorn backend.main:app --reload --port 8000
     ```
   - Task Manager:
     ```
     uvicorn agents.task_manager.app:app --reload --port 8101
     ```
3. Test add-task:
   ```
   curl -X POST "http://localhost:8000/api/v1/handle" -H "Content-Type: application/json" -d '{"user_id":"u1","text":"Add task: buy milk"}'
   ```

## Project structure
- backend/           Coordinator (FastAPI)
- agents/            Agents (task_manager, schedule, reminder, memory, search)
- shared/            Shared models & memory implementation
- notebooks/         Evaluation & demo scripts
- infra/             Docker / docker-compose (optional)

## Kaggle / Capstone checklist
See the email mapping and include README sections describing Unit 2–5 mappings.

## License
MIT