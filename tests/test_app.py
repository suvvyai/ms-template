import random
import string

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("name", ["".join(random.choices(string.ascii_letters, k=10)) for _ in range(10)])
async def test_hello_world(client: AsyncClient, name: str) -> None:
    response = await client.post("/api/hi", json={"name": name})

    assert response.status_code == 200
    assert response.json() == {"greeting": f"Hello, {name}!"}
