from langchain_core.language_models.chat_models import BaseChatModel

from tri_loop_dev.config import settings


def get_llm(
    provider: str | None = None,
    model: str | None = None,
    temperature: float | None = None
) -> BaseChatModel:
    """Factory to instantiate and return the requested LLM provider."""

    prov = provider or settings.primary_llm_provider

    # FIX: Updated fallback from primary_llm_model to pm_model
    mod = model or settings.pm_model

    temp = (
        temperature if temperature is not None
        else settings.llm_temperature
    )

    if prov.lower() == "anthropic":
        try:
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(model=mod, temperature=temp)
        except ImportError as err:
            raise ImportError(
                "Anthropic support is not installed. "
                "Run: pip install '.[anthropic]' or "
                "'hatch env run pip install .[anthropic]'"
            ) from err

    elif prov.lower() == "google":
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(model=mod, temperature=temp)
        except ImportError as err:
            raise ImportError(
                "Google GenAI support is not installed. "
                "Run: pip install '.[google]' or "
                "'hatch env run pip install .[google]'"
            ) from err

    elif prov.lower() == "bedrock":
        try:
            from langchain_aws import ChatBedrock
            return ChatBedrock(
                model_id=mod,
                model_kwargs={"temperature": temp}
            )
        except ImportError as err:
            raise ImportError(
                "AWS Bedrock support is not installed. "
                "Run: pip install '.[aws]' or "
                "'hatch env run pip install .[aws]'"
            ) from err

    else:
        raise ValueError(f"Unsupported LLM provider: {prov}")
