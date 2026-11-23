import json
from app.services.llm import generate_response, generate_response_reviewer


def create_research_plan(topic: str) -> dict:

    prompt = f"""
    You are an expert research planner.

    The user wants to research this topic:
    {topic}

    Break this topic into 3-5 specific research questions.

    Requirements:
    1. Questions must cover different aspects.
    2. Avoid overlapping questions.
    3. Questions should be suitable for web research.
    4. Return valid JSON only.

    Required JSON format:
    {{
        "topic": "{topic}",
        "research_questions": [
            "question 1",
            "question 2",
            "question 3"
        ]
    }}
    """

    response = generate_response_reviewer(prompt).strip()

    # Strip markdown code fences
    if response.startswith("```"):
        response = response.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    try:
        plan = json.loads(response) # converts string to dict
    except json.JSONDecodeError:
        raise ValueError("Bad JSON")

    questions = plan.get("research_questions")

    if not isinstance(questions, list) or not questions: # must be non-empty list
        raise ValueError("Invalid research plan")

    return plan

if __name__ == "__main__":
    topic = "The impact of climate change on global agriculture"
    research_plan = create_research_plan(topic)
    print(json.dumps(research_plan, indent=4))