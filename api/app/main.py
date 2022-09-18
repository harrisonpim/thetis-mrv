import orjson
import os
from fastapi import FastAPI, HTTPException, responses
from src import get_db_engine, Entry, Ship

from sqlmodel import Session, select
from typing import List, Any


class ORJSONResponse(responses.JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)


app = FastAPI(default_response_class=ORJSONResponse)

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


@app.get("/entries/{entry_id}", response_model=Entry)
def read_entry(entry_id: int):
    with Session(engine) as session:
        entry = session.get(Entry, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return entry


@app.get("/ships/", response_model=List[Ship])
def read_ships():
    with Session(engine) as session:
        return {}


@app.get("/ships/{ship_id}", response_model=List[Ship])
def read_ships():
    with Session(engine) as session:
        return {}
