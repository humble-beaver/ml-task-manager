"""Database configuration file
"""
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Database settings class

    :param BaseSettings: pydantic base settings class
    :type BaseSettings: class
    """
    db_url: str = Field(..., env='DATABASE_URL')


settings = Settings()
