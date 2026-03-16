from __future__ import annotations

import json
from pathlib import Path

from ..models import ThemeGenerateRequest, ThemeGenerateResponse


LOCAL_THEME_FILE = Path(__file__).resolve().parents[1] / "data" / "themes.json"
ROOT_THEME_FILE = Path(__file__).resolve().parents[3] / "shared" / "themes.json"


def list_themes() -> list[dict]:
    theme_file = ROOT_THEME_FILE if ROOT_THEME_FILE.exists() else LOCAL_THEME_FILE
    return json.loads(theme_file.read_text(encoding="utf-8"))


def generate_theme_variant(payload: ThemeGenerateRequest) -> ThemeGenerateResponse:
    themes = {theme["theme_id"]: theme for theme in list_themes()}
    base = themes.get(payload.base_theme, themes["elegant"])
    tokens = dict(base)
    tokens["label"] = f"{base['label']} / {payload.intent.title()}"
    tokens["theme_id"] = f"{base['theme_id']}-{payload.intent.lower().replace(' ', '-')}"
    return ThemeGenerateResponse(theme_id=tokens["theme_id"], tokens=tokens)
