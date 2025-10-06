"""
Application configuration.
Centralized settings loaded from environment variabels
"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    """
    Application settings with sensible defaults for development
    Override via environment variables .env files
    """

    NAME: str = "PDM Backend API"
    VERSION: str = "0.0.0"
    DEBUG: bool = True
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
