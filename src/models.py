import numpy as np
import pandas as pd
from datetime import datetime
from typing import Optional, Tuple

from sqlmodel import Field, SQLModel

# Entry class is very loosely based on the XML schema from
# https://portal.emsa.europa.eu/documents/10402/733966/Bulk_download_XSD_v4.10.1.zip/ed1d0ba8-ad92-f310-4889-7baeceece537


class Entry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shipImo: str
    shipName: str
    shipType: str
    reportingPeriod: int
    technicalEfficiencyLabel: Optional[str]
    technicalEfficiencyValue: Optional[float]
    portOfRegistry: Optional[str]
    shipHomePort: Optional[str]
    iceClassPolarCode: Optional[str]
    docIssueDate: datetime
    docExpiryDate: datetime
    verifierNumber: str
    verifierName: str
    verifierNab: str
    verifierAddress: str
    verifierCity: str
    verifierAccreditationNumber: str
    verifierCountry: str
    monitoringMethodA: bool
    monitoringMethodB: bool
    monitoringMethodC: bool
    monitoringMethodD: bool
    totalFuelConsumption: float
    onLadenFuelConsumption: float
    totalCo2Emissions: float
    betweenMSJurisdictionPortsCo2Emissions: float
    fromMSJurisdictionPortsCo2Emissions: float
    toMSJurisdictionPortsCo2Emissions: float
    atBerthMSJurisdictionPortsCo2Emissions: float
    passengerCo2Emissions: float
    freightCo2Emissions: float
    onLadenCo2Emissions: float
    annualTotalTimeSpentAtSeaHours: float
    fuelConsumptionPerDistance: float
    fuelConsumptionPerTransportWorkMass: float
    fuelConsumptionPerTransportWorkVolume: float
    fuelConsumptionPerTransportWorkDwt: float
    fuelConsumptionPerTransportWorkPax: float
    fuelConsumptionPerTransportWorkFreight: float
    Co2EmissionsPerDistance: float
    Co2EmissionsPerTransportWorkMass: float
    Co2EmissionsPerTransportWorkVolume: float
    Co2EmissionsPerTransportWorkDwt: float
    Co2EmissionsPerTransportWorkPax: float
    Co2EmissionsPerTransportWorkFreight: float
    distanceTravelledThroughIce: float
    totalTimeSpentAtSeaHours: float
    totalTimeSpentAtSeaThroughIceHours: float
    ladenFuelConsumptionPerDistance: float
    ladenFuelConsumptionPerTransportWorkMass: float
    ladenFuelConsumptionPerTransportWorkVolume: float
    ladenFuelConsumptionPerTransportWorkDwt: float
    ladenFuelConsumptionPerTransportWorkPax: float
    ladenFuelConsumptionPerTransportWorkFreight: float
    ladenCo2EmissionsPerDistance: float
    ladenCo2EmissionsPerTransportWorkMass: float
    ladenCo2EmissionsPerTransportWorkVolume: float
    ladenCo2EmissionsPerTransportWorkDwt: float
    ladenCo2EmissionsPerTransportWorkPax: float
    ladenCo2EmissionsPerTransportWorkFreight: float
    voluntaryReportingAdditionalInformation: str
    voluntaryReportingAverageDensityOfTheCargoTransported: float

def parse_technical_efficiency(technical_efficiency) -> Tuple[Optional[str], Optional[float]]:
    if (type(technical_efficiency) != str) | (technical_efficiency == "Not Applicable"):
        return None, None
    else:
        label, string_value = technical_efficiency.split(" ", 1)
        value = float(string_value[1:-11])
        return label, value

