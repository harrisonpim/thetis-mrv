from datetime import datetime
from typing import Optional, Tuple

import pandas as pd
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


def parse_technical_efficiency(
    technical_efficiency,
) -> Tuple[Optional[str], Optional[float]]:
    if type(technical_efficiency) != str:
        return None, None
    elif technical_efficiency.startswith("Not Applicable"):
        return None, None
    elif technical_efficiency == "":
        return None, None
    elif technical_efficiency.startswith("0"):
        return None, None
    else:
        try:
            label, string_value = technical_efficiency.split(" ", 1)
            value = float(
                string_value.replace("(", "")
                .replace("gCO₂/t·nm", "")
                .replace(")", "")
            )
            return label, value
        except ValueError as _:
            return None, None


def row_to_entry(row: pd.Series) -> Entry:
    (
        technicalEfficiencyLabel,
        technicalEfficiencyValue,
    ) = parse_technical_efficiency(row["Technical efficiency"])
    try:
        docIssueDate = (datetime.strptime(row["DoC issue date"], "%d/%m/%Y"),)
    except ValueError as _:
        docIssueDate = None
    try:
        docExpiryDate = (datetime.strptime(row["DoC expiry date"], "%d/%m/%Y"),)
    except ValueError as _:
        docExpiryDate = None
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
        docIssueDate=docIssueDate,
        docExpiryDate=docExpiryDate,
        verifierNumber=row["Verifier Number"],
        verifierName=row["Verifier Name"],
        verifierNab=row["Verifier NAB"],
        verifierAddress=row["Verifier Address"],
        verifierCity=row["Verifier City"],
        verifierAccreditationNumber=row["Verifier Accreditation number"],
        verifierCountry=row["Verifier Country"],
        monitoringMethodA=row["A"] == "Yes",
        monitoringMethodB=row["B"] == "Yes",
        monitoringMethodC=row["C"] == "Yes",
        monitoringMethodD=row["D"] == "Yes",
        totalFuelConsumption=row["Total fuel consumption [m tonnes]"],
        onLadenFuelConsumption=row[
            "Fuel consumptions assigned to On laden [m tonnes]"
        ],
        totalCo2Emissions=row["Total CO₂ emissions [m tonnes]"],
        betweenMSJurisdictionPortsCo2Emissions=row[
            "CO₂ emissions from all voyages between ports under a MS jurisdiction [m tonnes]"
        ],
        fromMSJurisdictionPortsCo2Emissions=row[
            "CO₂ emissions from all voyages which departed from ports under a MS jurisdiction [m tonnes]"
        ],
        toMSJurisdictionPortsCo2Emissions=row[
            "CO₂ emissions from all voyages to ports under a MS jurisdiction [m tonnes]"
        ],
        atBerthMSJurisdictionPortsCo2Emissions=row[
            "CO₂ emissions which occurred within ports under a MS jurisdiction at berth [m tonnes]"
        ],
        passengerCo2Emissions=row[
            "CO₂ emissions assigned to Passenger transport [m tonnes]"
        ],
        freightCo2Emissions=row[
            "CO₂ emissions assigned to Freight transport [m tonnes]"
        ],
        onLadenCo2Emissions=row[
            "CO₂ emissions assigned to On laden [m tonnes]"
        ],
        annualTotalTimeSpentAtSeaHours=row[
            "Annual Total time spent at sea [hours]"
        ],
        fuelConsumptionPerDistance=row[
            "Annual average Fuel consumption per distance [kg / n mile]"
        ],
        fuelConsumptionPerTransportWorkMass=row[
            "Annual average Fuel consumption per transport work (mass) [g / m tonnes · n miles]"
        ],
        fuelConsumptionPerTransportWorkVolume=row[
            "Annual average Fuel consumption per transport work (volume) [g / m³ · n miles]"
        ],
        fuelConsumptionPerTransportWorkDwt=row[
            "Annual average Fuel consumption per transport work (dwt) [g / dwt carried · n miles]"
        ],
        fuelConsumptionPerTransportWorkPax=row[
            "Annual average Fuel consumption per transport work (pax) [g / pax · n miles]"
        ],
        fuelConsumptionPerTransportWorkFreight=row[
            "Annual average Fuel consumption per transport work (freight) [g / m tonnes · n miles]"
        ],
        Co2EmissionsPerDistance=row[
            "Annual average CO₂ emissions per distance [kg CO₂ / n mile]"
        ],
        Co2EmissionsPerTransportWorkMass=row[
            "Annual average CO₂ emissions per transport work (mass) [g CO₂ / m tonnes · n miles]"
        ],
        Co2EmissionsPerTransportWorkVolume=row[
            "Annual average CO₂ emissions per transport work (volume) [g CO₂ / m³ · n miles]"
        ],
        Co2EmissionsPerTransportWorkDwt=row[
            "Annual average CO₂ emissions per transport work (dwt) [g CO₂ / dwt carried · n miles]"
        ],
        Co2EmissionsPerTransportWorkPax=row[
            "Annual average CO₂ emissions per transport work (pax) [g CO₂ / pax · n miles]"
        ],
        Co2EmissionsPerTransportWorkFreight=row[
            "Annual average CO₂ emissions per transport work (freight) [g CO₂ / m tonnes · n miles]"
        ],
        distanceTravelledThroughIce=row["Through ice [n miles]"],
        totalTimeSpentAtSeaHours=row["Total time spent at sea [hours]"],
        totalTimeSpentAtSeaThroughIceHours=row[
            "Total time spent at sea through ice [hours]"
        ],
        ladenFuelConsumptionPerDistance=row[
            "Fuel consumption per distance on laden voyages [kg / n mile]"
        ],
        ladenFuelConsumptionPerTransportWorkMass=row[
            "Fuel consumption per transport work (mass) on laden voyages [g / m tonnes · n miles]"
        ],
        ladenFuelConsumptionPerTransportWorkVolume=row[
            "Fuel consumption per transport work (volume) on laden voyages [g / m³ · n miles]"
        ],
        ladenFuelConsumptionPerTransportWorkDwt=row[
            "Fuel consumption per transport work (dwt) on laden voyages [g / dwt carried · n miles]"
        ],
        ladenFuelConsumptionPerTransportWorkPax=row[
            "Fuel consumption per transport work (pax) on laden voyages [g / pax · n miles]"
        ],
        ladenFuelConsumptionPerTransportWorkFreight=row[
            "Fuel consumption per transport work (freight) on laden voyages [g / m tonnes · n miles]"
        ],
        ladenCo2EmissionsPerDistance=row[
            "CO₂ emissions per distance on laden voyages [kg CO₂ / n mile]"
        ],
        ladenCo2EmissionsPerTransportWorkMass=row[
            "CO₂ emissions per transport work (mass) on laden voyages [g CO₂ / m tonnes · n miles]"
        ],
        ladenCo2EmissionsPerTransportWorkVolume=row[
            "CO₂ emissions per transport work (volume) on laden voyages [g CO₂ / m³ · n miles]"
        ],
        ladenCo2EmissionsPerTransportWorkDwt=row[
            "CO₂ emissions per transport work (dwt) on laden voyages [g CO₂ / dwt carried · n miles]"
        ],
        ladenCo2EmissionsPerTransportWorkPax=row[
            "CO₂ emissions per transport work (pax) on laden voyages [g CO₂ / pax · n miles]"
        ],
        ladenCo2EmissionsPerTransportWorkFreight=row[
            "CO₂ emissions per transport work (freight) on laden voyages [g CO₂ / m tonnes · n miles]"
        ],
        voluntaryReportingAdditionalInformation=row[
            "Additional information to facilitate the understanding of the reported average operational energy efficiency indicators"
        ],
        voluntaryReportingAverageDensityOfTheCargoTransported=row[
            "Average density of the cargo transported [m tonnes / m³]"
        ],
    )
