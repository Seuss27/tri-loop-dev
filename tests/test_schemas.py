import pytest
from pydantic import ValidationError

from tri_loop_dev.schemas.coder import CodeArtifacts
from tri_loop_dev.schemas.prd import PRDSchema


def test_prd_schema_valid_data(valid_prd_data: dict) -> None:
    """Test that valid dictionary data correctly instantiates the PRD."""
    prd = PRDSchema(**valid_prd_data)
    assert prd.project_name == "StringReverser"
    assert len(prd.core_features) == 1
    assert prd.core_features[0].name == "Reverse Endpoint"


def test_prd_schema_missing_required_fields() -> None:
    """Test that missing required fields raises a validation error."""
    incomplete_data = {
        "project_name": "StringReverser",
        # Missing executive_summary and core_features
    }
    with pytest.raises(ValidationError):
        PRDSchema(**incomplete_data)


def test_code_artifacts_schema() -> None:
    """Test that the Coder schema correctly formats file dictionaries."""
    data = {"files": {"main.py": "print('hello')", "utils.py": "pass"}}
    artifacts = CodeArtifacts(**data)
    assert "main.py" in artifacts.files
    assert artifacts.files["utils.py"] == "pass"
