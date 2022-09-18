from time import sleep

import psycopg2
from sqlalchemy import exc
from sqlmodel import SQLModel, create_engine

from .log import get_logger

log = get_logger()


def get_db_engine(user: str, password: str, db_name: str):
    try:
        engine = create_engine(
            f"postgresql://{user}:{password}@postgres:5432/{db_name}"
        )
        SQLModel.metadata.create_all(engine)
        return engine
    except (psycopg2.OperationalError, exc.OperationalError):
        log.error("Waiting for database to start...")
        sleep(1)
        return get_db_engine(user, password, db_name)


def clear_db():
    pass
