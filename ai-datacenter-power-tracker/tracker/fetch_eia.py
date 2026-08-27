"""Optional live data pull from the EIA Open Data API (v2).

Requires a free API key: register at https://www.eia.gov/opendata/register.php
and set it as the EIA_API_KEY environment variable. Without a key, the rest
of this project falls back to tracker/seed_data.py (real, citation-backed
figures, just not live-refreshed).

The EIA API is organized as a route hierarchy, e.g.:
    https://api.eia.gov/v2/electricity/retail-sales/data/
    https://api.eia.gov/v2/steo/data/                (Short-Term Energy Outlook)
Every request needs api_key, and most need facets/frequency params -- see
https://www.eia.gov/opendata/documentation.php for the full route catalog.
"""

import os
import urllib.request
import urllib.parse
import json

EIA_BASE_URL = "https://api.eia.gov/v2"


class EIAKeyMissing(RuntimeError):
    pass


def get_api_key() -> str:
    key = os.environ.get("EIA_API_KEY")
    if not key:
        raise EIAKeyMissing(
            "No EIA_API_KEY set. Get a free key at "
            "https://www.eia.gov/opendata/register.php and `export EIA_API_KEY=...`"
        )
    return key


def fetch_route(route: str, params: dict) -> dict:
    """GET a route under the EIA v2 API, e.g. route='electricity/retail-sales/data'.

    params should NOT include api_key -- it's added automatically.
    """
    api_key = get_api_key()
    query = dict(params)
    query["api_key"] = api_key
    url = f"{EIA_BASE_URL}/{route}?{urllib.parse.urlencode(query, doseq=True)}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_us_electricity_retail_sales(frequency: str = "annual", length: int = 5) -> list:
    """Example live pull: US total electricity retail sales by year.

    Returns a list of {period, value} dicts, most recent `length` periods.
    """
    data = fetch_route(
        "electricity/retail-sales/data",
        {
            "frequency": frequency,
            "data[0]": "sales",
            "facets[sectorid][]": "ALL",
            "facets[stateid][]": "US",
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
            "offset": 0,
            "length": length,
        },
    )
    rows = data.get("response", {}).get("data", [])
    return [{"period": r.get("period"), "value": r.get("sales")} for r in rows]


if __name__ == "__main__":
    try:
        rows = fetch_us_electricity_retail_sales()
        for r in rows:
            print(r)
    except EIAKeyMissing as e:
        print(e)
