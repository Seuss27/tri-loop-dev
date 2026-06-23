from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized configuration for the Tri-Loop application."""

    primary_llm_provider: str = "anthropic"  # anthropic, google, bedrock

    # Tier 1: Fast/Cheap reasoning for PM tasks
    pm_model: str = "claude-3-haiku-20240307"

    # Tier 2: Complex reasoning for Architecture and Coding
    architect_model: str = "claude-3-5-sonnet-20240620"
    coder_model: str = "claude-3-5-sonnet-20240620"

    llm_temperature: float = 0.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
