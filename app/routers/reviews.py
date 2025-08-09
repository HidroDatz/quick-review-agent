from fastapi import APIRouter
from pydantic import BaseModel
from ..services.review_service import trigger_review, get_current_findings

router = APIRouter()


class RunReviewRequest(BaseModel):
    project_id: int
    mr_iid: int


@router.post("/reviews/run")
async def run_review(body: RunReviewRequest):
    await trigger_review(body.project_id, body.mr_iid)
    return {"status": "queued"}


@router.get("/reviews/{project_id}/{mr_iid}")
async def get_review(project_id: int, mr_iid: int):
    return await get_current_findings(project_id, mr_iid)
