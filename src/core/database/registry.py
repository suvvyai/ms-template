"""Модуль инициализации базы данных MongoDB."""

from typing import Any

from beanie import init_beanie
from loguru import logger
from pymongo import AsyncMongoClient

from core import settings


async def initialize_database() -> None:
    """
    Инициализирует подключение к MongoDB через Beanie ODM.

    Создаёт асинхронное подключение к MongoDB и инициализирует Beanie
    с указанными моделями документов.

    :raises ConnectionError: если не удалось подключиться к базе данных
    """
    logger.info("Initialising DB...")
    kwargs: dict[str, Any] = {}
    if settings.mongo.cert_file_path:
        kwargs |= {"tlsCAFile": settings.mongo.cert_file_path}

    await init_beanie(
        database=AsyncMongoClient(settings.mongo.url, **kwargs).get_database(settings.mongo.db_name),
        document_models=[],
    )
    logger.success("DB is ready!")
