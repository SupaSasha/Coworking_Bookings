from datetime import datetime

from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, CoworkingNotFoundException
from src.schemas.coworkings import CoworkingAdd, CoworkingPatch, Coworking
from src.services.base import BaseService


class CoworkingService(BaseService):
    async def get_filtered_by_time(
            self,
            pagination,
            location: str | None,
            title: str | None,
            datetime_from: datetime,
            datetime_to: datetime,
    ):
        check_date_to_after_date_from(datetime_from, datetime_to)
        per_page = pagination.per_page or 5
        return await self.db.coworkings.get_filtered_by_time(
            datetime_from=datetime_from,
            datetime_to=datetime_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_coworking(self, coworking_id: int):
        return await self.db.coworkings.get_one(id=coworking_id)

    async def add_coworking(self, data: CoworkingAdd):
        coworking = await self.db.coworkings.add(data)
        await self.db.commit()
        return coworking

    async def edit_coworking(self, coworking_id: int, data: CoworkingAdd):
        await self.db.coworkings.edit(data, id=coworking_id)
        await self.db.commit()

    async def edit_coworking_partially(self, coworking_id: int, data: CoworkingPatch, exclude_unset: bool = False):
        await self.db.coworkings.edit(data, exclude_unset=exclude_unset, id=coworking_id)
        await self.db.commit()

    async def delete_coworking(self, coworking_id: int):
        await self.db.coworkings.delete(id=coworking_id)
        await self.db.commit()

    async def get_coworking_with_check(self, coworking_id: int) -> Coworking:
        try:
            return await self.db.coworkings.get_one(id=coworking_id)
        except ObjectNotFoundException:
            raise CoworkingNotFoundException
