"""Database utilities module"""
from sqlmodel import create_engine, SQLModel

# DATABASE_URL = os.environ.get("")
DATABASE_URL = "./app/data/mtm.db"
SQLITE_URL = f"sqlite:///{DATABASE_URL}"
connect_args = {"check_same_thread": False}
engine = create_engine(SQLITE_URL, echo=True, connect_args=connect_args)


def init_db():
    """Initialize database creation
    """
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
