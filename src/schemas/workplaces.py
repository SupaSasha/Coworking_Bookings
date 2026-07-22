from pydantic import BaseModel, ConfigDict

from src.schemas.facilities import Facility


class WorkplaceAddRequest(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []


class WorkplaceAdd(BaseModel):
    coworking_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Workplace(WorkplaceAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class WorkplaceWithRels(Workplace):
    facilities: list[Facility]


class WorkplacePatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []


class WorkplacePatch(BaseModel):
    coworking_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
