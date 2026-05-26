import { AgentPattern, PatternConfig } from '../types/agent';

interface HeaderProps {
  patterns: PatternConfig[];
  selectedPattern: AgentPattern;
  onPatternChange: (pattern: AgentPattern) => void;
}

export function Header({ patterns, selectedPattern, onPatternChange }: HeaderProps) {
  return (
    <header className="app-header">
      <div>
        <p className="eyebrow">Agent Orchestration Lab</p>
        <h1>Pattern visualizer</h1>
      </div>
      <nav className="pattern-tabs" aria-label="Agent orchestration patterns">
        {patterns.map((pattern) => (
          <button
            key={pattern.id}
            className={pattern.id === selectedPattern ? 'pattern-tab active' : 'pattern-tab'}
            onClick={() => onPatternChange(pattern.id)}
            type="button"
          >
            <span>{pattern.name}</span>
            <small>{pattern.description}</small>
          </button>
        ))}
      </nav>
    </header>
  );
}
