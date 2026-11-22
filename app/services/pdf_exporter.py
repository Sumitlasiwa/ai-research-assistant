import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
)
from reportlab.lib.units import inch
from xml.sax.saxutils import escape


def md_inline(text: str) -> str:
    """Convert inline markdown to ReportLab HTML-like tags."""
    text = escape(text)
    # **bold** → <b>bold</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # *italic* → <i>italic</i>
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    return text


def export_to_pdf(markdown_path: str) -> str:
    md_path = Path(markdown_path)
    pdf_path = md_path.with_suffix(".pdf")

    styles = getSampleStyleSheet()

    # Custom bullet style
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=styles["BodyText"],
        leftIndent=18,
        firstLineIndent=-12,
        spaceBefore=2,
        spaceAfter=4,
    )

    story = []
    lines = md_path.read_text(encoding="utf-8").splitlines()

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            story.append(Spacer(1, 0.12 * inch))

        elif stripped.startswith("# "):
            story.append(Paragraph(md_inline(stripped[2:]), styles["Title"]))

        elif stripped.startswith("## "):
            story.append(Paragraph(md_inline(stripped[3:]), styles["Heading2"]))

        elif stripped.startswith("### "):
            story.append(Paragraph(md_inline(stripped[4:]), styles["Heading3"]))

        elif stripped.startswith(("* ", "- ", "+ ")):
            # Collect consecutive bullet lines into a list
            bullets = []
            while i < len(lines):
                s = lines[i].strip()
                if s.startswith(("* ", "- ", "+ ")):
                    # Remove the bullet marker
                    content = re.sub(r'^[*+-]\s+', '', s)
                    bullets.append(content)
                    i += 1
                else:
                    break

            list_items = [
                ListItem(Paragraph(md_inline(b), bullet_style))
                for b in bullets
            ]
            story.append(ListFlowable(
                list_items,
                bulletType="bullet",
                start="•",
                leftIndent=12,
            ))
            continue  # already advanced i

        else:
            story.append(Paragraph(md_inline(stripped), styles["BodyText"]))

        i += 1

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )
    document.build(story)
    return str(pdf_path)


if __name__ == "__main__":
    markdown_file = "reports/the-impact-of-climate-change-on-global-agriculture-906d64f1.md"
    pdf_file = export_to_pdf(markdown_file)
    print(f"PDF exported to: {pdf_file}")   