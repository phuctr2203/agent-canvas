import { Agent, AgentPattern } from '../types/agent';

interface NodeGraphProps {
  pattern: AgentPattern;
  agents: Agent[];
  activeAgents: Set<string>;
}

function getLayout(pattern: AgentPattern, index: number, total: number) {
  if (pattern === 'single') return { left: 50, top: 50 };
  if (pattern === 'sequential') return { left: 18 + index * 32, top: 50 };
  if (pattern === 'parallel') return index === total - 1 ? { left: 76, top: 50 } : { left: 24, top: 28 + index * 34 };
  if (pattern === 'loop') return { left: index === 0 ? 35 : 65, top: 50 };
  return index === 0 ? { left: 50, top: 22 } : { left: 22 + (index - 1) * 28, top: 68 };
}

function getEdges(pattern: AgentPattern, agents: Agent[]) {
  if (pattern === 'single') return [];
  if (pattern === 'sequential') return agents.slice(0, -1).map((agent, index) => [agent.id, agents[index + 1].id]);
  if (pattern === 'parallel') return agents.slice(0, -1).map((agent) => [agent.id, agents[agents.length - 1].id]);
  if (pattern === 'loop') return [[agents[0]?.id, agents[1]?.id], [agents[1]?.id, agents[0]?.id]];
  return agents.slice(1).map((agent) => [agents[0].id, agent.id]);
}

export function NodeGraph({ pattern, agents, activeAgents }: NodeGraphProps) {
  const positions = new Map(agents.map((agent, index) => [agent.id, getLayout(pattern, index, agents.length)]));
  const edges = getEdges(pattern, agents);

  return (
    <div className="node-graph">
      <svg className="edge-layer" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
        {edges.map(([from, to]) => {
          const start = positions.get(from);
          const end = positions.get(to);
          if (!start || !end) return null;
          const active = activeAgents.has(from) || activeAgents.has(to);
          return (
            <line
              key={`${from}-${to}`}
              x1={start.left}
              y1={start.top}
              x2={end.left}
              y2={end.top}
              className={active ? 'edge active' : 'edge'}
            />
          );
        })}
      </svg>
      {agents.map((agent) => {
        const position = positions.get(agent.id)!;
        const active = activeAgents.has(agent.id);
        return (
          <div
            key={agent.id}
            className={active ? 'agent-node active' : 'agent-node'}
            style={{ left: `${position.left}%`, top: `${position.top}%`, borderColor: agent.color }}
          >
            {active && <span className="running-badge">Running</span>}
            <span className="node-orb" style={{ background: agent.color }} />
            <strong>{agent.name}</strong>
            <small>{agent.role}</small>
          </div>
        );
      })}
    </div>
  );
}
