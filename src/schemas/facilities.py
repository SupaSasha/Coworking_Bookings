from pydantic import BaseModel, ConfigDict


class FacilityAdd(BaseModel):
    title: str


class Facility(FacilityAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class WorkplaceFacilityAdd(BaseModel):
    workplace_id: int
    facility_id: int


class WorkplaceFacility(WorkplaceFacilityAdd):
    id: int
