from datetime import datetime

from sqlalchemy import select, func, Select

from src.models.bookings import BookingsOrm
from src.models.workplaces import WorkplacesOrm


def workplaces_ids_for_booking(
    datetime_from: datetime,
    datetime_to: datetime,
    coworking_id: int | None = None,
) -> Select:

    workplaces_count = (
        select(
            BookingsOrm.workplace_id,
            func.count("*").label("workplaces_booked"),
        )
        .select_from(BookingsOrm)
        .filter(
            BookingsOrm.datetime_from < datetime_to,
            BookingsOrm.datetime_to > datetime_from,
        )
        .group_by(BookingsOrm.workplace_id)
        .cte(name="workplaces_count")
    )

    workplaces_left_table = (
        select(
            WorkplacesOrm.id.label("workplace_id"),
            (
                WorkplacesOrm.quantity
                - func.coalesce(workplaces_count.c.workplaces_booked, 0)
            ).label("workplaces_left"),
        )
        .select_from(WorkplacesOrm)
        .outerjoin(
            workplaces_count,
            WorkplacesOrm.id == workplaces_count.c.workplace_id,
        )
        .cte(name="workplaces_left_table")
    )

    workplaces_ids_for_coworking = select(WorkplacesOrm.id)

    if coworking_id is not None:
        workplaces_ids_for_coworking = workplaces_ids_for_coworking.filter_by(
            coworking_id=coworking_id
        )

    workplaces_ids_to_get = (
        select(workplaces_left_table.c.workplace_id)
        .select_from(workplaces_left_table)
        .where(
            workplaces_left_table.c.workplaces_left > 0,
            workplaces_left_table.c.workplace_id.in_(
                workplaces_ids_for_coworking
            ),
        )
    )

    return workplaces_ids_to_get