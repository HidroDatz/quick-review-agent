"""Minimal GitLab API client using httpx."""
from __future__ import annotations
import httpx
from ..config import settings


async def get_merge_request(project_id: int, mr_iid: int) -> dict:
    url = f"{settings.gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}"
    async with httpx.AsyncClient(headers={"PRIVATE-TOKEN": settings.gitlab_token}) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()


async def get_changes(project_id: int, mr_iid: int) -> dict:
    url = f"{settings.gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/changes"
    async with httpx.AsyncClient(headers={"PRIVATE-TOKEN": settings.gitlab_token}) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()


async def post_comment(project_id: int, mr_iid: int, body: str) -> None:
    """Post a comment to a merge request."""
    url = f"{settings.gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes"
    async with httpx.AsyncClient(headers={"PRIVATE-TOKEN": settings.gitlab_token}) as client:
        resp = await client.post(url, json={"body": body})
        resp.raise_for_status()
