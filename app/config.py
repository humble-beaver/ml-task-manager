"""Compose environment loader
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv


class Settings(BaseSettings):
    """Database settings class

    :param BaseSettings: pydantic base settings class
    :type BaseSettings: class
    """
    load_dotenv()
    db_url: str = Field(validation_alias='DATABASE_URL')
    folder: str = Field(validation_alias='FOLDER')


settings = Settings()
