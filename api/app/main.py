from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, Request, Depends
from responses import ORJSONResponse, EntriesResponse
from src import Entry, get_db_engine, Model, Encoder

from sqlmodel import Session, select
import uuid
import os
from sqlalchemy import func


data_dir = Path("/data/models").absolute()
model_name = os.environ.get("MODEL_NAME", list(data_dir.iterdir())[-1])
model = Model(path=data_dir / model_name / "model.pkl")
encoder = Encoder(path=data_dir / model_name / "encoder.pkl")

app = FastAPI(default_response_class=ORJSONResponse)

engine = get_db_engine(
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    db_name=os.environ["POSTGRES_DB"],
)


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/health-check")
def health_check():
    return {"status": "healthy"}


@app.get("/entries/", response_model=EntriesResponse)
def read_entries(
    request: Request,
    session: Session = Depends(get_session),
    page: int = 1,
    pageSize: int = Query(default=10, le=100),
):
    offset = (page - 1) * pageSize
    entries = session.exec(select(Entry).offset(offset).limit(pageSize)).all()
    totalEntries = session.exec(select([func.count(Entry.id)])).one()
    response = {"entries": entries, "totalEntries": totalEntries}
    if offset + pageSize < totalEntries:
        response["nextPage"] = request.url.replace_query_params(
            page=page + 1, pageSize=pageSize
        )._url
    return response


@app.get("/entries/{entry_id}", response_model=Entry)
def read_entry(entry_id: uuid.UUID, session: Session = Depends(get_session)):
    entry = session.get(Entry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@app.get("/ships/{shipImo}", response_model=EntriesResponse)
def read_ships(
    shipImo: int,
    request: Request,
    session: Session = Depends(get_session),
    page: int = 1,
    pageSize: int = Query(default=10, le=100),
):
    offset = (page - 1) * pageSize
    entries = session.exec(
        select(Entry)
        .where(Entry.shipImo == shipImo)
        .offset(offset)
        .limit(pageSize)
    ).all()

    totalEntries = session.exec(
        select([func.count(Entry.id)]).where(Entry.shipImo == shipImo)
    ).one()

    response = {"entries": entries, "totalEntries": totalEntries}
    if offset + pageSize < totalEntries:
        response["nextPage"] = request.url.replace_query_params(
            page=page + 1, pageSize=pageSize
        )._url
    return response


@app.get("/encode")
async def _encode(entry: Entry):
    encoded = encoder.transform([entry])
    return encoded.tolist()


@app.get("/predict")
async def _predict(entry: Entry):
    encoded = encoder.transform([entry])
    result = model.predict(encoded)
    return result.tolist()
