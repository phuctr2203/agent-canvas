# Agent Orchestration Patterns

Interactive web app for exploring common multi-agent orchestration patterns with real model calls through Ollama.

Users can select an orchestration pattern, write a prompt, run it through multiple configured agents, and watch the agent-to-agent communication in a visual UI.

## Patterns included

- **Single Agent** — one agent handles the full prompt.
- **Sequential** — agents pass work step-by-step from analysis to execution to formatting.
- **Parallel** — multiple agents work at the same time, then a synthesizer combines results.
- **Review Loop** — writer and critic iterate through draft, critique, and revision.
- **Coordinator (Router)** — router chooses a specialist agent based on the prompt.

## Features

- React UI for selecting patterns and entering prompts.
- FastAPI backend for orchestration logic.
- Ollama integration for real model responses.
- Agent configuration panel for names and system prompts.
- Visual node graph with active-agent highlighting.
- Live communication log showing message flow between agents.
- Markdown rendering for model output, including tables, lists, code blocks, and bold text.
- Light-mode interface optimized for readability.

## Tech stack

### Frontend

- React
- TypeScript
- Vite
- react-markdown
- remark-gfm

### Backend

- Python 3.11+
- FastAPI
- Pydantic
- httpx
- Uvicorn

### Model runtime

- Ollama
- Default model: `gpt-oss:20b-cloud`

## Project structure

```text
agent-orchestration/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI routes
│   │   ├── models.py          # Pydantic contracts
│   │   ├── ollama_client.py   # Ollama chat client
│   │   ├── patterns.py        # Pattern and agent definitions
│   │   └── simulation.py      # Orchestration flow logic
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/               # API client
│   │   ├── components/        # UI components
│   │   ├── types/             # TypeScript contracts
│   │   ├── App.tsx
│   │   └── styles.css
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Prerequisites

- Python 3.11 or newer
- Node.js 20 or newer
- npm
- Ollama running locally or reachable over network

## Ollama setup

Start Ollama and make sure the model is available:

```powershell
ollama run gpt-oss:20b-cloud
```

The backend reads these environment variables:

| Variable | Default | Description |
| --- | --- | --- |
| `OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `gpt-oss:20b-cloud` | Model used for all agent calls |

Example:

```powershell
$env:OLLAMA_BASE_URL="http://127.0.0.1:11434"
$env:OLLAMA_MODEL="gpt-oss:20b-cloud"
```

## Run locally

### 1. Install backend dependencies

From repository root:

```powershell
python -m pip install -e "backend"
```

### 2. Start backend

```powershell
python -m uvicorn app.main:app --app-dir backend --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Health check:

```text
http://127.0.0.1:8000/api/health
```

### 3. Install frontend dependencies

```powershell
npm.cmd install --prefix "frontend"
```

On Windows PowerShell, use `npm.cmd` if script execution blocks `npm.ps1`.

### 4. Start frontend

```powershell
npm.cmd run dev --prefix "frontend"
```

Frontend runs at:

```text
http://127.0.0.1:5173
```

## Build frontend

```powershell
npm.cmd run build --prefix "frontend"
```

## API endpoints

### `GET /api/health`

Returns backend health status.

### `GET /api/patterns`

Returns available orchestration patterns and default agent configurations.

### `POST /api/simulate`

Runs a prompt through selected orchestration pattern.

Request:

```json
{
  "pattern": "parallel",
  "prompt": "Compare Mini Cooper and Mercedes-Benz for city driving",
  "agents": [
    {
      "id": "agent-1",
      "name": "Researcher A",
      "role": "Technical Research",
      "systemPrompt": "You research technical aspects.",
      "color": "#10b981"
    }
  ]
}
```

Response:

```json
{
  "messages": [
    {
      "id": "msg-1",
      "timestamp": 1710000000000,
      "fromAgent": "Researcher A",
      "toAgent": "Synthesizer",
      "type": "response",
      "content": "Markdown response from model",
      "activeAgents": ["agent-1"]
    }
  ],
  "finalResult": "Final synthesized answer"
}
```

## How it works

1. Frontend loads pattern definitions from FastAPI.
2. User selects a pattern and enters a prompt.
3. Backend runs pattern-specific orchestration logic.
4. Each agent step calls Ollama with that agent's system prompt and current context.
5. Backend returns ordered messages and final result.
6. Frontend replays messages and highlights active agents in the graph.

## Notes

- Current orchestration is request/response based, not token streaming.
- Parallel pattern currently executes model calls sequentially on the backend while preserving parallel-style UI semantics.
- Coordinator routing uses keyword rules before calling the router model for explanation.

## License

MIT
