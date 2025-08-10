from fastapi import APIRouter, Request, Header, HTTPException
import structlog
from ..services.review_service import trigger_review
from ..config import settings

router = APIRouter()


@router.post("/gitlab/webhook")
async def gitlab_webhook(request: Request, x_gitlab_token: str = Header(None)):
    if x_gitlab_token != settings.webhook_secret:
        raise HTTPException(status_code=401, detail="Unauthorized")

    payload = await request.json()

    if payload.get("object_kind") == "merge_request":
        action = payload.get("object_attributes", {}).get("action")
        if action in {"open", "update"}:
            project_id = payload["project"]["id"]
            mr_iid = payload["object_attributes"]["iid"]
            await trigger_review(project_id, mr_iid)

    elif (
        payload.get("object_kind") == "note"
        and payload.get("object_attributes", {}).get("note") == "/ai-review"
    ):
        project_id = payload["project"]["id"]
        mr_iid = payload["merge_request"]["iid"]
        await trigger_review(project_id, mr_iid)

    return {"status": "ok"}
