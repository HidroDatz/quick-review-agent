from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlmodel import SQLModel


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/postgres"
    gitlab_url: str = "https://gitlab.com"
    gitlab_token: str = ""
    webhook_secret: str = ""
    model_name: str = "qwen-coder"
    openai_base_url: str = ""
    openai_api_key: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(settings.database_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
