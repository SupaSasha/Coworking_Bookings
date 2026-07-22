from datetime import datetime

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import ObjectNotFoundException, CoworkingNotFoundHTTPException
from src.schemas.coworkings import CoworkingPatch, CoworkingAdd
from src.services.coworkings import CoworkingService

router = APIRouter(prefix="/coworkings", tags=["Coworkings"])


@router.get("")
@cache(expire=10)
async def get_coworkings(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Loca"),
    title: str | None = Query(None, description="Coworking Name"),
    datetime_from: datetime = Query(examples=["2026-08-01T12:30"]),
    datetime_to: datetime = Query(examples=["2026-08-01T15:30"]),
):
    return await CoworkingService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        datetime_from,
        datetime_to,
    )


@router.get("/{coworking_id}")
async def get_coworking(coworking_id: int, db: DBDep):
    try:
        return await CoworkingService(db).get_coworking(coworking_id)
    except ObjectNotFoundException:
        raise CoworkingNotFoundHTTPException


@router.post("")
async def create_coworking(
    db: DBDep,
    coworking_data: CoworkingAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Montevideo",
                "value": {
                    "title": "IT Amingos Coworking",
                    "location": "La Rambla, 1",
                },
            },
            "2": {
                "summary": "Punta del este",
                "value": {
                    "title": "las Gafas Coworking",
                    "location": "La Rambla, 1",
                },
            },
        }
    ),
):
    coworking = await CoworkingService(db).add_coworking(coworking_data)
    return {"status": "OK", "data": coworking}


@router.put("/{coworking_id}")
async def edit_coworking(coworking_id: int, coworking_data: CoworkingAdd, db: DBDep):
    await CoworkingService(db).edit_coworking(coworking_id, coworking_data)
    return {"status": "OK"}


@router.patch(
    "/{coworking_id}",
    summary="Partial update of coworking data",
    description="<h1>Partial update of hotel coworking header</h1>",
)
async def partially_edit_coworking(
    coworking_id: int,
    coworking_data: CoworkingPatch,
    db: DBDep,
):
    await CoworkingService(db).edit_coworking_partially(coworking_id, coworking_data, exclude_unset=True)
    return {"status": "OK"}


@router.delete("/{coworking_id}")
async def delete_coworking(coworking_id: int, db: DBDep):
    await CoworkingService(db).delete_coworking(coworking_id)
    return {"status": "OK"}
