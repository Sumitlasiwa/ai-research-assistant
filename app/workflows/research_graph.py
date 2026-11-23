from langgraph.graph import StateGraph, START, END
from app.workflows.nodes import (
    plan_node,
    research_node,
    write_node,
    review_node,
    query_generator_node,
    finalize_node,
)
from app.workflows.state import ResearchState

MAX_RESEARCH_REVISIONS = 1
MAX_WRITING_REVISIONS = 1

def route_after_review(state: ResearchState) -> str:
    """Decide which agent should handle the review feedback."""

    if state["llm_review"].get("approved", False):
        return "finish"

    target = state.get("revision_target")

    if (
        target == "researcher"
        and state["research_revision_count"] < MAX_RESEARCH_REVISIONS
    ):
        return "research"

    if (
        target == "writer"
        and state["writing_revision_count"] < MAX_WRITING_REVISIONS
    ):
        return "writer"

    # No eligible revision remains.
    return "finish"


def route_after_query_generation(state: ResearchState) -> str:
    """Decide whether follow-up research can proceed."""

    if state.get("additional_queries"):
        return "research"

    return "finish"


def build_research_graph():
    """Construct and compile the research workflow."""

    builder = StateGraph(ResearchState)

    # Register nodes
    builder.add_node("planner", plan_node)
    builder.add_node("researcher", research_node)
    builder.add_node("writer", write_node)
    builder.add_node("reviewer", review_node)
    builder.add_node("query_generator", query_generator_node)
    builder.add_node("finalizer", finalize_node)

    # Initial sequential workflow
    builder.add_edge(START, "planner")
    builder.add_edge("planner", "researcher")
    builder.add_edge("researcher", "writer")
    builder.add_edge("writer", "reviewer")
    builder.add_edge("finalizer", END)

    # Conditional feedback routing
    builder.add_conditional_edges(
        "reviewer",
        route_after_review,
        {
            "research": "query_generator",
            "writer": "writer",
            "finish": "finalizer",
        },
    )

    builder.add_conditional_edges(
    "query_generator",
    route_after_query_generation,
    {
        "research": "researcher",
        "finish": "finalizer",
    },
)
    
    return builder.compile()

    


def conduct_research_graph(topic: str) -> dict:
    """Run the complete research workflow."""

    graph = build_research_graph()

    initial_state: ResearchState = {
        "topic": topic,
        "plan": {},
        "sources": [],
        "report": "",
        "additional_queries": [],
        "llm_review": {},
        "critique": "",
        "revision_target": "",
        "research_revision_count": 0,
        "writing_revision_count": 0,
        "status": "running",
        "report_path": "",
        "pdf_path": "",
    }

    return graph.invoke(initial_state)

