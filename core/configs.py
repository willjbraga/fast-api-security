from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):

    API_V1_STR: str = '/api/v1'
    DB_URL: str
    DBBaseModel = declarative_base()

    JWT_SECRET: str
    ALGORITHM: str = 'HS256'

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 4

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings: Settings = Settings()