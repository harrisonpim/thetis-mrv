from sqlmodel import SQLModel, create_engine


def get_db_engine(user: str, password: str, db_name: str):
    engine = create_engine(
        f"postgresql://{user}:{password}@postgres:5432/{db_name}"
    )
    SQLModel.metadata.create_all(engine)
    return engine
