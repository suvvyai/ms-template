import random
import string
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


@pytest.mark.parametrize("name", ["".join(random.choices(string.ascii_letters, k=10)) for _ in range(10)])
async def test_hello_world(client: AsyncClient, name: str) -> None:
    response = await client.post("/api/hi", json={"name": name})

    assert response.status_code == 200
    assert response.json() == {"greeting": f"Hello, {name}!"}
