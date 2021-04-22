from pydantic import BaseSettings


class Settings(BaseSettings):
    TILE38_URI: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
