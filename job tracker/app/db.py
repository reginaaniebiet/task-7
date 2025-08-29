from sqlmodel import SQLModel, Session, create_engine

SQLITE_URL = "sqlite:///./jobs.db"
engine = create_engine(SQLITE_URL, echo=False)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
