from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    TILE38_URI: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
