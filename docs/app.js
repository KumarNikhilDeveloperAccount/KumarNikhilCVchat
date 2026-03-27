const profile = {
  headline: "Kumar Nikhil's Personalized AI Chat CV",
  identity: {
    name: "Kumar Nikhil",
    location: "Palam, New Delhi, India",
    phone: "9315600875",
    email: "nkashyapnikhilnk@gmail.com"
  },
  summary:
    "IT Service Management and Infrastructure professional with strong hands-on experience across Change Management, Incident Management, and Service Request operations in large-scale enterprise environments. Exposure includes Windows server operations, patch management, privileged access management, virtualization, storage platforms, KT delivery, cross-training, client-facing knowledge transfer, and major project transitions with an ITIL-aligned governance mindset.",
  experience: {
    company: "DXC Technology",
    role: "Analyst III, Infrastructure Services",
    duration: "July 2022 - Present",
    highlights: [
      "Incident Management aligned to SLA and OLA commitments",
      "Change Management and service requests using ServiceNow and HPE Service Manager",
      "RFC validation before CAB and eCAB approvals",
      "Coordination with infrastructure, application, network, security, storage, and vendor teams",
      "MFSA patching, SCCM patch coordination, and Windows Server troubleshooting",
      "Active Directory, BeyondTrust PAM, VMware vSphere, and NetApp ONTAP support",
      "CMDB maintenance, reporting, KT delivery, and client transition support"
    ]
  },
  skills: [
    "Incident Management",
    "Change Management",
    "Service Request Management",
    "ITIL Framework",
    "ServiceNow",
    "HPE Service Manager (HPSM)",
    "Windows Server Administration and Troubleshooting",
    "Active Directory",
    "RBAC",
    "User Access Management",
    "Group Policies",
    "CAB and eCAB Governance",
    "MFSA Patching",
    "SCCM Patch Coordination",
    "BeyondTrust PAM",
    "VMware vSphere",
    "NetApp ONTAP",
    "CMDB and Configuration Management",
    "SLA, OLA, KPI Tracking",
    "Operational Reporting",
    "Knowledge Transfer",
    "Client Transition and Handover",
    "Audit and Compliance Support",
    "Program Management Support"
  ],
  education: [
    "Central Board of Secondary Education - Secondary (10th Standard) (2018-2019)",
    "CBSE Skill India - Information Technology (NSQF Level-2) (2018-2019)",
    "Ambedkar Institute of Technology, New Delhi - Diploma in Electronics Engineering (2019-2022)",
    "Mangalayatan University, Aligarh - B.Tech (WILP) in Computer Science and Engineering (2024-2027)"
  ],
  certifications: [
    "Oracle Certified Foundations Associate",
    "AWS Certified Cloud Practitioner",
    "Oracle Cloud Data Management 2023 Certified Foundations Associate",
    "Business Intelligence Professional Foundations Certification (BIFPC)",
    "Aviatrix Certified Engineer - Multicloud Network Associate"
  ],
  internships: [
    "Student Partner - IIT Roorkee and Cognizance (Techfest 2021)",
    "Campus Ambassador - Lyriclious (Golden Level Internship, July 2021)"
  ],
  languages: ["English - Fluent", "Hindi - Fluent"]
};

