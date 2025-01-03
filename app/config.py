from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings"""

    db_username: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    class Config:
        env_file = ".env"


settings = Settings
settings.db_url = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
