from datetime import datetime

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.exceptions import CoworkingNotFoundHTTPException, \
    WorkplaceNotFoundHTTPException, WorkplaceNotFoundException, CoworkingNotFoundException
from src.schemas.workplaces import WorkplaceAddRequest, WorkplacePatchRequest
from src.services.workplaces import WorkplaceService

router = APIRouter(prefix="/coworkings", tags=["Workplaces"])


@router.get("/{coworking_id}/workplaces")
async def get_workplaces(
    coworking_id: int,
    db: DBDep,
    datetime_from: datetime = Query(examples=["2026-08-01T12:30"]),
    datetime_to: datetime = Query(examples=["2026-08-01T15:30"]),
):
    return await WorkplaceService(db).get_filtered_by_time(coworking_id, datetime_from, datetime_to)


@router.get("/{coworking_id}/workplaces/{workplace_id}")
async def get_workplace(coworking_id: int, workplace_id: int, db: DBDep):
    try:
        return await WorkplaceService(db).get_workplace(workplace_id, coworking_id=coworking_id)
    except WorkplaceNotFoundException:
        raise WorkplaceNotFoundHTTPException


@router.post("/{coworking_id}/workplaces")
async def create_workplace(coworking_id: int, db: DBDep, workplace_data: WorkplaceAddRequest = Body()):
    try:
        workplace = await WorkplaceService(db).create_workplace(coworking_id, workplace_data)
    except CoworkingNotFoundException:
        raise CoworkingNotFoundHTTPException
    return {"status": "OK", "data": workplace}


@router.put("/{coworking_id}/workplaces/{workplace_id}")
async def edit_workplace(
    coworking_id: int,
    workplace_id: int,
    workplace_data: WorkplaceAddRequest,
    db: DBDep,
):
    await WorkplaceService(db).edit_workplace(coworking_id, workplace_id, workplace_data)
    return {"status": "OK"}


@router.patch("/{coworking_id}/workplaces/{workplace_id}")
async def partially_edit_workplace(
    coworking_id: int,
    workplace_id: int,
    workplace_data: WorkplacePatchRequest,
    db: DBDep,
):
    await WorkplaceService(db).partially_edit_workplace(coworking_id, workplace_id, workplace_data)
    return {"status": "OK"}


@router.delete("/{coworking_id}/workplaces/{workplace_id}")
async def delete_workplace(coworking_id: int, workplace_id: int, db: DBDep):
    await WorkplaceService(db).delete_workplace(coworking_id, workplace_id)
    return {"status": "OK"}
