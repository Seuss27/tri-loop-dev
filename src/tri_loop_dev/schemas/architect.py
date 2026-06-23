from typing import Dict, List

from pydantic import BaseModel, Field


class FileDefinition(BaseModel):
    filepath: str = Field(
        ...,
        description=(
            "The exact relative path for the file "
            "(e.g., 'src/rag/retriever.py')"
        ),
    )
    purpose: str = Field(
        ...,
        description="A clear explanation of what this specific file does",
    )
    internal_imports: List[str] = Field(
        default_factory=list,
        description=(
            "Other local modules this file needs to import from "
            "within the project"
        ),
    )

class FunctionSignature(BaseModel):
    function_name: str = Field(
        ...,
        description="The exact name of the function or class method",
    )
    input_args: Dict[str, str] = Field(
        ...,
        description=(
            "Dictionary of argument names and their strict type hints "
            "(e.g., {'query': 'str', 'k': 'int'})"
        ),
    )
    return_type: str = Field(
        ...,
        description="The exact type hint for the return value",
    )
    behavior: str = Field(
        ...,
        description=(
            "Step-by-step logical instructions for what the code "
            "inside this function must do"
        ),
    )

class ModuleDesign(BaseModel):
    module_name: str = Field(
        ...,
        description=(
            "Logical name of the module "
            "(e.g., 'AWS Bedrock Integration')"
        ),
    )
    files: List[FileDefinition] = Field(
        ...,
        description="The files required to build this module",
    )
    core_functions: List[FunctionSignature] = Field(
        ...,
        description="The required API contracts for this module",
    )

class ArchitectureSchema(BaseModel):
    system_overview: str = Field(
        ...,
        description="A high-level technical summary of the system design.",
    )
    project_dependencies: List[str] = Field(
        ...,
        description=(
            "Strict list of external packages required (e.g., "
            "'langgraph', 'boto3', 'pydantic'). The coder will add "
            "these via the project's dependency manager like Hatch."
        ),
    )
    modules: List[ModuleDesign] = Field(
        ...,
        min_length=1,
        description=(
            "The detailed breakdown of every module required to "
            "satisfy the PRD."
        ),
    )
    infrastructure_needs: List[str] = Field(
        default_factory=list,
        description=(
            "Required cloud resources (e.g., 'DynamoDB table', "
            "'OpenTofu state bucket') that need to be provisioned "
            "before the code runs."
        ),
    )
    step_by_step_execution_plan: List[str] = Field(
        ...,
        description=(
            "An ordered list of instructions telling the Coder exactly "
            "which module to build first."
        ),
    )
