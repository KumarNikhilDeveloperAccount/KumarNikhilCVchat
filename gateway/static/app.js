const themes = {
  royal: {
    label: "Royal",
    bodyClass: "theme-royal",
    subtitle: "A polished dark presentation for Kumar Nikhil's AI Chat CV."
  },
  classic: {
    label: "Classic",
    bodyClass: "theme-classic",
    subtitle: "A clean light presentation for Kumar Nikhil's AI Chat CV."
  }
};

const quickPrompts = [
  "Where does he work?",
  "Where does he live?",
  "What does Kumar Nikhil do at DXC Technology?",
  "What are Kumar Nikhil's core skills?",
  "What certifications does Kumar Nikhil have?",
  "Tell me about Kumar Nikhil's education",
  "What internships has Kumar Nikhil done?",
  "Give me a recruiter summary of Kumar Nikhil"
];

const heroChips = [
  "Give me a recruiter summary of Kumar Nikhil",
  "What does Kumar Nikhil do at DXC Technology?",
  "What certifications does Kumar Nikhil have?"
];

const state = {
  theme: "royal",
  sending: false,
  knowledgeItems: [],
  libraryStatus: null,
  messages: [
    {
      role: "assistant",
      text: "I am Kumar Nikhil's Official AI CV Companion. Ask about his work at DXC Technology, skills, certifications, education, internships, languages, or contact details.",
      meta: ""
    }
  ]
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function escapeAttribute(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("\"", "&quot;");
}

function escapeJSString(value) {
  return String(value ?? "")
    .replaceAll("\\", "\\\\")
    .replaceAll("'", "\\'")
    .replaceAll("\n", "\\n")
    .replaceAll("\r", "");
}

function formatDate(value) {
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? String(value ?? "") : parsed.toLocaleString();
}

function formatLibraryCount(value) {
  return new Intl.NumberFormat().format(value || 0);
}

function parseFollowUps(text) {
  const lines = String(text || "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
  const prompts = [];
  const body = [];

  lines.forEach((line) => {
    const cleaned = line.replace(/^[-*]\s*/, "").trim();
    if (
      cleaned.endsWith("?") &&
      prompts.length < 3 &&
      /kumar|his|him|he|dxc|certification|skill|education|internship|language|contact|work|role/i.test(cleaned)
    ) {
      prompts.push(cleaned);
    } else {
      body.push(line);
    }
  });

  return {
    body: body.join("\n").trim() || text,
    prompts
  };
}

function renderMessages() {
  const chatLog = document.getElementById("chat-log");
  if (!chatLog) return;

  chatLog.innerHTML = state.messages
    .map((message, index) => {
      const parsed = message.role === "assistant" ? parseFollowUps(message.text) : { body: message.text, prompts: [] };
      return `
        <article class="bubble ${message.role} ${message.role === "assistant" ? "reveal" : ""}" style="animation-delay:${Math.min(index * 40, 240)}ms">
          <div class="bubble-top">
            <strong>${message.role === "assistant" ? "Kumar Nikhil AI CV" : "You"}</strong>
          </div>
          <p>${escapeHtml(parsed.body).replaceAll("\n", "<br />")}</p>
          ${parsed.prompts.length ? `
            <div class="follow-up-row">
              ${parsed.prompts.map((prompt) => `
                <button type="button" class="follow-up-chip" onclick="window.handleSuggestionClick('${escapeJSString(prompt)}')">
                  ${escapeHtml(prompt)}
                </button>
              `).join("")}
            </div>
          ` : ""}
          ${message.meta ? `<span class="meta">${escapeHtml(message.meta)}</span>` : ""}
        </article>
      `;
    })
    .join("");

  chatLog.scrollTop = chatLog.scrollHeight;
}

function renderKnowledge() {
  const knowledgeList = document.getElementById("knowledge-list");
  if (!knowledgeList) return;

  knowledgeList.innerHTML = state.knowledgeItems.length
    ? state.knowledgeItems.map((item) => `
      <article class="knowledge-card">
        <strong>${escapeHtml(item.title)}</strong>
        <p>${escapeHtml(item.content)}</p>
        <span class="meta">${escapeHtml((item.tags || []).join(", ") || item.source_kind || "profile-note")}</span>
      </article>
    `).join("")
    : `<div class="knowledge-empty">No extra profile notes saved yet.</div>`;
}

function renderShell() {
  document.body.dataset.theme = themes[state.theme].bodyClass;
  const app = document.getElementById("app");
  app.className = "shell";
  app.innerHTML = `
    <div class="ambient ambient-a"></div>
    <div class="ambient ambient-b"></div>
    <div class="app cv-app">
      <section class="hero">
        <div class="hero-main">
          <p class="eyebrow">Personalized AI Chat CV</p>
          <h1>Kumar Nikhil</h1>
          <div class="signature-line">
            <span class="signature-kicker">Signature Note</span>
            <strong>Architected by Kumar Nikhil, shaped for conversation.</strong>
          </div>
          <p class="subtitle">${themes[state.theme].subtitle} This assistant answers only from his profile, experience, credentials, and recruiter-facing details.</p>
          <div class="scene-badges">
            ${heroChips.map((item) => `
              <button type="button" class="scene-badge scene-action" onclick="window.handleSuggestionClick('${escapeJSString(item)}')">
                ${escapeHtml(item.replace("What ", "").replace("Give me a ", ""))}
              </button>
            `).join("")}
          </div>
        </div>
        <div class="hero-right">
          <p class="brand">Kumar Nikhil AI CV</p>
          <div class="theme-toggle">
            ${Object.entries(themes).map(([id, item]) => `
              <button type="button" class="theme-pill ${state.theme === id ? "active" : ""}" onclick="window.handleThemeSwitch('${id}')">
                ${item.label}
              </button>
            `).join("")}
          </div>
          ${state.libraryStatus ? `
            <div class="library-banner">
              <strong>${formatLibraryCount(state.libraryStatus.total_documents)} profile records</strong>
              <small>${formatDate(state.libraryStatus.last_updated)}</small>
            </div>
          ` : ""}
          <div class="profile-card">
            <span class="status-label">Ask About</span>
            <strong>Experience, skills, certifications, education, and contact</strong>
            <small>This is a dedicated profile assistant, not a general knowledge bot.</small>
          </div>
        </div>
      </section>

      <section class="content">
        <section class="chat-panel panel">
          <div class="panel-head">
            <div>
              <p class="eyebrow">Kumar Nikhil AI CV</p>
              <h2>Interactive Resume Chat</h2>
            </div>
            <span class="chip">${themes[state.theme].label} Mode</span>
          </div>

          <div class="status-row">
            <div class="status-card">
              <span class="status-label">Profile Scope</span>
              <strong>Kumar Nikhil only</strong>
              <small>Answers are constrained to the CV-backed profile knowledge.</small>
            </div>
            <div class="status-card">
              <span class="status-label">Conversation</span>
              <strong>${state.messages.length} entries</strong>
              <small>Pronoun-aware profile chat is active.</small>
            </div>
            <div class="status-card">
              <span class="status-label">Usage</span>
              <strong>Recruiters, hiring managers, interviewers</strong>
              <small>Designed to work cleanly on phone and desktop browsers.</small>
            </div>
          </div>

          ${state.libraryStatus ? `
            <div class="library-summary panel-inline">
              <strong>Knowledge Last Updated</strong>
              <span>${formatDate(state.libraryStatus.last_updated)}</span>
              <small>${escapeHtml(state.libraryStatus.headline || "")}</small>
            </div>
          ` : ""}

          <div class="suggestions">
            ${quickPrompts.map((item) => `
              <button type="button" class="suggestion-chip" onclick="window.handleSuggestionClick('${escapeJSString(item)}')">${escapeHtml(item)}</button>
            `).join("")}
          </div>

          <div id="typing-ribbon" class="typing-ribbon ${state.sending ? "active" : ""}">
            <span></span><span></span><span></span>
            <em>Kumar Nikhil AI CV is preparing the next answer...</em>
          </div>

          <div id="chat-log" class="chat-log"></div>

          <section class="chat-form" aria-label="Chat composer">
            <div class="composer-shell">
              <textarea id="draft" placeholder="Ask about Kumar Nikhil's profile. Example: Where does he work?" onkeydown="window.handleDraftKeydown(event)"></textarea>
              <div class="composer-actions">
                <button type="button" class="subtle-action" onclick="window.handleSurprisePrompt()">Try A Prompt</button>
                <button type="button" id="send-button" onclick="window.handleSendClick()" ${state.sending ? "disabled" : ""}>${state.sending ? "Thinking..." : "Ask"}</button>
              </div>
            </div>
          </section>
        </section>

        <aside class="stack">
          <section class="panel detail-panel">
            <div class="panel-head">
              <div>
                <p class="eyebrow">Profile Highlights</p>
                <h2>Quick View</h2>
              </div>
            </div>
            <div class="deck">
              <button type="button" class="deck-card" onclick="window.handleSuggestionClick('What does Kumar Nikhil do at DXC Technology?')">
                <span>Experience</span>
                <strong>Current responsibilities at DXC</strong>
              </button>
              <button type="button" class="deck-card" onclick="window.handleSuggestionClick('What are Kumar Nikhil\\'s strongest technical skills?')">
                <span>Skills</span>
                <strong>Technical strengths and tools</strong>
              </button>
              <button type="button" class="deck-card" onclick="window.handleSuggestionClick('List Kumar Nikhil\\'s certifications and education')">
                <span>Credentials</span>
                <strong>Certifications and education path</strong>
              </button>
            </div>
          </section>

          <section class="panel detail-panel">
            <div class="panel-head">
              <div>
                <p class="eyebrow">Profile Notes</p>
                <h2>Add More Context</h2>
              </div>
            </div>
            <form id="knowledge-form" class="knowledge-form" onsubmit="window.handleKnowledgeForm(event)">
              <input id="knowledge-title" class="knowledge-input" placeholder="Profile note title" />
              <textarea id="knowledge-content" placeholder="Add a recruiter note, portfolio detail, or interview talking point..."></textarea>
              <button type="submit">Save Note</button>
            </form>
            <div id="knowledge-list" class="knowledge-list"></div>
          </section>

          <section class="panel detail-panel">
            <div class="panel-head">
              <div>
                <p class="eyebrow">What To Ask</p>
                <h2>Conversation Ideas</h2>
              </div>
            </div>
            <ul class="list">
              <li>Ask where Kumar Nikhil works and what he does there</li>
              <li>Ask for certifications, education, skills, internships, or languages</li>
              <li>Ask for recruiter summaries and interview-oriented profile explanations</li>
              <li>Use pronouns naturally: he, his, and him refer to Kumar Nikhil</li>
            </ul>
          </section>
        </aside>
      </section>
    </div>
  `;

  renderMessages();
  renderKnowledge();
}

function populateDraft(text) {
  const draft = document.getElementById("draft");
  if (!draft) return;
  draft.value = text;
  draft.focus();
  draft.setSelectionRange(draft.value.length, draft.value.length);
}

async function handleSend() {
  const draft = document.getElementById("draft");
  if (!draft || state.sending) return;
  const text = draft.value.trim();
  if (!text) {
    draft.focus();
    return;
  }

  state.messages.push({ role: "user", text, meta: "" });
  draft.value = "";
  state.sending = true;
  renderShell();

  try {
    const response = await fetch("/v1/chat/respond", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: text,
        platform: "web",
        theme_context: state.theme,
        mode: "assist",
        user_id: "demo-user"
      })
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Request failed");
    }
    state.messages.push({
      role: "assistant",
      text: data.response,
      meta: ""
    });
  } catch (error) {
    state.messages.push({
      role: "assistant",
      text: "The request failed. Check that the CV backend services are running.",
      meta: ""
    });
  } finally {
    state.sending = false;
    renderShell();
  }
}

