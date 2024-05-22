"""Database configuration file
"""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Database settings class

    :param BaseSettings: pydantic base settings class
    :type BaseSettings: class
    """
    db_url: str = Field(validation_alias='DATABASE_URL')


settings = Settings()
