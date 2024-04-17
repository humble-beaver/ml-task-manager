"""Task Model Class"""
from sqlmodel import SQLModel, Field


class TaskBase(SQLModel):
    """Task base model class

    :param SQLModel: Default SQLModel class
    :type SQLModel: obj
    """
    dominion: str
    backend: str
    account: str
    num_instances: int
    dataset: str
    container_name: str
    train_script: str
    in_path: str
    out_path: str


class Task(TaskBase, table=True):
    """Task class that will generate the table in database

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


class TaskRead(TaskBase):
    """Task class that will be returned upon get status requests

    :param TaskBase: The base model class
    :type TaskBase: SQLModel
    """
    id: int
