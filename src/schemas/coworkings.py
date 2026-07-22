from pydantic import BaseModel


class CoworkingAdd(BaseModel):
    title: str
    location: str


class Coworking(CoworkingAdd):
    id: int


class CoworkingPatch(BaseModel):
    title: str | None = None
    location: str | None = None