async function onKnowledgeSave(event) {
  event.preventDefault();
  const title = document.getElementById("knowledge-title");
  const content = document.getElementById("knowledge-content");
  const nextTitle = title.value.trim();
  const nextContent = content.value.trim();
  if (!nextTitle || !nextContent) return;

  const response = await fetch("/v1/chat/knowledge", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: "demo-user",
      title: nextTitle,
      content: nextContent,
      tags: ["profile-note", "kumar-nikhil"],
      source_kind: "ui"
    })
  });

  const data = await response.json();
  if (response.ok) {
    state.knowledgeItems.unshift(data.item);
    title.value = "";
    content.value = "";
    renderShell();
  }
}

async function bootstrapKnowledge() {
  const response = await fetch("/v1/chat/knowledge?user_id=demo-user");
  const data = await response.json();
  if (response.ok) {
    state.knowledgeItems = data.items || [];
    renderShell();
  }
}

async function bootstrapLibraryStatus() {
  const response = await fetch("/v1/chat/library/status?user_id=demo-user");
  const data = await response.json();
  if (response.ok) {
    state.libraryStatus = data;
    renderShell();
  }
}

window.handleSuggestionClick = function handleSuggestionClick(text) {
  populateDraft(text);
};

window.handleThemeSwitch = function handleThemeSwitch(themeId) {
  state.theme = themeId || "royal";
  renderShell();
};

window.handleSurprisePrompt = function handleSurprisePrompt() {
  const pick = quickPrompts[Math.floor(Math.random() * quickPrompts.length)];
  populateDraft(pick);
};

window.handleSendClick = function handleSendClick() {
  handleSend();
};

window.handleDraftKeydown = function handleDraftKeydown(event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    handleSend();
  }
};

window.handleKnowledgeForm = function handleKnowledgeForm(event) {
  onKnowledgeSave(event);
};

renderShell();
bootstrapKnowledge();
bootstrapLibraryStatus();
