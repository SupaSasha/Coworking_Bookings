from fastapi import APIRouter
from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    AllWorkplacesAreBookedException,
    AllWorkplacesAreBookedHTTPException,
    WorkplaceNotFoundException,
    WorkplaceNotFoundHTTPException,
)
from src.schemas.bookings import BookingAddRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest,
):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except WorkplaceNotFoundException:
        raise WorkplaceNotFoundHTTPException
    except AllWorkplacesAreBookedException:
        raise AllWorkplacesAreBookedHTTPException
    return {"status": "OK", "data": booking}