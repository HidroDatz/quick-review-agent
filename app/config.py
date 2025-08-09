from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/postgres"
    gitlab_url: str = "https://gitlab.com"
    gitlab_token: str = ""
    webhook_secret: str = ""
    model_name: str = "qwen-coder"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
