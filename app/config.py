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
    db_url: str = Field(validation_alias='DATABASE_URL')
    atena_root: str = Field(validation_alias='ATENA_ROOT')


load_dotenv()
settings = Settings()
