import type { ChatResponse, Theme } from "./types";

const gatewayUrl = import.meta.env.VITE_GATEWAY_URL || "http://localhost:8080";

export async function sendMessage(message: string, themeContext: string): Promise<ChatResponse> {
  const response = await fetch(`${gatewayUrl}/v1/chat/respond`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      platform: "web",
      theme_context: themeContext,
      mode: "standard",
      user_id: "demo-user"
    })
  });

  if (!response.ok) {
    throw new Error("Chat request failed");
  }

  return response.json();
}

export async function fetchThemes(): Promise<Theme[]> {
  const response = await fetch(`${gatewayUrl}/v1/themes`);
  if (!response.ok) {
    throw new Error("Theme fetch failed");
  }

  const data = await response.json();
  return data.themes;
}

