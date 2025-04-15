from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from core import settings
from core.errors import SuvvyError


async def microservice_auth(
    api_key: Annotated[str, Depends(APIKeyHeader(name="Microservice-Api-Key"))],
) -> None:
    if api_key != settings.microservices.key:
        raise SuvvyError.AUTH_INVALID_TOKEN.as_exception()


MicroserviceAuth = Depends(microservice_auth)
