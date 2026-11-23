
from app.agents.planner import create_research_plan
from app.agents.researcher import conduct_research
from app.agents.writer import generate_research_report
from app.agents.reviewer import evaluate_report
from app.agents.query_generator import generate_followup_queries
from app.services.md_generator import save_markdown_report
from app.services.pdf_exporter import export_to_pdf


def plan_node(state: dict) -> dict:
    """Generate the research plan."""
    plan = create_research_plan(state["topic"])

    return {"plan": plan}



def research_node(state: dict) -> dict:
    """Collect and prepare research sources."""

    is_researcher_revision = (
        state.get("revision_target") == "researcher"
    )

    if is_researcher_revision:
        additional_queries = state.get("additional_queries", [])

        if not additional_queries:
            raise ValueError(
                "Research revision requested, but no follow-up queries were generated."
            )

        sources = conduct_research(
            plan=state["plan"],
            previous_sources=state["sources"],
            additional_research_queries=additional_queries,
        )
    else:
        sources = conduct_research(plan=state["plan"])

    updates = {"sources": sources}

    if is_researcher_revision:
        updates["research_revision_count"] = (
            state.get("research_revision_count", 0) + 1
        )

    return updates




def write_node(state: dict) -> dict:
    """Generate or revise the research report."""

    is_writer_revision = state.get("revision_target") == "writer"

    # Pass critique after either research or writing feedback.
    critique = state.get("critique") or None

    report = generate_research_report(
        topic=state["topic"],
        sources=state["sources"],
        critique=critique,
        previous_report=state.get("report") or None,
    )

    updates = {
        "report": report,
        # Clear feedback after the Writer has addressed it.
        "critique": "",
        "revision_target": "",
    }

    if is_writer_revision:
        updates["writing_revision_count"] = (
            state.get("writing_revision_count", 0) + 1
        )

    return updates



def review_node(state: dict) -> dict:
    """Evaluate the generated report using the LLM reviewer."""
    review = evaluate_report(
        topic=state["topic"],
        plan=state["plan"],
        report=state["report"],
        sources=state["sources"],
    )

    findings = review.get("findings", [])

    critique = "\n".join(
        f"- [{finding['severity']}] "
        f"{finding['criterion']}: {finding['issue']} "
        f"Recommendation: {finding['recommendation']}"
        for finding in findings
    )

    # Prioritize additional research when both agents need work.
    targets = {finding["target"] for finding in findings}

    # if "researcher" in targets:
    #     revision_target = "researcher"
    if "writer" in targets:
        revision_target = "writer"
    else:
        revision_target = ""

    return {
        "llm_review": review,
        "critique": critique,
        "revision_target": revision_target,
        "status": "approved" if review.get("approved") else "needs_revision",
    }


def query_generator_node(state: dict) -> dict:
    """Generate additional research queries based on reviewer feedback."""

    additional_queries = generate_followup_queries(
        topic=state["topic"],
        critique=state.get("critique", ""),
        existing_questions=state["plan"].get("research_questions", []),
    )

    if not additional_queries:
        # No useful follow-up queries could be generated.
        # The graph will proceed to the finalizer.
        return {
            "additional_queries": [],
            "revision_target": "",
            "status": "needs_revision",
        }

    return {"additional_queries": additional_queries}



def finalize_node(state: dict) -> dict:
    """Save the final report as Markdown and export it to PDF."""

    markdown_path = save_markdown_report(
        topic=state["topic"],
        report=state["report"],
        sources=state["sources"],
    )

    pdf_path = export_to_pdf(markdown_path)

    return {
        "report_path": markdown_path,
        "pdf_path": pdf_path,
    }
