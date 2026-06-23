import pytest

from tri_loop_dev.utils.llm_factory import get_llm


def test_llm_factory_unsupported_provider() -> None:
    """Test that requesting an unknown provider raises a ValueError."""
    with pytest.raises(ValueError) as exc_info:
        get_llm(provider="fake_ai")

    assert "Unsupported LLM provider: fake_ai" in str(exc_info.value)


def test_llm_factory_import_error_message(mocker) -> None:
    """Test that missing dependencies trigger the actionable ImportError."""
    # Force the factory to think anthropic is NOT installed
    mocker.patch.dict("sys.modules", {"langchain_anthropic": None})

    with pytest.raises(ImportError) as exc_info:
        get_llm(provider="anthropic")

    assert "Anthropic support is not installed" in str(exc_info.value)
    assert "pip install .[anthropic]" in str(exc_info.value)
