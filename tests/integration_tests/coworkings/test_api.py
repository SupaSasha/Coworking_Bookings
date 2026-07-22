from httpx import AsyncClient


async def test_get_coworkings(ac: AsyncClient):
    response = await ac.get(
        "/coworkings",
        params={
            "datetime_from": "2026-08-01",
            "datetime_to": "2026-08-10",
        },
    )
    print(f"{response.json()=}")

    assert response.status_code == 200
