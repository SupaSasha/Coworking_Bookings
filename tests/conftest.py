# ruff: noqa: E402
import json
from typing import AsyncGenerator
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest

from httpx import AsyncClient, ASGITransport

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *  # noqa
from src.schemas.coworkings import CoworkingAdd
from src.schemas.workplaces import WorkplaceAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_coworkings.json", encoding="utf-8") as file_coworkings:
        coworkings = json.load(file_coworkings)

    with open("tests/mock_workplaces.json", encoding="utf-8") as file_workplaces:
        workplaces = json.load(file_workplaces)

    coworkings = [
        CoworkingAdd.model_validate(coworking)
        for coworking in coworkings
    ]

    workplaces = [
        WorkplaceAdd.model_validate(workplace)
        for workplace in workplaces
    ]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.coworkings.add_bulk(coworkings)
        await db_.workplaces.add_bulk(workplaces)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac: AsyncClient, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "corben@dallas.com",
            "password": "1234",
        },
    )


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac: AsyncClient):
    await ac.post(
        "/auth/login",
        json={
            "email": "corben@dallas.com",
            "password": "1234",
        },
    )

    assert ac.cookies["access_token"]

    yield ac