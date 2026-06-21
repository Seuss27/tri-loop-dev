from typing import Dict, List

from pydantic import BaseModel, Field


class FileDefinition(BaseModel):
    filepath: str = Field(..., description="Relative path from project root")
    purpose: str = Field(..., description="Brief description of file responsibility")
    dependencies: List[str] = Field(
        ..., description="List of internal/external modules required"
    )

class APIDefinition(BaseModel):
    endpoint: str = Field(..., description="API route or function signature")
    input_schema: Dict[str, str] = Field(..., description="Data structure for inputs")
    output_schema: Dict[str, str] = Field(..., description="Data structure for outputs")

class SystemArchitectureSchema(BaseModel):
    project_structure: List[FileDefinition] = Field(..., description="File system map")
    api_contracts: List[APIDefinition] = Field(..., description="Defined interfaces")
    data_models: List[Dict[str, str]] = Field(
        ..., description="Core data structures/DB schemas"
    )
    implementation_steps: List[str] = Field(
        ..., description="Step-by-step dev plan for the Coder"
    )
