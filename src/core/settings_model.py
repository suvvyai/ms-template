from typing import Annotated

from pydantic import BaseModel, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseModel):
    url: Annotated[str, MongoDsn]
    db_name: str
    cert_file_path: str | None = None


class MicroservicesSettings(BaseModel):
    key: str


class ServerSettings(BaseModel):
    workers: int = 1


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        extra="ignore",
    )

    mongo: MongoSettings
    microservices: MicroservicesSettings
    server: ServerSettings = ServerSettings()


settings = Settings()  # type: ignore[call-arg]
