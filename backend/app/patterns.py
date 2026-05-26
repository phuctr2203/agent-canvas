from app.models import Agent, AgentPattern, PatternConfig

PATTERN_CONFIGS: dict[AgentPattern, PatternConfig] = {
    "single": PatternConfig(
        id="single",
        name="Single Agent",
        description="One agent processes the entire task.",
        agents=[
            Agent(id="agent-1", name="Assistant", role="General Purpose AI", systemPrompt="You are a helpful AI assistant.", color="#6366f1"),
        ],
    ),
    "sequential": PatternConfig(
        id="sequential",
        name="Sequential",
        description="Agents process tasks in sequence, passing context forward.",
        agents=[
            Agent(id="agent-1", name="Analyzer", role="Task Analysis", systemPrompt="You analyze the request and break it down into steps.", color="#8b5cf6"),
            Agent(id="agent-2", name="Executor", role="Task Execution", systemPrompt="You execute analyzed steps and provide results.", color="#3b82f6"),
            Agent(id="agent-3", name="Formatter", role="Output Formatting", systemPrompt="You format results in a user-friendly way.", color="#06b6d4"),
        ],
    ),
    "parallel": PatternConfig(
        id="parallel",
        name="Parallel",
        description="Multiple agents work at once, then a synthesizer combines output.",
        agents=[
            Agent(id="agent-1", name="Researcher A", role="Technical Research", systemPrompt="You research technical aspects.", color="#10b981"),
            Agent(id="agent-2", name="Researcher B", role="Practical Research", systemPrompt="You research practical applications.", color="#14b8a6"),
            Agent(id="agent-3", name="Synthesizer", role="Result Aggregator", systemPrompt="You combine all researcher results.", color="#6366f1"),
        ],
    ),
    "loop": PatternConfig(
        id="loop",
        name="Review Loop",
        description="Writer and critic iterate until quality criteria are met.",
        agents=[
            Agent(id="agent-1", name="Writer", role="Content Creator", systemPrompt="You create content based on requirements.", color="#f59e0b"),
            Agent(id="agent-2", name="Critic", role="Quality Reviewer", systemPrompt="You review content and provide critique.", color="#ef4444"),
        ],
    ),
    "coordinator": PatternConfig(
        id="coordinator",
        name="Coordinator (Router)",
        description="A coordinator routes tasks to the best specialist.",
        agents=[
            Agent(id="coordinator", name="Router", role="Task Coordinator", systemPrompt="You route tasks to the right specialist.", color="#8b5cf6"),
            Agent(id="agent-1", name="Code Expert", role="Programming Specialist", systemPrompt="You handle programming questions.", color="#3b82f6"),
            Agent(id="agent-2", name="Design Expert", role="Design Specialist", systemPrompt="You handle design questions.", color="#ec4899"),
            Agent(id="agent-3", name="Writing Expert", role="Content Specialist", systemPrompt="You handle writing and content questions.", color="#10b981"),
        ],
    ),
}

def list_patterns() -> list[PatternConfig]:
    return list(PATTERN_CONFIGS.values())

def get_pattern(pattern: AgentPattern) -> PatternConfig:
    return PATTERN_CONFIGS[pattern]
