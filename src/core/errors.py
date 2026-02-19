"""Модуль ошибок приложения."""

from enum import auto

from fastapi_enum_errors import ErrorEnum


class SuvvyError(ErrorEnum):
    """
    Перечисление ошибок приложения.

    Каждая ошибка содержит уникальный код и HTTP статус.
    Используется с библиотекой ``fastapi-enum-errors``.
    """

    AUTH_INVALID_TOKEN = (auto(), 401)
    """Неверный токен аутентификации."""

    @classmethod
    def error_response_models(cls) -> dict:
        """Возвращает модели ответов для OpenAPI документации."""
        return {}
