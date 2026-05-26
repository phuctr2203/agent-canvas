import { useCallback, useEffect, useMemo, useState } from 'react';
import { getPatterns, simulate } from './api/client';
import { Header } from './components/Header';
import { LeftPanel } from './components/LeftPanel';
import { LogInspector } from './components/LogInspector';
import { NodeGraph } from './components/NodeGraph';
import { Agent, AgentPattern, Message, PatternConfig } from './types/agent';

const replayDelayMs = 450;

function wait(ms: number) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

export default function App() {
  const [patterns, setPatterns] = useState<PatternConfig[]>([]);
  const [selectedPattern, setSelectedPattern] = useState<AgentPattern>('single');
  const [agents, setAgents] = useState<Agent[]>([]);
  const [prompt, setPrompt] = useState('Explain how this orchestration pattern handles a product research task.');
  const [messages, setMessages] = useState<Message[]>([]);
  const [activeAgents, setActiveAgents] = useState<Set<string>>(new Set());
  const [activeMessageId, setActiveMessageId] = useState<string>();
  const [finalResult, setFinalResult] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState('');

  const selectedConfig = useMemo(
    () => patterns.find((pattern) => pattern.id === selectedPattern),
    [patterns, selectedPattern],
  );

  useEffect(() => {
    getPatterns()
      .then((configs) => {
        setPatterns(configs);
        const first = configs[0];
        if (first) {
          setSelectedPattern(first.id);
          setAgents(first.agents);
        }
      })
      .catch((caught: Error) => setError(caught.message));
  }, []);

  const handlePatternChange = useCallback(
    (pattern: AgentPattern) => {
      const config = patterns.find((item) => item.id === pattern);
      if (!config) return;
      setSelectedPattern(pattern);
      setAgents(config.agents);
      setMessages([]);
      setActiveAgents(new Set());
      setActiveMessageId(undefined);
      setFinalResult('');
      setError('');
    },
    [patterns],
  );

  const handleUpdateAgent = useCallback((agentId: string, updates: Partial<Agent>) => {
    setAgents((current) => current.map((agent) => (agent.id === agentId ? { ...agent, ...updates } : agent)));
  }, []);

  const handleRunSimulation = useCallback(async () => {
    setIsRunning(true);
    setMessages([]);
    setActiveAgents(new Set());
    setFinalResult('');
    setError('');

    try {
      const result = await simulate(selectedPattern, prompt, agents);
      for (const message of result.messages) {
        setActiveAgents(new Set(message.activeAgents));
        setActiveMessageId(message.id);
        setMessages((current) => [...current, message]);
        await wait(replayDelayMs);
      }
      setFinalResult(result.finalResult);
      setActiveAgents(new Set());
      setActiveMessageId(undefined);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : 'Simulation failed');
    } finally {
      setIsRunning(false);
    }
  }, [agents, prompt, selectedPattern]);

  return (
    <div className="app-shell">
      <Header patterns={patterns} selectedPattern={selectedPattern} onPatternChange={handlePatternChange} />

      {error && <div className="error-banner">{error}</div>}

      <main className="workspace">
        <LeftPanel
          agents={agents}
          prompt={prompt}
          isRunning={isRunning}
          finalResult={finalResult}
          onPromptChange={setPrompt}
          onRunSimulation={handleRunSimulation}
          onUpdateAgent={handleUpdateAgent}
        />

        <section className="right-panel">
          <div className="graph-card">
            <div className="section-title">
              <div>
                <p className="eyebrow">Visual Node Graph</p>
                <h2>{selectedConfig?.name ?? 'Loading pattern'}</h2>
              </div>
              <span>{agents.length} agents</span>
            </div>
            <NodeGraph pattern={selectedPattern} agents={agents} activeAgents={activeAgents} />
          </div>

          <div className="log-card">
            <div className="section-title">
              <div>
                <p className="eyebrow">Live Inspector Log</p>
                <h2>Agent communication</h2>
              </div>
              <span>{messages.length} events</span>
            </div>
            <LogInspector messages={messages} activeMessageId={activeMessageId} />
          </div>
        </section>
      </main>
    </div>
  );
}
