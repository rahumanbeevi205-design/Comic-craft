from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import router
from .config import BASE_DIR, PANEL_DIR, EXPORT_DIR
import os

os.makedirs(PANEL_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="AI powered comic story generator using Gemini and Stable Diffusion.",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "healthy", "application": "ComicCraft", "version": "1.0.0"}
