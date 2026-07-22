from src.exceptions import ObjectNotFoundException, WorkplaceNotFoundException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.coworkings import Coworking
from src.schemas.workplaces import Workplace
from src.services.base import BaseService


class BookingService(BaseService):
    async def add_booking(self, user_id: int, booking_data: BookingAddRequest):
        try:
            workplace: Workplace = await self.db.workplaces.get_one(id=booking_data.workplace_id)
        except ObjectNotFoundException as ex:
            raise WorkplaceNotFoundException from ex
        coworking: Coworking = await self.db.coworkings.get_one(id=workplace.coworking_id)
        workplace_price: int = workplace.price
        _booking_data = BookingAdd(
            user_id=user_id,
            price=workplace_price,
            **booking_data.model_dump(),
        )
        booking = await self.db.bookings.add_booking(_booking_data, coworking_id=coworking.id)
        await self.db.commit()
        return booking

    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)
