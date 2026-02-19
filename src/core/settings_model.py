"""Модуль настроек приложения через переменные окружения."""

from typing import Annotated

from pydantic import BaseModel, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseModel):
    """Настройки подключения к MongoDB."""

    url: Annotated[str, MongoDsn]
    db_name: str
    cert_file_path: str | None = None


class MicroservicesSettings(BaseModel):
    """Настройки аутентификации микросервисов."""

    key: str


class ServerSettings(BaseModel):
    """Настройки сервера."""

    workers: int = 1


class Settings(BaseSettings):
    """
    Главный класс настроек приложения.

    Загружает настройки из переменных окружения с разделителем ``__``.
    Пример: ``MONGO__URL``, ``MICROSERVICES__KEY``.
    """

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        extra="ignore",
    )

    mongo: MongoSettings
    microservices: MicroservicesSettings
    server: ServerSettings = ServerSettings()


settings = Settings()  # type: ignore[call-arg]
