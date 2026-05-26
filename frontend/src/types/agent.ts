export type AgentPattern = 'single' | 'sequential' | 'parallel' | 'loop' | 'coordinator';

export interface Agent {
  id: string;
  name: string;
  role: string;
  systemPrompt: string;
  color: string;
}

export interface PatternConfig {
  id: AgentPattern;
  name: string;
  description: string;
  agents: Agent[];
}

export type MessageType = 'thinking' | 'response' | 'routing' | 'critique' | 'received';

export interface Message {
  id: string;
  timestamp: number;
  fromAgent: string;
  toAgent?: string;
  type: MessageType;
  content: string;
  receivedFrom?: string;
  activeAgents: string[];
}

export interface SimulationResult {
  messages: Message[];
  finalResult: string;
}
