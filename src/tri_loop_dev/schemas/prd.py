from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class PriorityLevel(str, Enum):
    MUST_HAVE = "must_have"
    SHOULD_HAVE = "should_have"
    NICE_TO_HAVE = "nice_to_have"

class Feature(BaseModel):
    name: str = Field(..., description="Short, descriptive name of the feature")
    description: str = Field(..., description="Business value and core functionality")
    priority: PriorityLevel = Field(..., description="Requirement priority")

class SecurityConstraint(BaseModel):
    requirement: str = Field(
        ..., description="Specific security or identity constraint"
    )
    impact: str = Field(..., description="Architectural impact (e.g., requires RBAC)")

class PRDSchema(BaseModel):
    project_name: str = Field(..., description="The name of the project")
    executive_summary: str = Field(..., description="2-3 sentence project overview")
    core_features: List[Feature] = Field(..., min_length=1)
    out_of_scope: List[str] = Field(
        ..., description="Explicit non-goals to prevent scope creep"
    )
    infrastructure_constraints: List[str] = Field(
        ..., description="Mandated tech stack"
    )
    security_and_identity: List[SecurityConstraint] = Field(default_factory=list)
    success_criteria: List[str] = Field(
        ..., description="Measurable definition of done"
    )
    unresolved_questions: Optional[List[str]] = Field(
        None, description="Questions for the Architect"
    )
