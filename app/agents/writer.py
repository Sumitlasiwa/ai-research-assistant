
from app.services.llm import generate_response


def generate_research_report(
    topic: str,
    sources: list[dict],
    critique: str | None = None,
    previous_report: str | None = None,
) -> str:

    source_context = ""

    for source in sources:
        source_context += f"""
        Source ID: {source.get('source_id', '')}
        Title: {source.get('title', '')}
        URL: {source.get('url', '')}
        Content: {source.get('snippet', '')}
        """

    revision_context = ""

    if critique:
        revision_context = f"""
        REVIEWER FEEDBACK:
        {critique}

        You must address the reviewer's feedback.
        """

    if previous_report:
        revision_context += f"""
        PREVIOUS REPORT:
        {previous_report}

        Revise this report based on the reviewer's feedback.
        Preserve correct and relevant content. Do not unnecessarily
        rewrite sections that already meet the requirements.
        """

    prompt = f"""
    You are a professional research report writer.

    Research topic: {topic}

    Use the following web search sources to prepare a
    professional research report.

    SOURCES:
    {source_context}

    {revision_context}

    REPORT REQUIREMENTS:

    1. Executive Summary
    2. Key Findings
    3. Detailed Analysis
    4. Challenges and Limitations
    5. Conclusion

    RULES:
    - Use only information supported by the provided sources.
    - Cite factual claims using source IDs like [S1] or [S2].
    - Only cite source IDs that exist in the provided sources.
    - Never invent sources, statistics, or URLs.
    - If evidence is insufficient, explicitly say so.
    - Do not treat search snippets as complete articles.
    - Avoid repeating the same information.
    - Use professional, clear language.
    - Return the report in Markdown format.
    - Do not generate a References section.
      The application will generate it from source metadata.

    """

    return generate_response(prompt)
