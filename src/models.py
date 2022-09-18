from datetime import datetime
from typing import Optional

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
    docIssueDate: Optional[datetime]
    docExpiryDate: Optional[datetime]
    verifierNumber: Optional[str]
    verifierName: Optional[str]
    verifierNab: Optional[str]
    verifierAddress: Optional[str]
    verifierCity: Optional[str]
    verifierAccreditationNumber: Optional[str]
    verifierCountry: Optional[str]
    monitoringMethodA: Optional[bool]
    monitoringMethodB: Optional[bool]
    monitoringMethodC: Optional[bool]
    monitoringMethodD: Optional[bool]
    totalFuelConsumption: Optional[float]
    onLadenFuelConsumption: Optional[float]
    totalCo2Emissions: Optional[float]
    betweenMSJurisdictionPortsCo2Emissions: Optional[float]
    fromMSJurisdictionPortsCo2Emissions: Optional[float]
    toMSJurisdictionPortsCo2Emissions: Optional[float]
    atBerthMSJurisdictionPortsCo2Emissions: Optional[float]
    passengerCo2Emissions: Optional[float]
    freightCo2Emissions: Optional[float]
    onLadenCo2Emissions: Optional[float]
    annualTotalTimeSpentAtSeaHours: Optional[float]
    fuelConsumptionPerDistance: Optional[float]
    fuelConsumptionPerTransportWorkMass: Optional[float]
    fuelConsumptionPerTransportWorkVolume: Optional[float]
    fuelConsumptionPerTransportWorkDwt: Optional[float]
    fuelConsumptionPerTransportWorkPax: Optional[float]
    fuelConsumptionPerTransportWorkFreight: Optional[float]
    Co2EmissionsPerDistance: Optional[float]
    Co2EmissionsPerTransportWorkMass: Optional[float]
    Co2EmissionsPerTransportWorkVolume: Optional[float]
    Co2EmissionsPerTransportWorkDwt: Optional[float]
    Co2EmissionsPerTransportWorkPax: Optional[float]
    Co2EmissionsPerTransportWorkFreight: Optional[float]
    distanceTravelledThroughIce: Optional[float]
    totalTimeSpentAtSeaHours: Optional[float]
    totalTimeSpentAtSeaThroughIceHours: Optional[float]
    ladenFuelConsumptionPerDistance: Optional[float]
    ladenFuelConsumptionPerTransportWorkMass: Optional[float]
    ladenFuelConsumptionPerTransportWorkVolume: Optional[float]
    ladenFuelConsumptionPerTransportWorkDwt: Optional[float]
    ladenFuelConsumptionPerTransportWorkPax: Optional[float]
    ladenFuelConsumptionPerTransportWorkFreight: Optional[float]
    ladenCo2EmissionsPerDistance: Optional[float]
    ladenCo2EmissionsPerTransportWorkMass: Optional[float]
    ladenCo2EmissionsPerTransportWorkVolume: Optional[float]
    ladenCo2EmissionsPerTransportWorkDwt: Optional[float]
    ladenCo2EmissionsPerTransportWorkPax: Optional[float]
    ladenCo2EmissionsPerTransportWorkFreight: Optional[float]
    voluntaryReportingAdditionalInformation: Optional[str]
    voluntaryReportingAverageDensityOfTheCargoTransported: Optional[float]
