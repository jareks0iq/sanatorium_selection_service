from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    environment: Literal["dev", "prod"] = "dev"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
