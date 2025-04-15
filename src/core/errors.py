from enum import auto

from fastapi_enum_errors import ErrorEnum, classproperty


class SuvvyError(ErrorEnum):
    AUTH_INVALID_TOKEN = (auto(), 401)
    """Неверный токен"""

    @classproperty
    def error_response_models(cls) -> dict:
        return {}
