
import json
import re

from app.services.llm import generate_response


def generate_followup_queries(
    topic: str,
    critique: str,
    existing_questions: list[str],
    max_queries: int = 3,
) -> list[str]:
    """
    Generate targeted search queries based on reviewer feedback.
    """

    if not critique.strip():
        return []

    prompt = f"""
You are a research query generation assistant.

Your task is to generate targeted web search queries
to address gaps identified by a research report reviewer.

RESEARCH TOPIC:
{topic}

EXISTING RESEARCH QUESTIONS:
{json.dumps(existing_questions, ensure_ascii=False, indent=2)}

REVIEWER FEEDBACK:
{critique}

INSTRUCTIONS:
1. Identify the specific evidence or information missing.
2. Generate queries that directly address those gaps.
3. Avoid repeating the existing research questions.
4. Keep queries concise and suitable for web search.
5. Do not generate unrelated queries.
6. Generate at most {max_queries} queries.
7. Return an empty list if no additional research is needed.

OUTPUT FORMAT:
Return ONLY valid JSON in this format:

{{
    "queries": [
        "first search query",
        "second search query"
    ]
}}
"""

    response = generate_response(prompt).strip()

    # Remove Markdown JSON fences if the model includes them.
    response = re.sub(
        r"^```(?:json)?\s*|\s*```$",
        "",
        response,
        flags=re.IGNORECASE,
    ).strip()

    # Extract JSON if the model includes extra text.
    if not response.startswith("{"):
        match = re.search(r"\{.*\}", response, flags=re.DOTALL)

        if not match:
            raise ValueError(
                "Query generator did not return valid JSON."
            )

        response = match.group(0)

    try:
        result = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Query generator returned malformed JSON."
        ) from exc

    queries = result.get("queries", [])

    if not isinstance(queries, list):
        raise ValueError("Generated queries must be a list.")

    return queries