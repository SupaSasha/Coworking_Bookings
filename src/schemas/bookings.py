from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


DATE_FORMAT = "%Y-%m-%dT%H:%M"


class BookingAddRequest(BaseModel):
    workplace_id: int

    datetime_from: datetime = Field(
        examples=["2026-07-18T11:30"]
    )

    datetime_to: datetime = Field(
        examples=["2026-07-18T15:30"]
    )

    @field_validator("datetime_from", "datetime_to", mode="before")
    @classmethod
    def validate_datetime(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, DATE_FORMAT)
            except ValueError:
                raise ValueError(
                    "Format must be YYYY-MM-DDTHH:MM"
                )

        return value


class BookingAdd(BaseModel):
    user_id: int
    workplace_id: int
    datetime_from: datetime
    datetime_to: datetime
    price: int


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)