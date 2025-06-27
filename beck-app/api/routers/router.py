from fastapi import APIRouter, Depends, HTTPException
from typing import List
from core.services.service import SpyCatService
from api.routers.schemas import CatCreate, CatUpdate, CatResponse, MissionCreate, MissionResponse, TargetUpdate
from core.db_helper import db_helper

router = APIRouter(prefix="", tags=["Spy Cat Agency"])

# Dependency to get service instances
async def get_spy_cat_service():
    return SpyCatService(db_helper.session_factory)

# Cat Routes
@router.post("/cats/", response_model=CatResponse)
async def create_cat_endpoint(
    cat: CatCreate,
    spy_cat_service: SpyCatService = Depends(get_spy_cat_service)
):
    try:
        created_cat = await spy_cat_service.create_cat(cat.dict())
        return created_cat
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/cats/", response_model=List[CatResponse])
async def read_cats_endpoint(
    skip: int = 0,
    limit: int = 100,
    spy_cat_service: SpyCatService = Depends(get_spy_cat_service)
):
    try:
        cats = await spy_cat_service.get_cats(skip, limit)
        return cats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/cats/{cat_id}", response_model=CatResponse)
async def read_cat_endpoint(
    cat_id: int,
    spy_cat_service: SpyCatService = Depends(get_spy_cat_service)
):
    try:
        cat = await spy_cat_service.get_cat(cat_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")
        return cat
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/cats/{cat_id}", response_model=CatResponse)
async def update_cat_endpoint(
    cat_id: int,
    salary: CatUpdate,
    spy_cat_service: SpyCatService = Depends(get_spy_cat_service)
):
    try:
        updated_cat = await spy_cat_service.update_cat(cat_id, salary.salary)
        if not updated_cat:
            raise HTTPException(status_code=404, detail="Cat not found")
        return updated_cat
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.delete("/cats/{cat_id}")
async def delete_cat_endpoint(
    cat_id: int,
    spy_cat_service: SpyCatService = Depends(get_spy_cat_service)
):
    try:
        deleted_cat = await spy_cat_service.delete_cat(cat_id)
        if not deleted_cat:
            raise HTTPException(status_code=404, detail="Cat not found")
        return {"message": "Cat deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Mission Routes
@router.post("/missions/", response_model=MissionResponse)
async def create_mission_endpoint(
    mission: MissionCreate,
    cat_id: int | None = None,
    spy_cat_service: SpyCatService = Depends(get_spy_cat_service)
):
    try:
        created_mission = await spy_cat_service.create_mission(mission.dict(), cat_id)
        return created_mission
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/missions/{mission_id}/targets/{target_id}")
async def update_target_endpoint(
    mission_id: int,
    target_id: int,
    target_update: TargetUpdate,
    spy_cat_service: SpyCatService = Depends(get_spy_cat_service)
):
    try:
        updated_target = await spy_cat_service.update_target(mission_id, target_id, target_update.dict(exclude_unset=True))
        if not updated_target:
            raise HTTPException(status_code=404, detail="Target not found")
        return updated_target
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/missions/{mission_id}/assign/{cat_id}")
async def assign_cat_endpoint(
    mission_id: int,
    cat_id: int,
    spy_cat_service: SpyCatService = Depends(get_spy_cat_service)
):
    try:
        assigned_mission = await spy_cat_service.assign_cat_to_mission(mission_id, cat_id)
        if not assigned_mission:
            raise HTTPException(status_code=404, detail="Mission not found")
        return assigned_mission
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/missions/", response_model=List[MissionResponse])
async def read_missions_endpoint(
    skip: int = 0,
    limit: int = 100,
    spy_cat_service: SpyCatService = Depends(get_spy_cat_service)
):
    try:
        missions = await spy_cat_service.get_missions(skip, limit)
        return missions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/missions/{mission_id}", response_model=MissionResponse)
async def read_mission_endpoint(
    mission_id: int,
    spy_cat_service: SpyCatService = Depends(get_spy_cat_service)
):
    try:
        mission = await spy_cat_service.get_mission(mission_id)
        if not mission:
            raise HTTPException(status_code=404, detail="Mission not found")
        return mission
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.delete("/missions/{mission_id}")
async def delete_mission_endpoint(
    mission_id: int,
    spy_cat_service: SpyCatService = Depends(get_spy_cat_service)
):
    try:
        deleted_mission = await spy_cat_service.delete_mission(mission_id)
        if not deleted_mission:
            raise HTTPException(status_code=404, detail="Mission not found")
        return {"message": "Mission deleted"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

