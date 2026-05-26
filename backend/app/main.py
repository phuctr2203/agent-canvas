from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import PatternConfig, SimulationRequest, SimulationResult
from app.patterns import get_pattern, list_patterns
from app.simulation import simulate_pattern

app = FastAPI(title="Agent Orchestration Patterns API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/patterns", response_model=list[PatternConfig])
def patterns() -> list[PatternConfig]:
    return list_patterns()


@app.post("/api/simulate", response_model=SimulationResult)
async def simulate(request: SimulationRequest) -> SimulationResult:
    agents = request.agents or get_pattern(request.pattern).agents
    return await simulate_pattern(request.pattern, agents, request.prompt)
