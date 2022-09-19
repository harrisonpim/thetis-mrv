import os

import orjson
from sqlmodel import Session, func, select

from src import Entry, get_db_engine

engine = get_db_engine(
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    db_name=os.environ["POSTGRES_DB"],
)
with Session(engine) as session:
    entry = session.exec(
        select(
            Entry.totalFuelConsumption,
            Entry.onLadenFuelConsumption,
            Entry.totalCo2Emissions,
            Entry.betweenMSJurisdictionPortsCo2Emissions,
            Entry.fromMSJurisdictionPortsCo2Emissions,
            Entry.toMSJurisdictionPortsCo2Emissions,
            Entry.atBerthMSJurisdictionPortsCo2Emissions,
            Entry.passengerCo2Emissions,
            Entry.freightCo2Emissions,
            Entry.onLadenCo2Emissions,
            Entry.annualTotalTimeSpentAtSeaHours,
            Entry.fuelConsumptionPerDistance,
            Entry.fuelConsumptionPerTransportWorkMass,
            Entry.fuelConsumptionPerTransportWorkVolume,
            Entry.fuelConsumptionPerTransportWorkDwt,
            Entry.fuelConsumptionPerTransportWorkPax,
            Entry.fuelConsumptionPerTransportWorkFreight,
            Entry.Co2EmissionsPerDistance,
            Entry.Co2EmissionsPerTransportWorkMass,
            Entry.Co2EmissionsPerTransportWorkVolume,
            Entry.Co2EmissionsPerTransportWorkDwt,
            Entry.Co2EmissionsPerTransportWorkPax,
            Entry.Co2EmissionsPerTransportWorkFreight,
            Entry.shipType,
        ).order_by(func.random())
    ).first()

with open("/data/random_entry.json", "w") as f:
    f.write(orjson.dumps(dict(entry)).decode("utf-8"))
