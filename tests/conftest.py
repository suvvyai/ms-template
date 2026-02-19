import asyncio
from asyncio import AbstractEventLoop
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from pymongo import AsyncMongoClient

from app.app import app
from core import settings
from core.database import initialize_database


@pytest.fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    """Ивент луп"""
    return asyncio.get_event_loop()


@pytest.fixture(autouse=True, scope="session")
async def init_db() -> None:
    """Ининциализировать базу данных"""
    await initialize_database()


@pytest.fixture(autouse=True)
async def drop_db() -> None:
    """Дропнуть бд перед каждым тестом."""
    if not settings.mongo.db_name.lower().endswith("test"):
        msg = f"Попытка запустить тесты с продакшн БД: {settings.mongo.db_name}. Используйте БД с суффиксом 'test'"
        raise RuntimeError(msg)

    await AsyncMongoClient(settings.mongo.url).drop_database(settings.mongo.db_name)

    # TODO(template): сюда добавлять Redis и прочее  # noqa: FIX002


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient]:
    """Получить тестовый клиент"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        headers={"Microservice-Api-Key": settings.microservices.key},
    ) as client:
        yield client
