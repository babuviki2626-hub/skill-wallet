from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.services.comic_service import generate_comic
from app.services.exporters import export_comic_pdf


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):
    comic = await generate_comic(
        story_prompt=story_prompt,
        character_name=character_name,
        setting=setting,
        tone=tone,
        art_style=art_style
    )

    return templates.TemplateResponse(
        "comic_preview.html",
        {
            "request": request,
            "comic": comic
        }
    )


@router.post("/generate-comic/json")
async def generate_comic_json(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str
):
    comic = await generate_comic(
        story_prompt=story_prompt,
        character_name=character_name,
        setting=setting,
        tone=tone,
        art_style=art_style
    )

    return JSONResponse(content=comic)


@router.post("/export-success", response_class=HTMLResponse)
async def export_success(
    request: Request,
    comic_data: str = Form(...)
):
    pdf_path = export_comic_pdf(comic_data)

    return templates.TemplateResponse(
        "export_success.html",
        {
            "request": request,
            "pdf_path": pdf_path
        }
    )


@router.get("/test-image")
async def test_image():
    return {
        "status": "success",
        "message": "Image generation endpoint is working."
    }