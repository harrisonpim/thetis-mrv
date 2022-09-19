import pickle
from textwrap import fill
from typing import List, Optional

import numpy as np
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

from sklearn.impute import SimpleImputer

from .. import Entry

class ContinuousEncoder:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.imputer = SimpleImputer(
            missing_values=np.nan, strategy='constant', fill_value=0
        )

    def fit(self, data):
        self.scaler.fit(data)
        self.imputer.fit(data)
        return self

    def transform(self, data):
        is_none = np.isnan(data.astype(float)).astype(int)
        scaled = self.scaler.transform(self.imputer.transform(data))
        return np.stack([scaled, is_none], axis=1).reshape(-1, 2)

    def fit_transform(self, data):
        self.fit(data)
        return self.transform(data)



class Encoder:
    def __init__(self, path: Optional[str] = None):
        self.totalFuelConsumption_encoder = ContinuousEncoder()
        self.onLadenFuelConsumption_encoder = ContinuousEncoder()
        self.totalCo2Emissions_encoder = ContinuousEncoder()
        self.betweenMSJurisdictionPortsCo2Emissions_encoder = ContinuousEncoder()
        self.fromMSJurisdictionPortsCo2Emissions_encoder = ContinuousEncoder()
        self.toMSJurisdictionPortsCo2Emissions_encoder = ContinuousEncoder()
        self.atBerthMSJurisdictionPortsCo2Emissions_encoder = ContinuousEncoder()
        self.passengerCo2Emissions_encoder = ContinuousEncoder()
        self.freightCo2Emissions_encoder = ContinuousEncoder()
        self.onLadenCo2Emissions_encoder = ContinuousEncoder()
        self.annualTotalTimeSpentAtSeaHours_encoder = ContinuousEncoder()
        self.fuelConsumptionPerDistance_encoder = ContinuousEncoder()
        self.fuelConsumptionPerTransportWorkMass_encoder = ContinuousEncoder()
        self.fuelConsumptionPerTransportWorkVolume_encoder = ContinuousEncoder()
        self.fuelConsumptionPerTransportWorkDwt_encoder = ContinuousEncoder()
        self.fuelConsumptionPerTransportWorkPax_encoder = ContinuousEncoder()
        self.fuelConsumptionPerTransportWorkFreight_encoder = ContinuousEncoder()
        self.Co2EmissionsPerDistance_encoder = ContinuousEncoder()
        self.Co2EmissionsPerTransportWorkMass_encoder = ContinuousEncoder()
        self.Co2EmissionsPerTransportWorkVolume_encoder = ContinuousEncoder()
        self.Co2EmissionsPerTransportWorkDwt_encoder = ContinuousEncoder()
        self.Co2EmissionsPerTransportWorkPax_encoder = ContinuousEncoder()
        self.Co2EmissionsPerTransportWorkFreight_encoder = ContinuousEncoder()
        self.shipType_OHE = OneHotEncoder()
        if path:
            self.load(path)

    def fit(self, entries: List[Entry]):
        self.shipType_OHE = self.shipType_OHE.fit(
            np.array([entry.shipType for entry in entries]).reshape(-1, 1)
        )
        self.totalFuelConsumption_encoder = self.totalFuelConsumption_encoder.fit(
            np.array([entry.totalFuelConsumption for entry in entries]).reshape(-1, 1)
        )
        self.onLadenFuelConsumption_encoder = self.onLadenFuelConsumption_encoder.fit(
            np.array([entry.onLadenFuelConsumption for entry in entries]).reshape(-1, 1)
        )
        self.totalCo2Emissions_encoder = self.totalCo2Emissions_encoder.fit(
            np.array([entry.totalCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        self.betweenMSJurisdictionPortsCo2Emissions_encoder = self.betweenMSJurisdictionPortsCo2Emissions_encoder.fit(
            np.array([entry.betweenMSJurisdictionPortsCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        self.fromMSJurisdictionPortsCo2Emissions_encoder = self.fromMSJurisdictionPortsCo2Emissions_encoder.fit(
            np.array([entry.fromMSJurisdictionPortsCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        self.toMSJurisdictionPortsCo2Emissions_encoder = self.toMSJurisdictionPortsCo2Emissions_encoder.fit(
            np.array([entry.toMSJurisdictionPortsCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        self.atBerthMSJurisdictionPortsCo2Emissions_encoder = self.atBerthMSJurisdictionPortsCo2Emissions_encoder.fit(
            np.array([entry.atBerthMSJurisdictionPortsCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        self.passengerCo2Emissions_encoder = self.passengerCo2Emissions_encoder.fit(
            np.array([entry.passengerCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        self.freightCo2Emissions_encoder = self.freightCo2Emissions_encoder.fit(
            np.array([entry.freightCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        self.onLadenCo2Emissions_encoder = self.onLadenCo2Emissions_encoder.fit(
            np.array([entry.onLadenCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        self.annualTotalTimeSpentAtSeaHours_encoder = self.annualTotalTimeSpentAtSeaHours_encoder.fit(
            np.array([entry.annualTotalTimeSpentAtSeaHours for entry in entries]).reshape(-1, 1)
        )
        self.fuelConsumptionPerDistance_encoder = self.fuelConsumptionPerDistance_encoder.fit(
            np.array([entry.fuelConsumptionPerDistance for entry in entries]).reshape(-1, 1)
        )
        self.fuelConsumptionPerTransportWorkMass_encoder = self.fuelConsumptionPerTransportWorkMass_encoder.fit(
            np.array([entry.fuelConsumptionPerTransportWorkMass for entry in entries]).reshape(-1, 1)
        )
        self.fuelConsumptionPerTransportWorkVolume_encoder = self.fuelConsumptionPerTransportWorkVolume_encoder.fit(
            np.array([entry.fuelConsumptionPerTransportWorkVolume for entry in entries]).reshape(-1, 1)
        )
        self.fuelConsumptionPerTransportWorkDwt_encoder = self.fuelConsumptionPerTransportWorkDwt_encoder.fit(
            np.array([entry.fuelConsumptionPerTransportWorkDwt for entry in entries]).reshape(-1, 1)
        )
        self.fuelConsumptionPerTransportWorkPax_encoder = self.fuelConsumptionPerTransportWorkPax_encoder.fit(
            np.array([entry.fuelConsumptionPerTransportWorkPax for entry in entries]).reshape(-1, 1)
        )
        self.fuelConsumptionPerTransportWorkFreight_encoder = self.fuelConsumptionPerTransportWorkFreight_encoder.fit(
            np.array([entry.fuelConsumptionPerTransportWorkFreight for entry in entries]).reshape(-1, 1)
        )
        self.Co2EmissionsPerDistance_encoder = self.Co2EmissionsPerDistance_encoder.fit(
            np.array([entry.Co2EmissionsPerDistance for entry in entries]).reshape(-1, 1)
        )
        self.Co2EmissionsPerTransportWorkMass_encoder = self.Co2EmissionsPerTransportWorkMass_encoder.fit(
            np.array([entry.Co2EmissionsPerTransportWorkMass for entry in entries]).reshape(-1, 1)
        )
        self.Co2EmissionsPerTransportWorkVolume_encoder = self.Co2EmissionsPerTransportWorkVolume_encoder.fit(
            np.array([entry.Co2EmissionsPerTransportWorkVolume for entry in entries]).reshape(-1, 1)
        )
        self.Co2EmissionsPerTransportWorkDwt_encoder = self.Co2EmissionsPerTransportWorkDwt_encoder.fit(
            np.array([entry.Co2EmissionsPerTransportWorkDwt for entry in entries]).reshape(-1, 1)
        )
        self.Co2EmissionsPerTransportWorkPax_encoder = self.Co2EmissionsPerTransportWorkPax_encoder.fit(
            np.array([entry.Co2EmissionsPerTransportWorkPax for entry in entries]).reshape(-1, 1)
        )
        self.Co2EmissionsPerTransportWorkFreight_encoder = self.Co2EmissionsPerTransportWorkFreight_encoder.fit(
            np.array([entry.Co2EmissionsPerTransportWorkFreight for entry in entries]).reshape(-1, 1)
        )

    def transform(self, entries: List[Entry]):
        encoded_y = self.shipType_OHE.transform(
            np.array([entry.shipType for entry in entries]).reshape(-1, 1)
        ).toarray()
        encoded_totalFuelConsumption = self.totalFuelConsumption_encoder.transform(
            np.array([entry.totalFuelConsumption for entry in entries]).reshape(-1, 1)
        )
        encoded_onLadenFuelConsumption = self.onLadenFuelConsumption_encoder.transform(
            np.array([entry.onLadenFuelConsumption for entry in entries]).reshape(-1, 1)
        )
        encoded_totalCo2Emissions = self.totalCo2Emissions_encoder.transform(
            np.array([entry.totalCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        encoded_betweenMSJurisdictionPortsCo2Emissions = self.betweenMSJurisdictionPortsCo2Emissions_encoder.transform(
            np.array([entry.betweenMSJurisdictionPortsCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        encoded_fromMSJurisdictionPortsCo2Emissions = self.fromMSJurisdictionPortsCo2Emissions_encoder.transform(
            np.array([entry.fromMSJurisdictionPortsCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        encoded_toMSJurisdictionPortsCo2Emissions = self.toMSJurisdictionPortsCo2Emissions_encoder.transform(
            np.array([entry.toMSJurisdictionPortsCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        encoded_atBerthMSJurisdictionPortsCo2Emissions = self.atBerthMSJurisdictionPortsCo2Emissions_encoder.transform(
            np.array([entry.atBerthMSJurisdictionPortsCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        encoded_passengerCo2Emissions = self.passengerCo2Emissions_encoder.transform(
            np.array([entry.passengerCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        encoded_freightCo2Emissions = self.freightCo2Emissions_encoder.transform(
            np.array([entry.freightCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        encoded_onLadenCo2Emissions = self.onLadenCo2Emissions_encoder.transform(
            np.array([entry.onLadenCo2Emissions for entry in entries]).reshape(-1, 1)
        )
        encoded_annualTotalTimeSpentAtSeaHours = self.annualTotalTimeSpentAtSeaHours_encoder.transform(
            np.array([entry.annualTotalTimeSpentAtSeaHours for entry in entries]).reshape(-1, 1)
        )
        encoded_fuelConsumptionPerDistance = self.fuelConsumptionPerDistance_encoder.transform(
            np.array([entry.fuelConsumptionPerDistance for entry in entries]).reshape(-1, 1)
        )
        encoded_fuelConsumptionPerTransportWorkMass = self.fuelConsumptionPerTransportWorkMass_encoder.transform(
            np.array([entry.fuelConsumptionPerTransportWorkMass for entry in entries]).reshape(-1, 1)
        )
        encoded_fuelConsumptionPerTransportWorkVolume = self.fuelConsumptionPerTransportWorkVolume_encoder.transform(
            np.array([entry.fuelConsumptionPerTransportWorkVolume for entry in entries]).reshape(-1, 1)
        )
        encoded_fuelConsumptionPerTransportWorkDwt = self.fuelConsumptionPerTransportWorkDwt_encoder.transform(
            np.array([entry.fuelConsumptionPerTransportWorkDwt for entry in entries]).reshape(-1, 1)
        )
        encoded_fuelConsumptionPerTransportWorkPax = self.fuelConsumptionPerTransportWorkPax_encoder.transform(
            np.array([entry.fuelConsumptionPerTransportWorkPax for entry in entries]).reshape(-1, 1)
        )
        encoded_fuelConsumptionPerTransportWorkFreight = self.fuelConsumptionPerTransportWorkFreight_encoder.transform(
            np.array([entry.fuelConsumptionPerTransportWorkFreight for entry in entries]).reshape(-1, 1)
        )
        encoded_Co2EmissionsPerDistance = self.Co2EmissionsPerDistance_encoder.transform(
            np.array([entry.Co2EmissionsPerDistance for entry in entries]).reshape(-1, 1)
        )
        encoded_Co2EmissionsPerTransportWorkMass = self.Co2EmissionsPerTransportWorkMass_encoder.transform(
            np.array([entry.Co2EmissionsPerTransportWorkMass for entry in entries]).reshape(-1, 1)
        )
        encoded_Co2EmissionsPerTransportWorkVolume = self.Co2EmissionsPerTransportWorkVolume_encoder.transform(
            np.array([entry.Co2EmissionsPerTransportWorkVolume for entry in entries]).reshape(-1, 1)
        )
        encoded_Co2EmissionsPerTransportWorkDwt = self.Co2EmissionsPerTransportWorkDwt_encoder.transform(
            np.array([entry.Co2EmissionsPerTransportWorkDwt for entry in entries]).reshape(-1, 1)
        )
        encoded_Co2EmissionsPerTransportWorkPax = self.Co2EmissionsPerTransportWorkPax_encoder.transform(
            np.array([entry.Co2EmissionsPerTransportWorkPax for entry in entries]).reshape(-1, 1)
        )
        encoded_Co2EmissionsPerTransportWorkFreight = self.Co2EmissionsPerTransportWorkFreight_encoder.transform(
            np.array([entry.Co2EmissionsPerTransportWorkFreight for entry in entries]).reshape(-1, 1)
        )
        encoded_X = np.concatenate(
            [
                encoded_totalFuelConsumption,
                encoded_onLadenFuelConsumption,
                encoded_totalCo2Emissions,
                encoded_betweenMSJurisdictionPortsCo2Emissions,
                encoded_fromMSJurisdictionPortsCo2Emissions,
                encoded_toMSJurisdictionPortsCo2Emissions,
                encoded_atBerthMSJurisdictionPortsCo2Emissions,
                encoded_passengerCo2Emissions,
                encoded_freightCo2Emissions,
                encoded_onLadenCo2Emissions,
                encoded_annualTotalTimeSpentAtSeaHours,
                encoded_fuelConsumptionPerDistance,
                encoded_fuelConsumptionPerTransportWorkMass,
                encoded_fuelConsumptionPerTransportWorkVolume,
                encoded_fuelConsumptionPerTransportWorkDwt,
                encoded_fuelConsumptionPerTransportWorkPax,
                encoded_fuelConsumptionPerTransportWorkFreight,
                encoded_Co2EmissionsPerDistance,
                encoded_Co2EmissionsPerTransportWorkMass,
                encoded_Co2EmissionsPerTransportWorkVolume,
                encoded_Co2EmissionsPerTransportWorkDwt,
                encoded_Co2EmissionsPerTransportWorkPax,
                encoded_Co2EmissionsPerTransportWorkFreight,
            ],
            axis=1,
        ).reshape(len(entries), -1)
        return encoded_X, encoded_y

    def fit_transform(self, entries: List[Entry]):
        self.fit(entries)
        return self.transform(entries)

    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    def load(self, path: str):
        with open(path, "rb") as f:
            self = pickle.load(f)
