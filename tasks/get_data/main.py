import os
from src.models import Entry, row_to_entry
import pandas as pd
import httpx
from pathlib import Path
from loguru import logger
import sys
from sqlmodel import create_engine, Session, SQLModel

logger.remove()
logger.add(sys.stderr, format="{time} | {level} | {message} | {extra}")


data_url = "https://mrv.emsa.europa.eu/api/public-emission-report/reporting-period-document/binary/"
data_dir = Path("/data/raw").absolute()
if not data_dir.exists():
    data_dir.mkdir(parents=True, exist_ok=True)

year = 2018
while True:
    file_path = data_dir / f"{year}.xlsx"
    if file_path.exists():
        logger.info(f"{year}.xlsx already exists.")
    else:
        response = httpx.get(data_url + str(year))
        if response.status_code == 200:
            logger.info(f"Downloading {year}.xlsx")
            with open(file_path, "wb") as f:
                f.write(response.content)
        else:
            break
    year += 1
logger.info("Downloaded all data files from source")


logger.info("Opening session with database")

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
db = os.environ["POSTGRES_DB"]
engine = create_engine(f"postgresql://{user}:{password}@postgres:5432/{db}")

SQLModel.metadata.create_all(engine)

session = Session(engine)

for file in data_dir.iterdir():
    logger.info(f"Reading data from {file}")
    df = pd.read_excel(file, header=2)
    for i in range(len(df)):
        try:
            data = df.loc[i]
            entry: Entry = row_to_entry(data)
            session.add(entry)
            session.commit()
            logger.info(f"Processed {i}")
        except ValueError as _:
            logger.exception(f"Error on {i}", dict(data))
