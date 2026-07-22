from datetime import datetime

from sqlalchemy import select, func

from src.models.workplaces import WorkplacesOrm
from src.repositories.base import BaseRepository
from src.models.coworkings import CoworkingsOrm
from src.repositories.mappers.mappers import CoworkingDataMapper
from src.repositories.utils import workplaces_ids_for_booking
from src.schemas.coworkings import Coworking


class CoworkingsRepository(BaseRepository):
    model = CoworkingsOrm
    mapper = CoworkingDataMapper

    async def get_filtered_by_time(
        self,
        datetime_from: datetime,
        datetime_to: datetime,
        location,
        title,
        limit,
        offset,
    ) -> list[Coworking]:
        workplaces_ids_to_get = workplaces_ids_for_booking(datetime_from=datetime_from, datetime_to=datetime_to)
        coworkings_ids_to_get = (
            select(WorkplacesOrm.coworking_id)
            .select_from(WorkplacesOrm)
            .filter(WorkplacesOrm.id.in_(workplaces_ids_to_get))
        )

        query = select(CoworkingsOrm).filter(CoworkingsOrm.id.in_(coworkings_ids_to_get))
        if location:
            query = query.filter(func.lower(CoworkingsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(CoworkingsOrm.title).contains(title.strip().lower()))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(coworking) for coworking in result.scalars().all()]
