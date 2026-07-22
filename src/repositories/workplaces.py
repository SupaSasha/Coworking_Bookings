from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.exceptions import WorkplaceNotFoundException
from src.repositories.base import BaseRepository
from src.models.workplaces import WorkplacesOrm
from src.repositories.mappers.mappers import WorkplaceDataMapper, WorkplaceDataWithRelsMapper
from src.repositories.utils import workplaces_ids_for_booking


class WorkplacesRepository(BaseRepository):
    model: WorkplacesOrm = WorkplacesOrm
    mapper = WorkplaceDataMapper

    async def get_filtered_by_time(
        self,
        coworking_id,
        datetime_from: date,
        datetime_to: date,
    ):
        workplaces_ids_to_get = workplaces_ids_for_booking(datetime_from, datetime_to, coworking_id)

        query = (
            select(self.model)  # type: ignore
            .options(selectinload(WorkplacesOrm.facilities))
            .filter(WorkplacesOrm.id.in_(workplaces_ids_to_get))  # type: ignore
        )
        result = await self.session.execute(query)
        return [
            WorkplaceDataWithRelsMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_with_rels(self, **filter_by):
        query = (
            select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by)  # type: ignore
        )
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise WorkplaceNotFoundException
        return WorkplaceDataWithRelsMapper.map_to_domain_entity(model)
