# ai-datacenter-power-tracker

A small tracker + dashboard for how AI is reshaping US and global
electricity demand — pulling from public EIA/DOE/IEA/BloombergNEF
reporting on data center power growth, grid capacity, and where that
demand is headed through 2050.

## Why

Everyone talks about AI compute. The actual constraint the industry is
running into is **power** — utilities, grid interconnection queues, and
generation capacity. This tracker keeps a running, sourced view of the
public numbers behind that story: how fast US electricity demand is
growing, what share of it data centers account for, and how that
compares globally.

## What it produces

Running the dashboard builds:
- `output/power_demand_charts.png` — a grid of trend charts
- `output/dashboard.html` — a single-page report with the charts plus a
  full data table, every row linked to its original source

## Install & run

```bash
git clone https://github.com/<your-username>/ai-datacenter-power-tracker.git
cd ai-datacenter-power-tracker
pip install -r requirements.txt
python3 -m tracker.dashboard --out-dir output
open output/dashboard.html   # or just open the file in a browser
```

Works out of the box with **real, citation-backed figures** bundled in
`tracker/seed_data.py` — no API key required.

## Live data (optional)

`tracker/fetch_eia.py` pulls live series from the EIA Open Data API v2.
To use it:

1. Get a free key: https://www.eia.gov/opendata/register.php
2. `export EIA_API_KEY=your_key_here`
3. `python3 -m tracker.fetch_eia`

The seed dataset stays as the default/fallback since not every metric in
this tracker (e.g. IEA global figures, BloombergNEF forecasts) has a live
API route — those get refreshed manually as new outlooks are published.

## Data sources

| Metric | Source |
|---|---|
| US total electricity demand | EIA Short-Term Energy Outlook |
| Data centers' share of US electricity | US Department of Energy |
| Global data center electricity consumption | International Energy Agency |
| US data center peak power demand | BloombergNEF |
| US data center server electricity (high-demand case) | EIA Annual Energy Outlook 2026 |

Full citations with links are in `tracker/seed_data.py` and rendered in
the generated dashboard table.

## Project structure

```
tracker/
  seed_data.py    # bundled, cited figures (default data source)
  fetch_eia.py     # optional live EIA API v2 pull
  dashboard.py     # builds the charts + HTML report
```

## About

Built by Nikki Solai — Supplier Industrialization Engineer intern at
Tesla, MEM candidate at Purdue, positioning toward AI infrastructure.
Paired with [grid-to-chip-calculator](https://github.com/<your-username>/grid-to-chip-calculator),
which models the same power story from the engineering side — this one
tracks the macro trend, that one sizes the hardware.
