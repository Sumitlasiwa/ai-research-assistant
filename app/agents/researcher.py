
from app.services.search import search_web
from app.services.source_manager import assign_source_ids
from app.services.deduplicator import remove_duplicate_sources


def conduct_research(
    plan: dict,
    previous_sources: list[dict] | None = None,
    additional_research_queries: list[str] | None = None,
    max_results_per_question: int = 5,
) -> list[dict]:

    research_questions = list(plan.get("research_questions", []))

    if not research_questions:
        raise ValueError("Research plan contains no research questions.")

    # Determine which questions to search.
    if previous_sources is None:
        # Initial research: search Planner's questions.
        questions_to_search = research_questions
        all_sources = []
    else:
        # Follow-up research: search only additional questions.
        questions_to_search = additional_research_queries or []
        all_sources = list(previous_sources)

    # Search and collect results.
    for question in questions_to_search:
        results = search_web(
            question,
            max_results=max_results_per_question,
        )

        for result in results:
            all_sources.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("snippet", ""),
                "score": result.get("score", 0),
                "research_question": question,
            })

    # Deduplicate and assign citation IDs.
    unique_sources = remove_duplicate_sources(all_sources)
    identified_sources = assign_source_ids(unique_sources)

    if not identified_sources:
        raise RuntimeError("No usable sources were found.")

    return identified_sources
