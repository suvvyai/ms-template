from typing import Any

from beanie import init_beanie
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from core import settings


async def initialize_database() -> None:
    logger.info("Initialising DB...")
    kwargs: dict[str, Any] = {}
    if settings.mongo.cert_file_path:
        kwargs |= {"tlsCAFile": settings.mongo.cert_file_path}

    await init_beanie(
        database=AsyncIOMotorClient(settings.mongo.url, **kwargs).get_database(settings.mongo.db_name),
        document_models=[],
    )
    logger.success("DB is ready!")
