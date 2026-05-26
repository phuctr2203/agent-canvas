import { Agent, AgentPattern, PatternConfig, SimulationResult } from '../types/agent';

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000';

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function getPatterns(): Promise<PatternConfig[]> {
  return request<PatternConfig[]>('/api/patterns');
}

export function simulate(pattern: AgentPattern, prompt: string, agents: Agent[]): Promise<SimulationResult> {
  return request<SimulationResult>('/api/simulate', {
    method: 'POST',
    body: JSON.stringify({ pattern, prompt, agents }),
  });
}
