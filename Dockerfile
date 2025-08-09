FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock* requirements.txt* /app/
RUN pip install --no-cache-dir fastapi uvicorn[standard] httpx structlog sqlmodel alembic pydantic-settings pytest pytest-cov
COPY . /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
