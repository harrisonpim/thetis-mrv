import os
from datetime import datetime
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sqlmodel import Session, select

from src import Encoder, Entry, Model, get_db_engine, get_logger

log = get_logger()

timestamp = datetime.now().isoformat(timespec="seconds")

engine = get_db_engine(
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    db_name=os.environ["POSTGRES_DB"],
)

model_dir = Path("/data/models").absolute() / timestamp
model_dir.mkdir(parents=True, exist_ok=True)


log.info("Fetching data from database")
with Session(engine) as session:
    entries = session.exec(
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
        )
    ).all()
log.info(f"Fetched {len(entries)} entries")


log.info("Fitting an encoder to the data, and encoding data for training")
encoder = Encoder()
X, y = encoder.fit_transform(entries)

encoder_path = model_dir / "encoder.pkl"
encoder.save(encoder_path)
log.info(f"Encoder saved to: {encoder_path}")


log.info("Splitting data into training, testing, and validation sets")
X_train, X_leftover, y_train, y_leftover = train_test_split(
    X, y, test_size=0.33, random_state=16, stratify=y
)

X_validation, X_test, y_validation, y_test = train_test_split(
    X_leftover, y_leftover, test_size=0.5, random_state=16, stratify=y_leftover
)

log.info("Saving datasets")
np.save(model_dir / "X_train", X_train)
np.save(model_dir / "X_test", X_test)
np.save(model_dir / "X_validation", X_validation)
np.save(model_dir / "y_train", y_train)
np.save(model_dir / "y_test", y_test)
np.save(model_dir / "y_validation", y_validation)


log.info("Training model")
model = Model()
model.train(X_train, y_train)
model_path = model_dir / "model.pkl"
model.save(model_path)
log.info(f"Model saved to: {model_path}")

log.info("Predicting on test set")
y_pred = model.predict(X_test)
log.info(f"{y_test.shape}, {y_pred.shape}")
log.info(f"{y_pred[0]}")

log.info("Evaluating model")
log.info(f"Accuracy: {accuracy_score(y_test, y_pred)}")
