from fastapi import APIRouter, Request, Header
from ..services.review_service import trigger_review

router = APIRouter()


@router.post("/gitlab/webhook")
async def gitlab_webhook(request: Request, x_gitlab_token: str = Header(None)):
    payload = await request.json()
    # For brevity, only respond to manual trigger in tests
    if payload.get("object_kind") == "note" and payload.get("object_attributes", {}).get("note") == "/ai-review":
        project_id = payload["project"]["id"]
        mr_iid = payload["merge_request"]["iid"]
        await trigger_review(project_id, mr_iid)
    return {"status": "ok"}
