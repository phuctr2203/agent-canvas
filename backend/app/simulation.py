from itertools import count
from time import time

from app.models import Agent, AgentPattern, Message, SimulationResult
from app.ollama_client import chat

_message_ids = count(1)


def _message(
    from_agent: str,
    message_type: str,
    content: str,
    active_agents: list[str],
    to_agent: str | None = None,
    received_from: str | None = None,
) -> Message:
    return Message(
        id=f"msg-{next(_message_ids)}",
        timestamp=int(time() * 1000),
        fromAgent=from_agent,
        toAgent=to_agent,
        type=message_type,
        content=content,
        receivedFrom=received_from,
        activeAgents=active_agents,
    )


def _agent_system(agent: Agent) -> str:
    return (
        f"You are {agent.name}, role: {agent.role}.\n"
        f"{agent.system_prompt}\n"
        "Respond as this agent inside an orchestration demo. Be concise, concrete, and show useful intermediate work."
    )


async def _ask(agent: Agent, user_prompt: str) -> str:
    return await chat(_agent_system(agent), user_prompt)


def _route_specialist(prompt: str, specialists: list[Agent]) -> Agent:
    lowered = prompt.lower()
    if any(word in lowered for word in ["code", "api", "python", "react", "bug", "function"]):
        return specialists[0]
    if any(word in lowered for word in ["design", "ui", "ux", "layout", "figma", "color"]):
        return specialists[1]
    return specialists[2]


async def simulate_pattern(pattern: AgentPattern, agents: list[Agent], prompt: str) -> SimulationResult:
    messages: list[Message] = []

    if pattern == "single":
        agent = agents[0]
        active = [agent.id]
        messages.append(_message(agent.name, "thinking", f'Analyzing prompt: "{prompt}"', active))
        result = await _ask(agent, f"User prompt: {prompt}\nProvide final answer.")
        messages.append(_message(agent.name, "response", result, active))
        return SimulationResult(messages=messages, finalResult=result)

    if pattern == "sequential":
        analyzer, executor, formatter = agents
        analysis = await _ask(analyzer, f"User prompt: {prompt}\nBreak this into 3-5 actionable steps for another agent.")
        messages.append(_message(analyzer.name, "thinking", f'Breaking down request: "{prompt}"', [analyzer.id]))
        messages.append(_message(analyzer.name, "response", analysis, [analyzer.id], executor.name))

        execution = await _ask(executor, f"Original prompt: {prompt}\nAnalyzer plan:\n{analysis}\nExecute the plan and return working results.")
        messages.append(_message(executor.name, "received", "Received plan from Analyzer. Starting execution.", [executor.id], received_from=analyzer.name))
        messages.append(_message(executor.name, "response", execution, [executor.id], formatter.name))

        result = await _ask(formatter, f"Original prompt: {prompt}\nExecution result:\n{execution}\nFormat this into final user-facing response.")
        messages.append(_message(formatter.name, "received", "Received completed work from Executor. Formatting output.", [formatter.id], received_from=executor.name))
        messages.append(_message(formatter.name, "response", result, [formatter.id]))
        return SimulationResult(messages=messages, finalResult=result)

    if pattern == "parallel":
        workers = agents[:-1]
        synthesizer = agents[-1]
        worker_ids = [agent.id for agent in workers]
        findings: list[tuple[Agent, str]] = []

        for worker in workers:
            messages.append(_message(worker.name, "thinking", f'Investigating from {worker.role} perspective: "{prompt}"', worker_ids))

        for worker in workers:
            finding = await _ask(worker, f"User prompt: {prompt}\nResearch only from your role perspective ({worker.role}). Return key findings.")
            findings.append((worker, finding))
            messages.append(_message(worker.name, "response", finding, worker_ids, synthesizer.name))

        combined = "\n\n".join(f"{worker.name} ({worker.role}):\n{finding}" for worker, finding in findings)
        result = await _ask(synthesizer, f"Original prompt: {prompt}\nParallel findings:\n{combined}\nSynthesize final answer.")
        messages.append(_message(synthesizer.name, "received", f"Received {len(workers)} parallel reports. Combining results.", [synthesizer.id], received_from="Parallel researchers"))
        messages.append(_message(synthesizer.name, "response", result, [synthesizer.id]))
        return SimulationResult(messages=messages, finalResult=result)

    if pattern == "loop":
        writer, critic = agents
        draft = await _ask(writer, f"User prompt: {prompt}\nCreate a concise first draft.")
        messages.append(_message(writer.name, "thinking", f'Creating first draft for: "{prompt}"', [writer.id]))
        messages.append(_message(writer.name, "response", draft, [writer.id], critic.name))

        critique = await _ask(critic, f"Original prompt: {prompt}\nDraft:\n{draft}\nCritique this draft. List concrete improvements.")
        messages.append(_message(critic.name, "received", "Draft received. Reviewing clarity, completeness, and structure.", [critic.id], received_from=writer.name))
        messages.append(_message(critic.name, "critique", critique, [critic.id], writer.name))

        revision = await _ask(writer, f"Original prompt: {prompt}\nDraft:\n{draft}\nCritique:\n{critique}\nRevise into final content.")
        messages.append(_message(writer.name, "received", "Critique received. Revising draft with requested improvements.", [writer.id], received_from=critic.name))
        messages.append(_message(writer.name, "response", revision, [writer.id], critic.name))

        final_review = await _ask(critic, f"Original prompt: {prompt}\nRevision:\n{revision}\nApprove or give one final note. Keep concise.")
        messages.append(_message(critic.name, "response", final_review, [critic.id]))
        result = revision
        return SimulationResult(messages=messages, finalResult=result)

    coordinator, *specialists = agents
    selected = _route_specialist(prompt, specialists)
    messages.append(_message(coordinator.name, "thinking", f'Classifying request: "{prompt}"', [coordinator.id]))
    route = await _ask(coordinator, f"User prompt: {prompt}\nAvailable specialists: {', '.join(f'{agent.name} ({agent.role})' for agent in specialists)}\nExplain briefly why this should route to {selected.name}.")
    messages.append(_message(coordinator.name, "routing", route, [coordinator.id], selected.name))

    specialist_result = await _ask(selected, f"Routed prompt: {prompt}\nCoordinator rationale:\n{route}\nAnswer using your specialist expertise.")
    messages.append(_message(selected.name, "received", f"Received routed task from {coordinator.name}. Applying {selected.role.lower()} expertise.", [selected.id], received_from=coordinator.name))
    messages.append(_message(selected.name, "response", specialist_result, [selected.id], coordinator.name))

    result = await _ask(coordinator, f"Original prompt: {prompt}\nSpecialist response from {selected.name}:\n{specialist_result}\nPrepare final user-facing response.")
    messages.append(_message(coordinator.name, "response", result, [coordinator.id]))
    return SimulationResult(messages=messages, finalResult=result)
