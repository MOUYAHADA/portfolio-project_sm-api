#!/usr/bin/env python3
"""
Module for general config settings
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings"""

    db_username: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
