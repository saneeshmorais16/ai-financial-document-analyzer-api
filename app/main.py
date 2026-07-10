from __future__ import annotations

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.analysis_service import analyze_text
from app.database import init_db
from app.schemas import AnalysisResponse, TextAnalysisRequest
from app.storage import get_analysis, list_analyses, save_analysis

app = FastAPI(title="AI Financial Document Analyzer API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def index() -> FileResponse:
    return FileResponse("app/static/index.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze/text", response_model=AnalysisResponse)
def analyze_text_endpoint(request: TextAnalysisRequest) -> dict:
    analysis = analyze_text(request.text, request.source_name)
    analysis_id = save_analysis(analysis)
    return {**analysis, "id": analysis_id}


@app.post("/analyze/file", response_model=AnalysisResponse)
async def analyze_file_endpoint(file: UploadFile = File(...)) -> dict:
    content = await file.read()
    text = content.decode("utf-8", errors="replace")
    analysis = analyze_text(text, file.filename or "uploaded_file")
    analysis_id = save_analysis(analysis)
    return {**analysis, "id": analysis_id}


@app.get("/analyses")
def analyses() -> list[dict]:
    return list_analyses()


@app.get("/analyses/{analysis_id}")
def analysis_detail(analysis_id: int) -> dict:
    return get_analysis(analysis_id)
