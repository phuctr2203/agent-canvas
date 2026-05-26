import { Message } from '../types/agent';
import { MarkdownContent } from './MarkdownContent';

interface LogInspectorProps {
  messages: Message[];
  activeMessageId?: string;
}

export function LogInspector({ messages, activeMessageId }: LogInspectorProps) {
  return (
    <section className="log-inspector">
      {messages.length === 0 ? (
        <div className="empty-state">Run a prompt to watch agent messages appear here.</div>
      ) : (
        messages.map((message) => (
          <article
            key={message.id}
            className={`log-row ${message.type}${message.id === activeMessageId ? ' active' : ''}`}
          >
            <div className="log-meta">
              <span className="message-type">{message.type}</span>
              <strong>{message.fromAgent}</strong>
              {message.toAgent && <span>→ {message.toAgent}</span>}
              {message.receivedFrom && <span>from {message.receivedFrom}</span>}
            </div>
            <MarkdownContent content={message.content} />
          </article>
        ))
      )}
    </section>
  );
}
