from datetime import datetime
from typing import Sequence

#from fastapi import HTTPException
from sqlalchemy import select

from src.exceptions import AllWorkplacesAreBookedException
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import workplaces_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsOrm).filter(BookingsOrm.datetime_from == datetime.today())
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, data: BookingAdd, coworking_id: int):
        workplaces_ids_to_get = workplaces_ids_for_booking(
            datetime_from=data.datetime_from,
            datetime_to=data.datetime_to,
            coworking_id=coworking_id,
        )
        workplaces_ids_to_book_res = await self.session.execute(workplaces_ids_to_get)
        workplaces_ids_to_book: Sequence[int] = workplaces_ids_to_book_res.scalars().all()

        if data.workplace_id in workplaces_ids_to_book:
            new_booking = await self.add(data)
            return new_booking

        raise AllWorkplacesAreBookedException
