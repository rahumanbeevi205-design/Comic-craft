import os
from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from .schemas import PromptRequest
from .services import generate_comic
from .image_generator import generate_image
from .config import BASE_DIR

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
def generate(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):
    try:
        layout, pdf_path = generate_comic(
            prompt, character_name, setting, tone, art_style
        )
        return templates.TemplateResponse(
            "comic_preview.html",
            {"request": request, "layout": layout, "pdf_path": pdf_path}
        )
    except Exception as exc:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": str(exc)},
            status_code=500
        )

@router.post("/generate-comic/json")
def generate_json(data: PromptRequest):
    try:
        layout, pdf_path = generate_comic(
            data.prompt, data.character_name, data.setting,
            data.tone, data.art_style
        )
        return {"layout": layout, "pdf_path": pdf_path}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/download-pdf")
def download_pdf(path: str):
    if not path.startswith("/static/exports/"):
        raise HTTPException(status_code=400, detail="Invalid PDF path")
    full_path = os.path.join(BASE_DIR, path.lstrip("/").replace("/", os.sep))
    if not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(full_path, media_type="application/pdf",
                        filename=os.path.basename(full_path))

@router.get("/export-success", response_class=HTMLResponse)
def export_success(request: Request):
    return templates.TemplateResponse("export_success.html", {"request": request})

@router.get("/test-image")
def test_image(prompt: str = "a brave fox in an enchanted forest, comic book art"):
    return {"image_path": generate_image(prompt, 999, "Test Image")}
