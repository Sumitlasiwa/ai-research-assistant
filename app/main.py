from fastapi import FastAPI, HTTPException
from pathlib import Path
from fastapi.responses import FileResponse, HTMLResponse
import html

from starlette.staticfiles import StaticFiles
from app.schemas.research import ResearchRequest
from app.workflows.research_workflow import conduct_research



app = FastAPI(
    title="AI Research Assistant",
    description="AI-powered web research and report generation",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Research Assistant is running"
    }


@app.post("/research")
def research(request: ResearchRequest):

    try:
        result = conduct_research(request.topic)
        return result

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


REPORTS_DIR = Path("reports").resolve()
ALLOWED_EXTENSIONS = {".md", ".pdf"}


@app.get("/reports", tags=["Reports"])
def list_reports():
    if not REPORTS_DIR.exists():
        return {"files": []}

    files = [
        file.name
        for file in sorted(REPORTS_DIR.iterdir())
        if file.is_file() and file.suffix.lower() in {".md", ".pdf"}
    ]

    return {"files": files}


@app.get("/reports/{filename}", tags=["Reports"])
def download_report(filename: str):
    # Only allow generated Markdown and PDF reports.
    if (
        Path(filename).name != filename
        or Path(filename).suffix not in {".md", ".pdf"}
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid report filename"
        )

    file_path = (REPORTS_DIR / filename).resolve()

    # Ensure the resolved path remains inside reports/.
    if REPORTS_DIR not in file_path.parents or not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    media_types = {
        ".md": "text/markdown",
        ".pdf": "application/pdf"
    }

    return FileResponse(
        path=file_path,
        media_type=media_types[file_path.suffix],
        filename=filename
    )