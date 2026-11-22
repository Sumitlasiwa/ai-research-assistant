from pathlib import Path
from app.services.pdf_exporter import export_to_pdf
from app.agents.planner import create_research_plan
from app.agents.writer import generate_research_report
from app.services.search import search_web
from app.services.source_manager import assign_source_ids
from app.services.md_generator import save_markdown_report
import json


def conduct_research(topic: str) -> dict:
    # 1. Generate research questions.
    plan = create_research_plan(topic)

    # 2. Search Tavily for each question.
    all_sources = []

    for question in plan["research_questions"]:
        results = search_web(question, max_results=5)

        for result in results:
            all_sources.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("content", ""),
                "score": result.get("score", 0),
                "research_question": question
            })

    # 3. Remove duplicate URLs.
    # unique_sources = remove_duplicate_sources(all_sources)

    # 4. Assign citation IDs.
    identified_sources = assign_source_ids(all_sources)

    if not identified_sources:
        raise RuntimeError("No usable sources were found.")

    # 5. Generate the report.
    report = generate_research_report(
        topic,
        identified_sources
    )

    # 6. Save Markdown report with application-generated references.
    report_path = save_markdown_report(
        topic,
        report,
        identified_sources
    )

    # 7. Export to PDF.
    pdf_path = export_to_pdf(report_path)


    return {
        "topic": topic,
        "plan": plan,
        "total_sources": len(identified_sources),
        "sources": identified_sources,
        "report": report,
        "report_urls": {
        "markdown": f"/reports/{Path(report_path).name}",
        "pdf": f"/reports/{Path(pdf_path).name}"
    }
    }

if __name__ == "__main__":
    topic = "The impact of climate change on global agriculture"
    research_data = conduct_research(topic)
    print(json.dumps(research_data, indent=4))