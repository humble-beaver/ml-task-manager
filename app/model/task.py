"""Task Model Class"""
from sqlmodel import SQLModel, Field


class TaskBase(SQLModel):
    """Base model class

    :param SQLModel: Default SQLModel class
    :type SQLModel: obj
    """
    dominion: str
    backend: str
    dataset: str
    container_name: str
    train_script: str
    out_path: str


class Task(TaskBase, table=True):
    """Task class that will generate the database

    :param TaskBase: The base model class
    :type TaskBase: SQLModel
    :param table: SQLModel param to declare as a table, defaults to True
    :type table: bool, optional
    """
    id: int | None = Field(default=None, primary_key=True)


class TaskCreate(TaskBase):
    """Task class that will be returned upon instance creation

    :param TaskBase: The base model class
    :type TaskBase: SQLModel
    """
    pass


class TaskRead(TaskBase):
    """Task class that will be returned upon get status requests

    :param TaskBase: The base model class
    :type TaskBase: SQLModel
    """
    id: int
