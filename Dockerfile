FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock* requirements.txt* /app/
RUN pip install --no-cache-dir fastapi uvicorn[standard] httpx structlog sqlmodel alembic pydantic-settings pytest pytest-cov psycopg2-binary
RUN apt-get update && apt-get install -y netcat-traditional
COPY . /app
COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
