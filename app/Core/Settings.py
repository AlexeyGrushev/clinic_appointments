from functools import lru_cache
from typing import ClassVar

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }
    # APP SETTINGS
    APP_NAME: str
    APP_PREFIX: str
    APP_HOST: str
    APP_PORT: int
    APP_LOGGER_NAME: str

    # DB SETTINGS
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_URL: str = ""

    LOG_LEVEL: str = "INFO"

    @model_validator(mode="before")
    @classmethod
    def get_database_url(cls, v):
        v["DB_URL"] = (
            "postgresql+asyncpg://"
            + f"{v["DB_USER"]}:{v["DB_PASS"]}@"
            + f"{v["DB_HOST"]}:{v["DB_PORT"]}/{v["DB_NAME"]}"
        )
        return v


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore


settings = get_settings()
