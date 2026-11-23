
from typing import TypedDict


class ResearchState(TypedDict):
    # User input
    topic: str

    # Planner output
    plan: dict

    # Researcher output
    sources: list[dict]
    additional_research_queries: list[str]

    # Writer output
    report: str

    # Reviewer outputs
    # deterministic_review: dict
    llm_review: dict

    # Feedback and routing
    critique: str
    revision_target: str

    # Revision limits
    research_revision_count: int
    writing_revision_count: int

    # Final output
    status: str
    report_path: str
    pdf_path: str

