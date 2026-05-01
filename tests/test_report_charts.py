from pathlib import Path

from src.pipeline.report_charts import generate_chart_assets
from src.pipeline.report_data import enrich_records


def test_generate_chart_assets_writes_svg(tmp_path: Path):
    enriched = enrich_records(
        [
            {"period_end": "2026-02-28T23:59:59+00:00", "metric": "heating", "value": 20.0, "unit": "units"},
            {"period_end": "2026-03-31T23:59:59+00:00", "metric": "heating", "value": 30.0, "unit": "units"},
            {"period_end": "2026-03-31T23:59:59+00:00", "metric": "heating_cost", "value": 95.0, "unit": "EUR"},
        ]
    )

    charts_dir = tmp_path / "charts"
    paths = generate_chart_assets(enriched, charts_dir)

    key_heating = (2026, "heating")
    assert key_heating in paths
    svg_path = charts_dir / "heating_2026.svg"
    assert svg_path.is_file()
    assert paths[key_heating].endswith("heating_2026.svg")

    svg_text = svg_path.read_text(encoding="utf-8")
    assert "€" in svg_text
    assert "Feb" in svg_text and "Mar" in svg_text
