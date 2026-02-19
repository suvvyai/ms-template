"""Модуль аутентификации микросервисов."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from core import settings
from core.errors import SuvvyError


async def microservice_auth(
    api_key: Annotated[str, Depends(APIKeyHeader(name="Microservice-Api-Key"))],
) -> None:
    """
    Проверяет API ключ микросервиса.

    :param api_key: API ключ из заголовка ``Microservice-Api-Key``
    :raises SuvvyError.AUTH_INVALID_TOKEN: если ключ неверный
    """
    if api_key != settings.microservices.key:
        raise SuvvyError.AUTH_INVALID_TOKEN.as_exception()


MicroserviceAuth = Depends(microservice_auth)
"""Зависимость FastAPI для аутентификации микросервисов."""
