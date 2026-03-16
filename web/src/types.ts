export type Theme = {
  theme_id: string;
  label: string;
  colors: {
    primary: string;
    secondary: string;
    accent: string;
    bg_base: string;
    bg_elevated: string;
    text_main: string;
    text_muted: string;
  };
  typography: {
    font_heading: string;
    font_body: string;
    scale: number;
  };
  shape: {
    radius_sm: string;
    radius_md: string;
    radius_lg: string;
  };
  effects: {
    shadow: string;
    glow: string;
  };
  motion: {
    duration_fast: string;
    duration_base: string;
    curve: string;
  };
};

export type ChatResponse = {
  message_id: string;
  model_used: string;
  response: string;
  memory_used: boolean;
  theme_hint: string;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
  };
  retrieved_memories: Array<{
    source: string;
    trust: number;
    text: string;
  }>;
};

