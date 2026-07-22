import pytest
from httpx import AsyncClient

from src.utils.db_manager import DBManager
from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "workplace_id, datetime_from, datetime_to, status_code",
    [
        (1, "2026-08-01T09:00", "2026-08-10T18:00", 200),
        (1, "2026-08-02T09:00", "2026-08-11T18:00", 200),
        (1, "2026-08-03T09:00", "2026-08-12T18:00", 200),
        (1, "2026-08-04T09:00", "2026-08-13T18:00", 200),
        (1, "2026-08-05T09:00", "2026-08-14T18:00", 200),
        (1, "2026-08-06T09:00", "2026-08-15T18:00", 409),
        (1, "2026-08-17T09:00", "2026-08-25T18:00", 200),
    ],
)
async def test_add_booking(
    workplace_id,
    datetime_from,
    datetime_to,
    status_code,
    db: DBManager,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "workplace_id": workplace_id,
            "datetime_from": datetime_from,
            "datetime_to": datetime_to,
        },
    )

    assert response.status_code == status_code

    if status_code == 200:
        res = response.json()

        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "workplace_id, datetime_from, datetime_to, booked_workplaces",
    [
        (1, "2026-08-01T09:00", "2026-08-10T18:00", 1),
        (1, "2026-08-02T09:00", "2026-08-11T18:00", 2),
        (1, "2026-08-03T09:00", "2026-08-12T18:00", 3),
    ],
)
async def test_add_and_get_my_bookings(
    workplace_id,
    datetime_from,
    datetime_to,
    booked_workplaces,
    delete_all_bookings,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "workplace_id": workplace_id,
            "datetime_from": datetime_from,
            "datetime_to": datetime_to,
        },
    )

    assert response.status_code == 200

    response_my_bookings = await authenticated_ac.get("/bookings/me")

    assert response_my_bookings.status_code == 200
    assert len(response_my_bookings.json()) == booked_workplaces