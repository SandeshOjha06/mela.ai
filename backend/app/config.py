"""
Application configuration using pydantic-settings.

Loads environment variables from a .env file and provides typed access
to all configuration parameters needed by the application.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database connection string (SQLite for local dev, PostgreSQL for production)
    DATABASE_URL: str = "sqlite+aiosqlite:///./event_command_center.db"

    # Groq API key for Llama-3 access
    GROQ_API_KEY: str = ""

    # ChromaDB persistence directory
    CHROMA_PERSIST_DIR: str = "./chroma_data"

    # LLM model identifier (Groq-hosted)
    LLM_MODEL: str = "llama-3.3-70b-versatile"

    # Gmail SMTP settings for sending real emails
    SMTP_USER: str = ""          # e.g. yourname@gmail.com
    SMTP_APP_PASSWORD: str = ""  # Gmail App Password (not your regular password)

    # Always read backend/.env, even when the process is launched from repo root.
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[1] / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        # Prefer .env over shell-exported vars to avoid stale SMTP values
        # from older terminal sessions taking precedence.
        return (
            init_settings,
            dotenv_settings,
            env_settings,
            file_secret_settings,
        )


# Singleton settings instance
settings = Settings()
