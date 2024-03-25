"""Task Model Class"""

from pydantic import BaseModel


class Task(BaseModel):
    """Task Model based on Pydantic BaseModel

    :param BaseModel: Pydantic base model for FastAPI features
    :type BaseModel: pydantic.BaseModel
    """
    backend: str
    data_path: str
    domain_group: str
    script_path: str
