"""Bundled, citation-backed data points on AI/data center power demand.

This is the tracker's offline fallback: real published figures (not
simulated), used automatically when no EIA_API_KEY is set so the dashboard
still renders something real out of the box. Each record cites the
publishing source so nothing here is presented without attribution.

Pulled from public reporting current as of August 2026. Numbers will move
as new EIA/IEA/BloombergNEF outlooks are published -- re-run with a live
EIA_API_KEY (see README) for current figures where an API path exists.
"""

from dataclasses import dataclass


@dataclass
class DataPoint:
    year: int
    metric: str
    value: float
    unit: str
    source: str
    source_url: str
    note: str = ""


US_ELECTRICITY_DEMAND_TWH = [
    DataPoint(2024, "US total electricity demand", 4097, "billion kWh",
              "EIA Short-Term Energy Outlook",
              "https://www.eia.gov/pressroom/releases/press582.php",
              "Record level, actual."),
    DataPoint(2025, "US total electricity demand", 4193, "billion kWh",
              "EIA Short-Term Energy Outlook",
              "https://www.eia.gov/pressroom/releases/press582.php",
              "Forecast."),
    DataPoint(2026, "US total electricity demand", 4283, "billion kWh",
              "EIA Short-Term Energy Outlook",
              "https://www.eia.gov/pressroom/releases/press582.php",
              "Forecast; strongest 4-year growth in US electricity demand since 2000."),
]

DATA_CENTER_SHARE_OF_US_POWER = [
    DataPoint(2023, "Data centers' share of US electricity", 4.4, "%",
              "US Department of Energy",
              "https://www.datacenterdynamics.com/en/news/eia-projects-record-us-data-center-power-use-amid-ai-and-crypto-boom/",
              "Actual."),
    DataPoint(2028, "Data centers' share of US electricity", 12.0, "%",
              "US Department of Energy",
              "https://www.datacenterdynamics.com/en/news/eia-projects-record-us-data-center-power-use-amid-ai-and-crypto-boom/",
              "Projection."),
]

GLOBAL_DATA_CENTER_CONSUMPTION_TWH = [
    DataPoint(2024, "Global data center electricity consumption", 415, "TWh",
              "International Energy Agency",
              "https://www.datacenterdynamics.com/en/news/eia-projects-record-us-data-center-power-use-amid-ai-and-crypto-boom/",
              "Actual."),
    DataPoint(2030, "Global data center electricity consumption", 945, "TWh",
              "International Energy Agency",
              "https://www.datacenterdynamics.com/en/news/eia-projects-record-us-data-center-power-use-amid-ai-and-crypto-boom/",
              "Forecast, published April 2026."),
]

US_DATA_CENTER_PEAK_DEMAND_GW = [
    DataPoint(2035, "US data center power demand", 106, "GW",
              "BloombergNEF",
              "https://www.utilitydive.com/news/energy-short-term-outlook-2026-load-demand-data-centers/807530/",
              "Forecast, published Dec 2025."),
]

EIA_SERVER_ELECTRICITY_HIGH_CASE_BKWH = [
    DataPoint(2020, "US commercial data center server electricity use", 50.0, "billion kWh",
              "EIA Annual Energy Outlook 2026",
              "https://www.power-eng.com/business/policy-and-regulation/eias-2026-outlook-projects-massive-capacity-buildout-as-data-centers-reshape-electricity-demand/",
              "Approximate baseline implied by AEO2026's '16x 2020 level by 2050' framing."),
    DataPoint(2050, "US commercial data center server electricity use", 818.0, "billion kWh",
              "EIA Annual Energy Outlook 2026",
              "https://www.power-eng.com/business/policy-and-regulation/eias-2026-outlook-projects-massive-capacity-buildout-as-data-centers-reshape-electricity-demand/",
              "High Electricity Demand case; >16x the 2020 level."),
]


def all_series():
    return {
        "US total electricity demand (billion kWh)": US_ELECTRICITY_DEMAND_TWH,
        "Data centers' share of US electricity (%)": DATA_CENTER_SHARE_OF_US_POWER,
        "Global data center electricity consumption (TWh)": GLOBAL_DATA_CENTER_CONSUMPTION_TWH,
        "US data center peak power demand (GW)": US_DATA_CENTER_PEAK_DEMAND_GW,
        "US data center server electricity, high-demand case (billion kWh)": EIA_SERVER_ELECTRICITY_HIGH_CASE_BKWH,
    }
