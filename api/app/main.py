import os
from fastapi import FastAPI, HTTPException, Query, Request
from responses import ORJSONResponse, EntriesResponse
from src import Entry, get_db_engine

from sqlmodel import Session, select


app = FastAPI(default_response_class=ORJSONResponse)

engine = get_db_engine(
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    db_name=os.environ["POSTGRES_DB"],
)


@app.get("/health-check")
def health_check():
    return {"status": "healthy"}


@app.get("/entries/", response_model=EntriesResponse)
def read_entries(
    request: Request, page: int = 1, pageSize: int = Query(default=10, lte=100)
):
    offset = (page - 1) * pageSize
    with Session(engine) as session:
        return {
            "entries": session.exec(
                select(Entry).offset(offset).limit(pageSize)
            ).all(),
            "nextPage": request.url.replace_query_params(
                page=page + 1, pageSize=pageSize
            )._url,
        }


@app.get("/entries/{entry_id}", response_model=Entry)
def read_entry(entry_id: int):
    with Session(engine) as session:
        entry = session.get(Entry, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Entry not found")
        return entry


@app.get("/ships/{shipImo}", response_model=EntriesResponse)
def read_ships(
    shipImo: str,
    request: Request,
    page: int = 1,
    pageSize: int = Query(default=10, lte=100),
):
    offset = (page - 1) * pageSize
    with Session(engine) as session:
        return {
            "entries": session.exec(
                select(Entry)
                .where(Entry.shipImo == shipImo)
                .offset(offset)
                .limit(pageSize)
            ).all(),
            "nextPage": request.url.replace_query_params(
                page=page + 1, pageSize=pageSize
            )._url,
        }
