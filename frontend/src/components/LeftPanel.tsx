import { FormEvent, useState } from 'react';
import { Agent } from '../types/agent';
import { MarkdownContent } from './MarkdownContent';

interface LeftPanelProps {
  agents: Agent[];
  prompt: string;
  isRunning: boolean;
  finalResult: string;
  onPromptChange: (prompt: string) => void;
  onRunSimulation: () => void;
  onUpdateAgent: (agentId: string, updates: Partial<Agent>) => void;
}

export function LeftPanel({
  agents,
  prompt,
  isRunning,
  finalResult,
  onPromptChange,
  onRunSimulation,
  onUpdateAgent,
}: LeftPanelProps) {
  const [expandedAgent, setExpandedAgent] = useState<string | null>(agents[0]?.id ?? null);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onRunSimulation();
  }

  return (
    <aside className="left-panel">
      <form className="prompt-card" onSubmit={handleSubmit}>
        <label htmlFor="prompt">Input prompt</label>
        <textarea
          id="prompt"
          value={prompt}
          onChange={(event) => onPromptChange(event.target.value)}
          placeholder="Ask agents to solve, research, write, design, or route something..."
          disabled={isRunning}
        />
        <button className="run-button" type="submit" disabled={isRunning || !prompt.trim()}>
          {isRunning ? 'Running simulation...' : 'Run orchestration'}
        </button>
      </form>

      <section className="panel-section">
        <h2>Agents</h2>
        <div className="agent-list">
          {agents.map((agent) => (
            <article key={agent.id} className="agent-card">
              <button
                type="button"
                className="agent-summary"
                onClick={() => setExpandedAgent(expandedAgent === agent.id ? null : agent.id)}
              >
                <span className="agent-dot" style={{ background: agent.color }} />
                <span>
                  <strong>{agent.name}</strong>
                  <small>{agent.role}</small>
                </span>
              </button>
              {expandedAgent === agent.id && (
                <div className="agent-editor">
                  <label>
                    Name
                    <input
                      value={agent.name}
                      disabled={isRunning}
                      onChange={(event) => onUpdateAgent(agent.id, { name: event.target.value })}
                    />
                  </label>
                  <label>
                    System prompt
                    <textarea
                      value={agent.systemPrompt}
                      disabled={isRunning}
                      onChange={(event) => onUpdateAgent(agent.id, { systemPrompt: event.target.value })}
                    />
                  </label>
                </div>
              )}
            </article>
          ))}
        </div>
      </section>

      {finalResult && (
        <section className="final-card">
          <h2>Final result</h2>
          <MarkdownContent content={finalResult} />
        </section>
      )}
    </aside>
  );
}
