from enum import auto

from fastapi_enum_errors import ErrorEnum


class SuvvyError(ErrorEnum):
    AUTH_INVALID_TOKEN = (auto(), 401)
    """Неверный токен"""

    @classmethod
    def error_response_models(cls) -> dict:
        return {}
