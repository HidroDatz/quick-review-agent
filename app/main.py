from fastapi import FastAPI
from .utils.logging import setup_logging, CorrelationIdMiddleware
from .routers import webhooks, reviews, analytics


setup_logging()
app = FastAPI(title="AI Code Review")
app.add_middleware(CorrelationIdMiddleware)
app.include_router(webhooks.router)
app.include_router(reviews.router)
app.include_router(analytics.router)


@app.get("/")
async def root():
    return {"status": "ok"}