const themes = {
  royal: {
    label: "Royal",
    bodyClass: "theme-royal",
    subtitle: "A polished dark presentation for Kumar Nikhil's public AI Chat CV."
  },
  classic: {
    label: "Classic",
    bodyClass: "theme-classic",
    subtitle: "A clean light presentation for Kumar Nikhil's public AI Chat CV."
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
  notes: loadNotes(),
  messages: [
    {
      role: "assistant",
      text: "I am Kumar Nikhil's Official AI CV Companion. Ask about his work at DXC Technology, skills, certifications, education, internships, languages, or contact details."
    }
  ]
};

function loadNotes() {
  try {
    return JSON.parse(localStorage.getItem("kumar-nikhil-cv-notes") || "[]");
  } catch {
    return [];
  }
}

function saveNotes() {
  localStorage.setItem("kumar-nikhil-cv-notes", JSON.stringify(state.notes));
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function escapeJSString(value) {
  return String(value ?? "")
    .replaceAll("\\", "\\\\")
    .replaceAll("'", "\\'")
    .replaceAll("\n", "\\n")
    .replaceAll("\r", "");
}

function formatDate(value) {
  return new Date(value).toLocaleString();
}

function parseFollowUps(text) {
  const lines = String(text || "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
  const prompts = [];
  const body = [];

  lines.forEach((line) => {
    if (line.endsWith("?") && prompts.length < 3) {
      prompts.push(line);
    } else {
      body.push(line);
    }
  });

  return { body: body.join("\n").trim() || text, prompts };
}

function normalize(message) {
  return message.trim().replace(/^(hey|hi|hello)[,\s]+/i, "").trim();
}

function resolvePronouns(message) {
  let result = ` ${message} `;
  result = result.replace(/\bhe\b/gi, "Kumar Nikhil");
  result = result.replace(/\bhim\b/gi, "Kumar Nikhil");
  result = result.replace(/\bhis\b/gi, "Kumar Nikhil's");
  return result.trim();
}

function finalize(answer, prompts) {
  return `${answer}\n\n${prompts.slice(0, 3).join("\n")}`;
}

function answerFor(message) {
  const lowered = normalize(resolvePronouns(message)).toLowerCase();

  if (/(where.*live|where.*based|where.*from|reside|stay)/.test(lowered)) {
    return finalize(
      `Kumar Nikhil lives in ${profile.identity.location}.`,
      [
        "What is his current role at DXC Technology?",
        "Give me a recruiter-style summary of his profile.",
        "What certifications does he have?"
      ]
    );
  }

  if (/(contact|phone|email|address)/.test(lowered)) {
    return finalize(
      `Kumar Nikhil is based in ${profile.identity.location}. His CV lists phone ${profile.identity.phone} and email ${profile.identity.email}. This makes it easy for recruiters and hiring teams to reach him directly.`,
      [
        "What are his current role and responsibilities?",
        "What are his core skills?",
        "How do his certifications strengthen his profile?"
      ]
    );
  }

  if (/(where.*work|company|employer|working)/.test(lowered)) {
    return finalize(
      `Kumar Nikhil currently works at ${profile.experience.company} as ${profile.experience.role}, and he has been in that role since ${profile.experience.duration}. His work sits at the intersection of IT service operations, infrastructure coordination, and governance-heavy enterprise support.`,
      [
        "Give me the full technical deep-dive with step-by-step process.",
        "What tools and platforms does he work with?",
        "Summarize his DXC role for a recruiter."
      ]
    );
  }

  if (/(dxc|responsibilit|experience|role|job|itsm|infrastructure|what does kumar nikhil do)/.test(lowered)) {
    return finalize(
      `Kumar Nikhil works in a role where stability, control, and response quality matter every day. At ${profile.experience.company}, he handles Incident Management, Change Management, and Service Requests across enterprise environments using tools like ServiceNow and HPE Service Manager. He validates RFCs before CAB and eCAB decisions, coordinates across technical teams, supports patching and Windows Server troubleshooting, and helps keep production changes controlled and reliable.`,
      [
        "How does he handle Change Management from RFC to PIR?",
        "Tell me more about his patching, Windows Server, and access management work.",
        "What tools and platforms does he work with?"
      ]
    );
  }

  if (/(certification|certified|aws|oracle|aviatrix|bifpc)/.test(lowered)) {
    return finalize(
      `Kumar Nikhil's certifications are: ${profile.certifications.join("; ")}. These credentials strengthen his profile by showing breadth across cloud, data, networking, and business intelligence foundations, even while his core work remains strongly infrastructure and service-operations focused.`,
      [
        "How do his AWS and Oracle certifications support his profile?",
        "Tell me about his education path too.",
        "Give me a concise recruiter summary that includes these credentials."
      ]
    );
  }

  if (/(education|study|degree|college|university|diploma)/.test(lowered)) {
    return finalize(
      `Kumar Nikhil's education includes: ${profile.education.join("; ")}. His education path shows a practical progression from early IT foundations to electronics engineering and then into Computer Science and Engineering, which supports the structured troubleshooting and systems thinking visible in his current work.`,
      [
        "How does his Diploma in Electronics Engineering connect to his infrastructure work?",
        "Tell me about his internships and early career exposure.",
        "How does his education support his current DXC role?"
      ]
    );
  }

  if (/(skill|skills|technolog|tools|strengths)/.test(lowered)) {
    return finalize(
      `Kumar Nikhil's core skills include: ${profile.skills.join("; ")}. His profile is especially strong because these skills connect process discipline with infrastructure execution, making him a strong fit for enterprise support environments where control, reliability, and technical ownership all matter together.`,
      [
        "Connect these skills to his daily responsibilities at DXC Technology.",
        "Explain his ITSM and infrastructure strengths in more depth.",
        "Which certifications align best with these skills?"
      ]
    );
  }

  if (/(internship|training|student partner|campus ambassador)/.test(lowered)) {
    return finalize(
      `Kumar Nikhil's trainings and internships include: ${profile.internships.join("; ")}. These early experiences highlight communication, outreach, coordination, and representation skills that later support the client-facing and KT-heavy parts of his professional profile.`,
      [
        "How do these early experiences connect to his current DXC role?",
        "Tell me about his education journey next.",
        "Give me a broader summary of his professional profile."
      ]
    );
  }

  if (/(language|languages|speak)/.test(lowered)) {
    return finalize(
      `Kumar Nikhil is fluent in ${profile.languages.join(" and ")}. That supports day-to-day collaboration, KT sessions, reporting, and smoother communication in professional environments.`,
      [
        "Show me his contact details too.",
        "Give me a recruiter summary of his overall profile.",
        "Tell me about his internships and early experience."
      ]
    );
  }

  if (/(recruiter summary|profile summary|introduce|career summary|who is kumar|about kumar nikhil|profile)/.test(lowered)) {
    return finalize(
      `Kumar Nikhil is an IT Service Management and Infrastructure professional currently working at ${profile.experience.company} as ${profile.experience.role}. He brings hands-on experience in incident management, change management, service requests, Windows Server support, patch coordination, access workflows, VMware, NetApp, CMDB operations, and ITIL-aligned service governance. His profile stands out because it combines technical operations with discipline, cross-team coordination, and client-facing knowledge transfer.`,
      [
        "Break down his DXC responsibilities in more detail.",
        "Tell me about his certifications and technical strengths.",
        "Give me a compact 3-line version for recruiter screening."
      ]
    );
  }

  return (
    "That specific detail isn't in Kumar's CV. Instead, you can ask about his current role at DXC Technology, his certifications, or his core skills.\n\n" +
    "What are his DXC responsibilities?\n" +
    "What certifications does he have?\n" +
    "What are his strongest technical skills?"
  );
}

function renderMessages() {
  const chatLog = document.getElementById("chat-log");
  chatLog.innerHTML = state.messages.map((message, index) => {
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
              <button type="button" class="follow-up-chip" onclick="window.handleSuggestionClick('${escapeJSString(prompt)}')">${escapeHtml(prompt)}</button>
            `).join("")}
          </div>
        ` : ""}
      </article>
    `;
  }).join("");
  chatLog.scrollTop = chatLog.scrollHeight;
}

function renderNotes() {
  const list = document.getElementById("knowledge-list");
  if (!state.notes.length) {
    list.innerHTML = `<div class="knowledge-empty">No profile notes saved in this browser yet.</div>`;
    return;
  }
  list.innerHTML = state.notes.map((item) => `
    <article class="knowledge-card">
      <strong>${escapeHtml(item.title)}</strong>
      <p>${escapeHtml(item.content)}</p>
      <span class="meta">${escapeHtml(item.timestamp)}</span>
    </article>
  `).join("");
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
          <p class="eyebrow">Public AI Chat CV</p>
          <h1>Kumar Nikhil</h1>
          <div class="signature-line">
            <span class="signature-kicker">Signature Note</span>
            <strong>Architected by Kumar Nikhil, shaped for conversation.</strong>
          </div>
          <p class="subtitle">${themes[state.theme].subtitle} This public version runs entirely in the browser and answers only from Kumar Nikhil's CV-backed profile.</p>
          <div class="scene-badges">
            ${heroChips.map((item) => `<button type="button" class="scene-badge scene-action" onclick="window.handleSuggestionClick('${escapeJSString(item)}')">${escapeHtml(item.replace("What ", "").replace("Give me a ", ""))}</button>`).join("")}
          </div>
        </div>
        <div class="hero-right">
          <p class="brand">Kumar Nikhil AI CV</p>
          <div class="theme-toggle">
            ${Object.entries(themes).map(([id, item]) => `<button type="button" class="theme-pill ${state.theme === id ? "active" : ""}" onclick="window.handleThemeSwitch('${id}')">${item.label}</button>`).join("")}
          </div>
          <div class="library-banner">
            <strong>Public browser edition</strong>
            <small>${formatDate(Date.now())}</small>
          </div>
          <div class="profile-card">
            <span class="status-label">Ask About</span>
            <strong>Experience, skills, certifications, education, internships, languages, and contact</strong>
            <small>No sign-in. No install. Just one link and a browser.</small>
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
              <small>Answers stay grounded in his published CV details.</small>
            </div>
            <div class="status-card">
              <span class="status-label">Conversation</span>
              <strong>${state.messages.length} entries</strong>
              <small>Pronoun-aware profile chat is active.</small>
            </div>
            <div class="status-card">
              <span class="status-label">Access</span>
              <strong>Phone and desktop ready</strong>
              <small>This public build runs fully in the browser.</small>
            </div>
          </div>

          <div class="suggestions">
            ${quickPrompts.map((item) => `<button type="button" class="suggestion-chip" onclick="window.handleSuggestionClick('${escapeJSString(item)}')">${escapeHtml(item)}</button>`).join("")}
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
              <button type="button" class="deck-card" onclick="window.handleSuggestionClick('What are Kumar Nikhil\\'s core skills?')">
                <span>Skills</span>
                <strong>Technical strengths and tools</strong>
              </button>
              <button type="button" class="deck-card" onclick="window.handleSuggestionClick('What certifications does Kumar Nikhil have?')">
                <span>Credentials</span>
                <strong>Certifications and education path</strong>
              </button>
            </div>
          </section>

          <section class="panel detail-panel">
            <div class="panel-head">
              <div>
                <p class="eyebrow">Profile Notes</p>
                <h2>Save Browser Notes</h2>
              </div>
            </div>
            <form id="notes-form" class="knowledge-form" onsubmit="window.handleNoteSave(event)">
              <input id="note-title" class="knowledge-input" placeholder="Note title" />
              <textarea id="note-content" placeholder="Save a recruiter note or talking point in this browser..."></textarea>
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
  renderNotes();
}

function populateDraft(text) {
  const draft = document.getElementById("draft");
  if (!draft) return;
  draft.value = text;
  draft.focus();
  draft.setSelectionRange(draft.value.length, draft.value.length);
}

function handleSend() {
  const draft = document.getElementById("draft");
  if (!draft || state.sending) return;
  const text = draft.value.trim();
  if (!text) {
    draft.focus();
    return;
  }

  state.messages.push({ role: "user", text });
  draft.value = "";
  state.sending = true;
  renderShell();

  window.setTimeout(() => {
    state.messages.push({ role: "assistant", text: answerFor(text) });
    state.sending = false;
    renderShell();
  }, 280);
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

window.handleNoteSave = function handleNoteSave(event) {
  event.preventDefault();
  const title = document.getElementById("note-title");
  const content = document.getElementById("note-content");
  if (!title.value.trim() || !content.value.trim()) return;
  state.notes.unshift({
    title: title.value.trim(),
    content: content.value.trim(),
    timestamp: formatDate(Date.now())
  });
  title.value = "";
  content.value = "";
  saveNotes();
  renderShell();
};

renderShell();
