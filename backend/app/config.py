from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


def _split(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings(BaseSettings):
    """Application settings, read from environment variables or a local .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Student Feedback System"
    app_version: str = "0.2.0"
    app_env: str = "development"
    log_level: str = "INFO"

    gcp_project_id: str
    firestore_database: str = "(default)"
    firestore_collection: str = "feedback"

    # NLP: Cloud Natural Language API for officially supported languages,
    # Gemini on Vertex AI for everything else (e.g. Albanian).
    nl_supported_languages: str = "en,es,fr,de,it,pt,ja,ko,zh,zh-Hant"
    gemini_model: str = "gemini-3.5-flash-lite"
    gemini_location: str = "global"

    # Score thresholds for mapping a sentiment score (-1..1) to a label
    sentiment_positive_threshold: float = 0.25
    sentiment_negative_threshold: float = -0.25

    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return _split(self.cors_origins)

    @property
    def nl_supported_language_list(self) -> list[str]:
        return _split(self.nl_supported_languages)


@lru_cache
def get_settings() -> Settings:
    return Settings()
