from fastapi import FastAPI
from .utils.logging import setup_logging, CorrelationIdMiddleware
from .routers import webhooks, reviews, analytics
from .config import create_db_and_tables


setup_logging()
app = FastAPI(title="AI Code Review")



@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.add_middleware(CorrelationIdMiddleware)
app.include_router(webhooks.router)
app.include_router(reviews.router)
app.include_router(analytics.router)


@app.get("/")
async def root():
    return {"status": "ok"}
