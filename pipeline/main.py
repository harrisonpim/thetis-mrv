import os
from pathlib import Path

import httpx
import numpy as np
import pandas as pd
from sqlmodel import Session

from src import Entry, get_db_engine, get_logger, row_to_entry

log = get_logger()

data_url = "https://mrv.emsa.europa.eu/api/public-emission-report/reporting-period-document/binary/"

data_dir = Path("/data/raw").absolute()
postgres_dir = Path("/data/postgres").absolute()

data_dir.mkdir(parents=True, exist_ok=True)
postgres_dir.mkdir(parents=True, exist_ok=True)

year = 2018
while True:
    file_path = data_dir / f"{year}.xlsx"
    if file_path.exists():
        log.info(f"{year}.xlsx already exists.")
    else:
        response = httpx.get(data_url + str(year))
        if response.status_code == 200:
            log.info(f"Downloading {year}.xlsx")
            with open(file_path, "wb") as f:
                f.write(response.content)
        else:
            break
    year += 1
log.info("Downloaded all data files from source")

log.info("Opening session with database")
engine = get_db_engine(
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    db_name=os.environ["POSTGRES_DB"],
)
session = Session(engine)

for file in data_dir.iterdir():
    log.info(f"Reading data from {file}")
    df = pd.read_excel(file, header=2)
    df = (
        df.replace("", np.nan)
        .replace("N/A", np.nan)
        .replace("Division by zero!", np.nan)
    )
    for i in range(len(df)):
        try:
            data = df.loc[i]
            entry: Entry = row_to_entry(data)
            session.add(entry)
            session.commit()
            log.info(f"Processed {i}")
        except ValueError as _:
            log.exception(f"Error on {i}", dict(data))
