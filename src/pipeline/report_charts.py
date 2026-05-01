from __future__ import annotations

import re
from calendar import month_abbr
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.pipeline.report_data import CHART_METRIC_PAIRS, compute_chart_series
from src.pipeline.schemas import EnrichedRecord

REL_CHART_ROOT = "assets/charts"


def _safe_filename(metric: str, year: int) -> str:
    cleaned = re.sub(r"[^\w\-]+", "_", metric.strip(), flags=re.ASCII)
    return f"{cleaned}_{year}.svg"


def _ylabel(metric_key: str) -> str:
    if metric_key == "hot_water":
        return "m³"
    if metric_key == "heating":
        return "Units"
    return "Consumption"


def _fmt_num(v: float) -> str:
    if abs(v - round(v)) < 1e-6:
        return str(int(round(v)))
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _month_tick_labels(months: list[int]) -> list[str]:
    return [month_abbr[m] for m in months]


def write_combo_chart_svg(
    consumption_key: str,
    cost_key: str,
    chart_title: str,
    year: int,
    series: dict[tuple[int, str], tuple[list[int], list[float]]],
    charts_dir: Path,
) -> Path | None:
    """Consumption per month (bar height); bar labels show cost only when available, formatted with €."""
    cons = series.get((year, consumption_key))
    cost = series.get((year, cost_key))

    cons_map: dict[int, float] = {}
    if cons:
        sm, sv = cons
        cons_map = dict(zip(sm, sv, strict=True))

    cost_map: dict[int, float] = {}
    if cost:
        cm, cv = cost
        cost_map = dict(zip(cm, cv, strict=True))

    months = sorted(cons_map.keys())
    if not months:
        return None

    vals = [cons_map[m] for m in months]
    bar_labels: list[str] = []
    for m in months:
        if m in cost_map:
            bar_labels.append(f"{_fmt_num(cost_map[m])} €")
        else:
            bar_labels.append("")

    charts_dir.mkdir(parents=True, exist_ok=True)
    out_file = charts_dir / _safe_filename(consumption_key, year)

    x_ticks = _month_tick_labels(months)
    plt.figure(figsize=(9.5, 4.2))
    bars = plt.bar(x_ticks, vals, color="#3372d6")
    plt.xlabel("Month")
    plt.ylabel(_ylabel(consumption_key))
    plt.title(f"{chart_title} — {year}")
    plt.grid(axis="y", alpha=0.25)

    fontsize = max(7, min(10, int(115 / max(len(months), 1))))
    plt.bar_label(bars, labels=bar_labels, fontsize=fontsize, padding=2, rotation=0)

    plt.tight_layout()
    plt.savefig(out_file, format="svg")
    plt.close()

    return out_file


def generate_chart_assets(
    enriched: list[EnrichedRecord],
    charts_dir: Path,
) -> dict[tuple[int, str], str]:
    """One combined chart per (year, consumption metric); labels on bars show cost in € only."""
    paths: dict[tuple[int, str], str] = {}
    series = compute_chart_series(enriched)

    years_needed = sorted({int(r["year"]) for r in enriched}, reverse=True)

    for year in years_needed:
        for consumption_key, cost_key, chart_title in CHART_METRIC_PAIRS:
            out_file = write_combo_chart_svg(
                consumption_key, cost_key, chart_title, year, series, charts_dir
            )
            if out_file is None:
                continue
            rel_path = f"{REL_CHART_ROOT}/{out_file.name}"
            paths[(year, consumption_key)] = rel_path

    return paths
