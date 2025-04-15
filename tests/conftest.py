from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from core import settings
from src.app.app import app


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient]:
    """Получить тестовый клиент"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        headers={"Microservice-Api-Key": settings.microservices.key},
    ) as client:
        yield client
