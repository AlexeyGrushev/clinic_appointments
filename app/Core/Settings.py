from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
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

    class Config:
        env_file = ".env"
        extra = "ignore"
        encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore


settings = get_settings()
