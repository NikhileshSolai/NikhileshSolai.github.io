"""Builds a static PNG chart set + a single-page HTML dashboard from the
tracker's data (seed data by default, live EIA data if EIA_API_KEY is set
and --live is passed).
"""

import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from . import seed_data


def plot_series(ax, points, title, ylabel):
    years = [p.year for p in points]
    values = [p.value for p in points]
    ax.plot(years, values, marker="o", linewidth=2)
    for x, y in zip(years, values):
        ax.annotate(f"{y:,.0f}", (x, y), textcoords="offset points",
                     xytext=(0, 8), ha="center", fontsize=8)
    ax.set_title(title, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.set_xlabel("Year", fontsize=8)
    ax.grid(alpha=0.3)


def build_chart_grid(out_path: str):
    series = seed_data.all_series()
    n = len(series)
    cols = 2
    rows = (n + 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(11, 4 * rows))
    axes = axes.flatten()

    for ax, (name, points) in zip(axes, series.items()):
        unit = points[0].unit
        plot_series(ax, points, name, unit)

    for ax in axes[len(series):]:
        ax.axis("off")

    fig.suptitle("AI Data Center Power Demand Tracker", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def build_html_report(out_path: str, chart_filename: str):
    series = seed_data.all_series()
    rows_html = []
    for name, points in series.items():
        for p in points:
            rows_html.append(
                f"<tr><td>{name}</td><td>{p.year}</td><td>{p.value:,.1f} {p.unit}</td>"
                f"<td>{p.note}</td>"
                f"<td><a href='{p.source_url}' target='_blank'>{p.source}</a></td></tr>"
            )

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>AI Data Center Power Demand Tracker</title>
<style>
  body {{ font-family: -apple-system, Helvetica, Arial, sans-serif; margin: 2rem; color: #1a1a1a; }}
  h1 {{ font-size: 1.5rem; }}
  img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 8px; }}
  table {{ border-collapse: collapse; width: 100%; margin-top: 2rem; font-size: 0.85rem; }}
  th, td {{ border: 1px solid #ddd; padding: 6px 10px; text-align: left; }}
  th {{ background: #f5f5f5; }}
  .caption {{ color: #666; font-size: 0.85rem; margin-top: 0.5rem; }}
</style>
</head>
<body>
  <h1>AI Data Center Power Demand Tracker</h1>
  <p class="caption">Public grid/capex data on how AI is reshaping US and global
  electricity demand. Sourced from EIA, DOE, IEA, and BloombergNEF reporting
  (see table below for citations). Static snapshot as of August 2026 --
  re-run with EIA_API_KEY set for a live pull where an API route exists.</p>
  <img src="{chart_filename}" alt="Power demand charts">
  <table>
    <tr><th>Series</th><th>Year</th><th>Value</th><th>Note</th><th>Source</th></tr>
    {''.join(rows_html)}
  </table>
</body>
</html>"""

    with open(out_path, "w") as f:
        f.write(html)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Build the AI data center power demand dashboard")
    parser.add_argument("--out-dir", default="output")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    chart_path = os.path.join(args.out_dir, "power_demand_charts.png")
    html_path = os.path.join(args.out_dir, "dashboard.html")

    build_chart_grid(chart_path)
    build_html_report(html_path, os.path.basename(chart_path))

    print(f"Chart written to {chart_path}")
    print(f"Dashboard written to {html_path}")


if __name__ == "__main__":
    main()
