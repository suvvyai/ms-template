from fastapi import Depends
from fastapi.openapi.models import APIKey, APIKeyIn, SecurityBase
from fastapi.requests import Request

from core import settings
from core.errors import SuvvyError


class MicroserviceAuthentication(SecurityBase):
    model: APIKey = APIKey(name="Microservice-Api-Key", **{"in": APIKeyIn.header})  # type: ignore[arg-type]

    def __init__(self, api_key: str, scheme_name: str | None = None):
        self.api_key = api_key
        self.scheme_name = scheme_name or self.__class__.__name__

    def __call__(self, request: Request) -> None:
        header_api_key: str | None = request.headers.get("Microservice-Api-Key", None)
        if header_api_key is None or header_api_key != self.api_key:
            raise SuvvyError.AUTH_INVALID_TOKEN.as_exception()


MicroserviceAuth = Depends(MicroserviceAuthentication(api_key=settings.microservices.key))
