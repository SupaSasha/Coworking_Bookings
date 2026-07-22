from datetime import datetime

from src.schemas.bookings import BookingAdd, Booking
from src.utils.db_manager import DBManager


async def test_booking_crud(db: DBManager):
    user_id = (await db.users.get_all())[0].id  # type: ignore
    workplace_id = (await db.workplaces.get_all())[0].id  # type: ignore
    booking_data = BookingAdd(
        user_id=user_id,
        workplace_id=workplace_id,
        datetime_from=datetime(year=2026, month=7, day=1),
        datetime_to=datetime(year=2026, month=7, day=30),
        price=100,
    )
    new_booking: Booking = await db.bookings.add(booking_data)

    # get booking
    booking: Booking | None = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.workplace_id == new_booking.workplace_id
    assert booking.user_id == new_booking.user_id
    assert booking.model_dump(exclude={"id"}) == booking_data.model_dump()

    # renew booking
    updated_date = datetime(year=2026, month=7, day=1)
    update_booking_data = BookingAdd(
        user_id=user_id,
        workplace_id=workplace_id,
        datetime_from=datetime(year=2026, month=7, day=30),
        datetime_to=updated_date,
        price=100,
    )
    await db.bookings.edit(update_booking_data, id=new_booking.id)
    updated_booking: Booking | None = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.datetime_to == updated_date

    # delete booking
    await db.bookings.delete(id=new_booking.id)
    booking: Booking | None = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking
