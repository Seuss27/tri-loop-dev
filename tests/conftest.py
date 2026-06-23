import pytest
from langchain_core.messages import HumanMessage

from tri_loop_dev.schemas.prd import PRDSchema, PriorityLevel


@pytest.fixture
def mock_initial_state() -> dict:
    return {
        "messages": [HumanMessage(content="Build a string reverse API.")],
        "prd_json": None,
        "architecture_schema": None,
        "code_artifacts": None,
        "current_error": None,
        "is_approved": False,
    }


@pytest.fixture
def valid_prd_data() -> dict:
    return {
        "project_name": "StringReverser",
        "executive_summary": "An API to reverse strings.",
        "core_features": [
            {
                "name": "Reverse Endpoint",
                "description": "Takes a string and reverses it.",
                "priority": PriorityLevel.MUST_HAVE,
            }
        ],
        "out_of_scope": ["UI components"],
        "infrastructure_constraints": ["Python 3.12"],
        "security_and_identity": [],
        "success_criteria": ["100% test coverage"],
        "unresolved_questions": None,
    }


@pytest.fixture
def valid_prd_object(valid_prd_data: dict) -> PRDSchema:
    return PRDSchema(**valid_prd_data)
