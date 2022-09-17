import os
from fastapi import FastAPI, HTTPException
from src import get_db_engine, Entry

from sqlmodel import Session, select
from typing import List


app = FastAPI()

engine = get_db_engine(
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    db_name=os.environ["POSTGRES_DB"],
)


@app.get("/health-check")
def health_check():
    return {"status": "healthy"}


@app.get("/entries/", response_model=List[Entry])
def read_entries():
    with Session(engine) as session:
        entries = session.exec(select(Entry)).first()
        return [entries]


@app.get("/entries/{entry_id}")
def read_entry(entry_id: int):
    with Session(engine) as session:
        entry = session.get(Entry, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return entry
