import re
from pathlib import Path
from uuid import uuid4


REPORTS_DIR = Path("reports")

def save_markdown_report(topic: str, report: str,
                         sources: list[dict]) -> str:
    REPORTS_DIR.mkdir(exist_ok=True)

    # Generate a safe filename from the topic.
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
    filename = f"{slug[:50]}-{uuid4().hex[:8]}.md"

    # Generate references from actual search results so that llm do not invent citations.
    references = "\n\n## 6.References\n\n"

    for source in sources:
        references += (
            f"- [{source['source_id']}] "
            f"[{source.get('title', 'Untitled')}])"
            f"({source['url']})\n"
        )

    # report += references

    file_path = REPORTS_DIR / filename
    file_path.write_text(report, encoding="utf-8")

    return str(file_path)