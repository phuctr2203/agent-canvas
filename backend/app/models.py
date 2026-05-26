from typing import Literal

from pydantic import BaseModel, Field

AgentPattern = Literal["single", "sequential", "parallel", "loop", "coordinator"]
MessageType = Literal["thinking", "response", "routing", "critique", "received"]


class Agent(BaseModel):
    id: str
    name: str
    role: str
    system_prompt: str = Field(alias="systemPrompt")
    color: str

    model_config = {"populate_by_name": True}


class PatternConfig(BaseModel):
    id: AgentPattern
    name: str
    description: str
    agents: list[Agent]


class Message(BaseModel):
    id: str
    timestamp: int
    from_agent: str = Field(alias="fromAgent")
    to_agent: str | None = Field(default=None, alias="toAgent")
    type: MessageType
    content: str
    received_from: str | None = Field(default=None, alias="receivedFrom")
    active_agents: list[str] = Field(default_factory=list, alias="activeAgents")

    model_config = {"populate_by_name": True}


class SimulationRequest(BaseModel):
    pattern: AgentPattern
    prompt: str
    agents: list[Agent] | None = None


class SimulationResult(BaseModel):
    messages: list[Message]
    final_result: str = Field(alias="finalResult")

    model_config = {"populate_by_name": True}
