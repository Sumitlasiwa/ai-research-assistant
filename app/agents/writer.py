
from app.services.llm import generate_response


def generate_research_report(topic: str, sources: list[dict]) -> str:

    source_context = ""

    for source in sources:
        source_context += f"""
        Source ID: {source['source_id']}
        Title: {source.get('title', '')}
        URL: {source.get('url', '')}
        Content: {source.get('snippet', '')}
        """

    prompt = f"""
    You are a professional research report writer.

    Research topic: {topic}

    Use the following web search sources to prepare a
    professional research report.

    SOURCES:
    {source_context}

    REPORT REQUIREMENTS:

    1. Executive Summary
    2. Key Findings
    3. Detailed Analysis
    4. Challenges and Limitations
    5. Conclusion
    6. References

    RULES:
    - Use only information supported by the provided sources.
    - Cite factual claims using source IDs like [S1] or [S2].
    - Never invent sources, statistics, or URLs.
    - If evidence is insufficient, explicitly say so.
    - Do not treat search snippets as complete articles.
    - Avoid repeating the same information.
    - Use professional, clear language.
    - Return the report in Markdown format.

    """

    return generate_response(prompt)
