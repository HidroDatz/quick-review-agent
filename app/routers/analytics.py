from fastapi import APIRouter

router = APIRouter()


@router.get("/analytics/mr/{project_id}/{mr_iid}")
async def mr_metrics(project_id: int, mr_iid: int):
    return {"project_id": project_id, "mr_iid": mr_iid}


@router.get("/analytics/user/{user_id}")
async def user_metrics(user_id: int):
    return {"user_id": user_id}
