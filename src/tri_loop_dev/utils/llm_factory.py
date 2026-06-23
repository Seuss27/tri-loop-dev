from langchain_core.language_models.chat_models import BaseChatModel

from tri_loop_dev.config import settings


def get_llm(
    provider: str | None = None,
    model: str | None = None,
    temperature: float | None = None
) -> BaseChatModel:
    """Factory to instantiate and return the requested LLM provider."""

    # Fallback to central settings if specific overrides aren't provided
    prov = provider or settings.primary_llm_provider
    mod = model or settings.primary_llm_model
    temp = temperature if temperature is not None else settings.llm_temperature

    if prov.lower() == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=mod, temperature=temp)

    elif prov.lower() == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=mod, temperature=temp)

    elif prov.lower() == "bedrock":
        from langchain_aws import ChatBedrock
        return ChatBedrock(model_id=mod, model_kwargs={"temperature": temp})

    else:
        raise ValueError(f"Unsupported LLM provider: {prov}")
