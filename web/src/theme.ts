import type { Theme } from "./types";
import themes from "./themes.json";

export const availableThemes = themes as Theme[];

export function applyTheme(theme: Theme) {
  const root = document.documentElement;
  root.style.setProperty("--color-primary", theme.colors.primary);
  root.style.setProperty("--color-secondary", theme.colors.secondary);
  root.style.setProperty("--color-accent", theme.colors.accent);
  root.style.setProperty("--color-bg-base", theme.colors.bg_base);
  root.style.setProperty("--color-bg-elevated", theme.colors.bg_elevated);
  root.style.setProperty("--color-text-main", theme.colors.text_main);
  root.style.setProperty("--color-text-muted", theme.colors.text_muted);
  root.style.setProperty("--font-heading", theme.typography.font_heading);
  root.style.setProperty("--font-body", theme.typography.font_body);
  root.style.setProperty("--radius-sm", theme.shape.radius_sm);
  root.style.setProperty("--radius-md", theme.shape.radius_md);
  root.style.setProperty("--radius-lg", theme.shape.radius_lg);
  root.style.setProperty("--shadow-card", theme.effects.shadow);
  root.style.setProperty("--glow-effect", theme.effects.glow);
  root.style.setProperty("--motion-fast", theme.motion.duration_fast);
  root.style.setProperty("--motion-base", theme.motion.duration_base);
  root.style.setProperty("--motion-curve", theme.motion.curve);
}
