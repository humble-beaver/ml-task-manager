"""Database utilities module"""
from sqlmodel import create_engine, SQLModel
from ..config import settings

engine = create_engine(settings.db_url, echo=True)


def init_db():
    """Initialize database creation
    """
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
