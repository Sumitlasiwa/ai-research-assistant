from typing import Literal
from pydantic import BaseModel, Field

class ReviewFinding(BaseModel):
    criterion: Literal["completeness", "readability", "citation_grounding"]
    severity: Literal["critical", "major", "minor"]
    target: Literal["researcher", "writer"]
    issue: str
    recommendation: str
    evidence: str = ""

class LLMReviewResult(BaseModel):
    approved: bool
    overall_assessment: str
    findings: list[ReviewFinding] = Field(default_factory=list)