
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.schemas.research import ResearchRequest
from app.workflows.research_graph import conduct_research_graph


app = FastAPI(
    title="AI Research Assistant",
    description="AI-powered web research and report generation",
    version="1.0.0",
)


REPORTS_DIR = Path("reports").resolve()
ALLOWED_EXTENSIONS = {".md", ".pdf"}


@app.get("/")
def root():
    return {"message": "AI Research Assistant is running"}


@app.post(
    "/research",
    summary="Generate a research report",
    description="Research a topic and generate Markdown and PDF reports.",
)
def research(request: ResearchRequest):
    try:
        result = conduct_research_graph(request.topic)

        return {
            "topic": result["topic"],
            "plan": result["plan"],
            "total_sources": len(result["sources"]),
            "sources": result["sources"],
            "report": result["report"],
            "review": result["llm_review"],
            "status": result["status"],
            "num_research_revisions": result["research_revision_count"],
            "num_writing_revisions": result["writing_revision_count"],
            "additional_queries": result.get("additional_queries", []),
            "report_urls": {
                "markdown": f"/reports/{Path(result['report_path']).name}",
                "pdf": f"/reports/{Path(result['pdf_path']).name}",
            },
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc


@app.get("/reports", tags=["Reports"])
def list_reports():
    if not REPORTS_DIR.exists():
        return {"files": []}

    files = [
        file.name
        for file in sorted(REPORTS_DIR.iterdir())
        if file.is_file()
        and file.suffix.lower() in ALLOWED_EXTENSIONS
    ]

    return {"files": files}


@app.get("/reports/{filename}", tags=["Reports"])
def download_report(filename: str):
    if (
        Path(filename).name != filename
        or Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid report filename",
        )

    file_path = (REPORTS_DIR / filename).resolve()

    if REPORTS_DIR not in file_path.parents or not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Report not found",
        )

    media_types = {
        ".md": "text/markdown",
        ".pdf": "application/pdf",
    }

    return FileResponse(
        path=file_path,
        media_type=media_types[file_path.suffix.lower()],
        filename=filename,
    )
