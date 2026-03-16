from fastapi import APIRouter

from ..models import ThemeGenerateRequest, ThemeGenerateResponse
from ..services.themes import generate_theme_variant, list_themes

router = APIRouter()


@router.get("/")
def get_themes() -> dict:
    return {"themes": list_themes()}


@router.post("/generate", response_model=ThemeGenerateResponse)
def generate(payload: ThemeGenerateRequest) -> ThemeGenerateResponse:
    return generate_theme_variant(payload)