def row_to_entry(row: pd.Series) -> Entry:
    technicalEfficiencyLabel, technicalEfficiencyValue = parse_technical_efficiency(row["Technical efficiency"])
    return Entry(
        shipImo=int(row["IMO Number"]),
        shipName=row["Name"],
        shipType=row["Ship type"],
        reportingPeriod=int(row["Reporting Period"]),
        technicalEfficiencyLabel=technicalEfficiencyLabel,
        technicalEfficiencyValue=technicalEfficiencyValue,
        portOfRegistry=row["Port of Registry"],
        shipHomePort=row["Home Port"],
        iceClassPolarCode=row["Ice Class"],
        docIssueDate=datetime.strptime(row["DoC issue date"], "%d/%m/%Y"),
        docExpiryDate=datetime.strptime(row["DoC expiry date"], '%d/%m/%Y'),
        verifierNumber=row["Verifier Number"],
        verifierName=row["Verifier Name"],
        verifierNab=row["Verifier NAB"],
        verifierAddress=row["Verifier Address"],
        verifierCity=row["Verifier City"],
        verifierAccreditationNumber=row["Verifier Accreditation number"],
        verifierCountry=row["Verifier Country"],
        monitoringMethodA=row["A"]=="Yes",
        monitoringMethodB=row["B"]=="Yes",
        monitoringMethodC=row["C"]=="Yes",
        monitoringMethodD=row["D"]=="Yes",
        totalFuelConsumption=row["Total fuel consumption [m tonnes]"],
        onLadenFuelConsumption=row["Fuel consumptions assigned to On laden [m tonnes]"],
        totalCo2Emissions=row["Total CO₂ emissions [m tonnes]"],
        betweenMSJurisdictionPortsCo2Emissions=row["CO₂ emissions from all voyages between ports under a MS jurisdiction [m tonnes]"],
        fromMSJurisdictionPortsCo2Emissions=row["CO₂ emissions from all voyages which departed from ports under a MS jurisdiction [m tonnes]"],
        toMSJurisdictionPortsCo2Emissions=row["CO₂ emissions from all voyages to ports under a MS jurisdiction [m tonnes]"],
        atBerthMSJurisdictionPortsCo2Emissions=row["CO₂ emissions which occurred within ports under a MS jurisdiction at berth [m tonnes]"],
        passengerCo2Emissions=row["CO₂ emissions assigned to Passenger transport [m tonnes]"],
        freightCo2Emissions=row["CO₂ emissions assigned to Freight transport [m tonnes]"],
        onLadenCo2Emissions=row["CO₂ emissions assigned to On laden [m tonnes]"],
        annualTotalTimeSpentAtSeaHours=row["Annual Total time spent at sea [hours]"],
        fuelConsumptionPerDistance=row["Annual average Fuel consumption per distance [kg / n mile]"],
        fuelConsumptionPerTransportWorkMass=row["Annual average Fuel consumption per transport work (mass) [g / m tonnes · n miles]"],
        fuelConsumptionPerTransportWorkVolume=row["Annual average Fuel consumption per transport work (volume) [g / m³ · n miles]"],
        fuelConsumptionPerTransportWorkDwt=row["Annual average Fuel consumption per transport work (dwt) [g / dwt carried · n miles]"],
        fuelConsumptionPerTransportWorkPax=row["Annual average Fuel consumption per transport work (pax) [g / pax · n miles]"],
        fuelConsumptionPerTransportWorkFreight=row["Annual average Fuel consumption per transport work (freight) [g / m tonnes · n miles]"],
        Co2EmissionsPerDistance=row["Annual average CO₂ emissions per distance [kg CO₂ / n mile]"],
        Co2EmissionsPerTransportWorkMass=row["Annual average CO₂ emissions per transport work (mass) [g CO₂ / m tonnes · n miles]"],
        Co2EmissionsPerTransportWorkVolume=row["Annual average CO₂ emissions per transport work (volume) [g CO₂ / m³ · n miles]"],
        Co2EmissionsPerTransportWorkDwt=row["Annual average CO₂ emissions per transport work (dwt) [g CO₂ / dwt carried · n miles]"],
        Co2EmissionsPerTransportWorkPax=row["Annual average CO₂ emissions per transport work (pax) [g CO₂ / pax · n miles]"],
        Co2EmissionsPerTransportWorkFreight=row["Annual average CO₂ emissions per transport work (freight) [g CO₂ / m tonnes · n miles]"],
        distanceTravelledThroughIce=row["Through ice [n miles]"],
        totalTimeSpentAtSeaHours=row["Total time spent at sea [hours]"],
        totalTimeSpentAtSeaThroughIceHours=row["Total time spent at sea through ice [hours]"],
        ladenFuelConsumptionPerDistance=row["Fuel consumption per distance on laden voyages [kg / n mile]"],
        ladenFuelConsumptionPerTransportWorkMass=row["Fuel consumption per transport work (mass) on laden voyages [g / m tonnes · n miles]"],
        ladenFuelConsumptionPerTransportWorkVolume=row["Fuel consumption per transport work (volume) on laden voyages [g / m³ · n miles]"],
        ladenFuelConsumptionPerTransportWorkDwt=row["Fuel consumption per transport work (dwt) on laden voyages [g / dwt carried · n miles]"],
        ladenFuelConsumptionPerTransportWorkPax=row["Fuel consumption per transport work (pax) on laden voyages [g / pax · n miles]"],
        ladenFuelConsumptionPerTransportWorkFreight=row["Fuel consumption per transport work (freight) on laden voyages [g / m tonnes · n miles]"],
        ladenCo2EmissionsPerDistance=row["CO₂ emissions per distance on laden voyages [kg CO₂ / n mile]"],
        ladenCo2EmissionsPerTransportWorkMass=row["CO₂ emissions per transport work (mass) on laden voyages [g CO₂ / m tonnes · n miles]"],
        ladenCo2EmissionsPerTransportWorkVolume=row["CO₂ emissions per transport work (volume) on laden voyages [g CO₂ / m³ · n miles]"],
        ladenCo2EmissionsPerTransportWorkDwt=row["CO₂ emissions per transport work (dwt) on laden voyages [g CO₂ / dwt carried · n miles]"],
        ladenCo2EmissionsPerTransportWorkPax=row["CO₂ emissions per transport work (pax) on laden voyages [g CO₂ / pax · n miles]"],
        ladenCo2EmissionsPerTransportWorkFreight=row["CO₂ emissions per transport work (freight) on laden voyages [g CO₂ / m tonnes · n miles]"],
        voluntaryReportingAdditionalInformation=row["Additional information to facilitate the understanding of the reported average operational energy efficiency indicators"],
        voluntaryReportingAverageDensityOfTheCargoTransported=row["Average density of the cargo transported [m tonnes / m³]"]
)
