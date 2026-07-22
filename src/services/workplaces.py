from datetime import date

from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, CoworkingNotFoundException, \
    WorkplaceNotFoundException
from src.schemas.facilities import WorkplaceFacilityAdd
from src.schemas.workplaces import WorkplaceAddRequest, Workplace, WorkplaceAdd, WorkplacePatchRequest, WorkplacePatch
from src.services.base import BaseService
from src.services.coworkings import CoworkingService


class WorkplaceService(BaseService):
    async def get_filtered_by_time(
            self,
            coworking_id: int,
            datetime_from: date,
            datetime_to: date,
    ):
        check_date_to_after_date_from(datetime_from, datetime_to)
        return await self.db.workplaces.get_filtered_by_time(
            coworking_id=coworking_id, datetime_from=datetime_from, datetime_to=datetime_to
        )
    
    async def get_workplace(self, workplace_id: int, coworking_id: int):
        return await self.db.workplaces.get_one_with_rels(id=workplace_id, coworking_id=coworking_id)

    async def create_workplace(
            self,
            coworking_id: int,
            workplace_data: WorkplaceAddRequest,
    ):
        try:
            await self.db.coworkings.get_one(id=coworking_id)
        except ObjectNotFoundException as ex:
            raise CoworkingNotFoundException from ex 
        _workplace_data = WorkplaceAdd(coworking_id=coworking_id, **workplace_data.model_dump())
        workplace: Workplace = await self.db.workplaces.add(_workplace_data)

        workplaces_facilities_data = [
            WorkplaceFacilityAdd(workplace_id=workplace.id, facility_id=f_id) for f_id in workplace_data.facilities_ids
        ]
        if workplaces_facilities_data:
            await self.db.workplaces_facilities.add_bulk(workplaces_facilities_data)
        await self.db.commit()

    async def edit_workplace(
            self,
            coworking_id: int,
            workplace_id: int,
            workplace_data: WorkplaceAddRequest,
    ):
        await CoworkingService(self.db).get_coworking_with_check(coworking_id)
        await self.get_workplace_with_check(workplace_id)
        _workplace_data = WorkplaceAdd(coworking_id=coworking_id, **workplace_data.model_dump())
        await self.db.workplaces.edit(_workplace_data, id=workplace_id)
        await self.db.workplaces_facilities.set_workplace_facilities(workplace_id, facilities_ids=workplace_data.facilities_ids)
        await self.db.commit()

    async def partially_edit_workplace(
            self,
            coworking_id: int,
            workplace_id: int,
            workplace_data: WorkplacePatchRequest,
    ):
        await CoworkingService(self.db).get_coworking_with_check(coworking_id)
        await self.get_workplace_with_check(workplace_id)

        _workplace_data_dict = workplace_data.model_dump(exclude_unset=True)
        _workplace_data = WorkplacePatch(coworking_id=coworking_id, **_workplace_data_dict)
        await self.db.workplaces.edit(_workplace_data, exclude_unset=True, id=workplace_id, coworking_id=coworking_id)
        if "facilities_ids" in _workplace_data_dict:
            await self.db.workplaces_facilities.set_workplace_facilities(
                workplace_id, facilities_ids=_workplace_data_dict["facilities_ids"]
            )
        await self.db.commit()

    async def delete_workplace(self, coworking_id: int, workplace_id: int):
        await CoworkingService(self.db).get_coworking_with_check(coworking_id)
        await self.get_workplace_with_check(workplace_id)
        await self.db.workplaces.delete(id=workplace_id, coworking_id=coworking_id)
        await self.db.commit()

    async def get_workplace_with_check(self, workplace_id: int) -> Workplace:
        try:
            return await self.db.workplaces.get_one(id=workplace_id)
        except ObjectNotFoundException:
            raise WorkplaceNotFoundException
