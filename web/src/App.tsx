import { FormEvent, useEffect, useState } from "react";

import { fetchThemes, sendMessage } from "./api";
import { applyTheme, availableThemes } from "./theme";
import type { ChatResponse, Theme } from "./types";

type Message = {
  role: "user" | "assistant";
  text: string;
  meta?: string;
};

const bootMessage =
  "I am the Nikhil-Bot, your autonomous agent within the Nikhil Ecosystem.";

export default function App() {
  const [themes, setThemes] = useState<Theme[]>(availableThemes);
  const [currentTheme, setCurrentTheme] = useState<Theme>(availableThemes[2]);
  const [draft, setDraft] = useState("");
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      text: `${bootMessage} Ask me to plan, reason, remember preferences, or switch the UI skin.`,
      meta: "Model router ready"
    }
  ]);

  useEffect(() => {
    applyTheme(currentTheme);
  }, [currentTheme]);

  useEffect(() => {
    let active = true;
    fetchThemes()
      .then((fetched) => {
        if (!active || !fetched.length) return;
        setThemes(fetched);
        setCurrentTheme(fetched.find((theme) => theme.theme_id === "elegant") || fetched[0]);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    const next = draft.trim();
    if (!next || sending) return;

    setDraft("");
    setSending(true);
    setMessages((current) => [...current, { role: "user", text: next }]);

    try {
      const response = await sendMessage(next, currentTheme.theme_id);
      const hintTheme = themes.find((theme) => theme.theme_id === response.theme_hint);
      if (hintTheme) {
        setCurrentTheme(hintTheme);
      }
      setMessages((current) => [...current, assistantMessageFromResponse(response)]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          text: "The request failed. Start the gateway and AI engine, then retry.",
          meta: "Gateway unavailable"
        }
      ]);
    } finally {
      setSending(false);
    }
  }

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-card">
          <p className="eyebrow">Booting Nikhil-OS</p>
          <h1>Nikhil-OS: Architected by Kumar Nikhil.</h1>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[var(--color-bg-base)] text-[var(--color-text-main)]">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col gap-6 px-4 py-6 md:px-8">
        <header className="hero-panel">
          <div>
            <p className="eyebrow">Cross-Platform AI Ecosystem</p>
            <h1 className="text-4xl md:text-6xl">Nikhil-OS</h1>
            <p className="hero-copy">
              Persistent memory, multi-model routing, and a shape-shifting interface driven by user intent.
            </p>
          </div>
          <div className="hero-side">
            <p className="brand-line">Nikhil-OS: Architected by Kumar Nikhil.</p>
            <select
              className="theme-select"
              value={currentTheme.theme_id}
              onChange={(event) => {
                const selected = themes.find((theme) => theme.theme_id === event.target.value);
                if (selected) setCurrentTheme(selected);
              }}
            >
              {themes.map((theme) => (
                <option key={theme.theme_id} value={theme.theme_id}>
                  {theme.label}
                </option>
              ))}
            </select>
          </div>
        </header>

        <main className="grid flex-1 gap-6 lg:grid-cols-[1.2fr_0.8fr]">
          <section className="panel">
            <div className="panel-header">
              <div>
                <p className="eyebrow">Nikhil-Bot</p>
                <h2>Adaptive Chat</h2>
              </div>
              <span className="capsule">{currentTheme.label}</span>
            </div>

            <div className="chat-log">
              {messages.map((message, index) => (
                <article key={`${message.role}-${index}`} className={`bubble ${message.role}`}>
                  <p>{message.text}</p>
                  {message.meta ? <span>{message.meta}</span> : null}
                </article>
              ))}
            </div>

            <form className="chat-form" onSubmit={onSubmit}>
              <textarea
                className="chat-input"
                placeholder="Ask for a launch plan, switch themes, or test memory..."
                rows={3}
                value={draft}
                onChange={(event) => setDraft(event.target.value)}
              />
              <button className="send-button" type="submit" disabled={sending}>
                {sending ? "Thinking..." : "Send"}
              </button>
            </form>
          </section>

          <aside className="stack">
            <section className="panel">
              <div className="panel-header">
                <div>
                  <p className="eyebrow">Skin-Shifter</p>
                  <h2>Theme DNA</h2>
                </div>
              </div>
              <ul className="token-list">
                <li>Primary: {currentTheme.colors.primary}</li>
                <li>Accent: {currentTheme.colors.accent}</li>
                <li>Heading Font: {currentTheme.typography.font_heading}</li>
                <li>Motion: {currentTheme.motion.duration_base}</li>
              </ul>
            </section>

            <section className="panel">
              <div className="panel-header">
                <div>
                  <p className="eyebrow">Operating Model</p>
                  <h2>MVP Stack</h2>
                </div>
              </div>
              <ul className="token-list">
                <li>Gateway: Go</li>
                <li>AI Engine: FastAPI</li>
                <li>Realtime: Node.js SSE</li>
                <li>Client: React + Tailwind</li>
                <li>Memory: mock-ready, RAG-compatible</li>
              </ul>
            </section>
          </aside>
        </main>
      </div>
    </div>
  );
}

function assistantMessageFromResponse(response: ChatResponse): Message {
  const memorySources = response.retrieved_memories.map((memory) => memory.source).join(", ") || "none";
  return {
    role: "assistant",
    text: response.response,
    meta: `Model: ${response.model_used} | Memory: ${memorySources} | Tokens: ${response.usage.prompt_tokens}/${response.usage.completion_tokens}`
  };
}

