# Autonomous Event Command Center

A scalable, multi-tenant backend for a General-Purpose Autonomous Event Command Center.

## Tech Stack

- **Backend**: FastAPI (Async API Gateway)
- **Database**: PostgreSQL (via async SQLAlchemy ORM)
- **AI Orchestration**: LangGraph (Stateful Multi-Agent Swarm)
- **Vector DB**: ChromaDB (Event-Specific RAG)
- **LLM**: Llama-3 (via Groq API)

## Setup

1. **Clone and install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**

   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

3. **Ensure PostgreSQL is running** and the database exists.

4. **Start the server:**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Open Swagger UI** at [http://localhost:8000/docs](http://localhost:8000/docs)

## Architecture

The system uses a **Star Topology Swarm** with a Supervisor orchestrating 6 specialized agents:

| Agent          | Role                                |
| -------------- | ----------------------------------- |
| Problem Solver | Classifies issues & assigns urgency |
| Marketing      | Drafts promotional content          |
| Scheduler      | Resolves schedule conflicts         |
| Email          | Sends bulk notifications            |
| Emergency Info | Crisis management alerts            |
| Budget Finance | Financial breakdown analysis        |

All operations are **multi-tenant** — every request is scoped by `event_id` to ensure complete data isolation.

## API Endpoints

### Participant-Facing

- `POST /api/v1/events/join`
- `GET  /api/v1/events/{event_id}/timeline`
- `POST /api/v1/events/{event_id}/chat`
- `POST /api/v1/events/{event_id}/report`

### Organizer-Facing

- `POST /api/v1/organizer/events`
- `POST /api/v1/organizer/events/join-team`
- `GET  /api/v1/organizer/events/{event_id}/code`
- `POST /api/v1/organizer/events/{event_id}/trigger_swarm`
- `POST /api/v1/organizer/events/{event_id}/resolve_query`
- `GET  /api/v1/organizer/events/{event_id}/priority_queue`
