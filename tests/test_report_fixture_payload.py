from pathlib import Path

import json

from src.pipeline.normalize import normalize
from src.pipeline.report import load_fixture_payload


def test_load_fixture_wraps_flat_uuid_map(tmp_path: Path):
    raw = {"unit-a": {"consumption": {"consumptions": [], "costs": []}}}
    fp = tmp_path / "fixture.json"
    fp.write_text(json.dumps(raw), encoding="utf-8")

    wrapped = load_fixture_payload(fp)

    assert wrapped["uuids"] == ["unit-a"]
    assert wrapped["items"]["unit-a"]["consumption"]["consumptions"] == []


def test_normalize_accepts_fixture_shape(tmp_path: Path):
    raw = {
        "unit-x": {
            "consumption": {
                "consumptions": [
                    {
                        "date": {"month": 4, "year": 2026},
                        "readings": [
                            {
                                "type": "heating",
                                "value": "100",
                                "unit": "Einheiten",
                            }
                        ],
                    }
                ],
                "costs": [
                    {
                        "date": {"month": 4, "year": 2026},
                        "costsByEnergyType": [
                            {"type": "heating", "value": 50, "unit": "EUR"},
                        ],
                    }
                ],
            }
        }
    }
    fp = tmp_path / "fixture.json"
    fp.write_text(json.dumps(raw), encoding="utf-8")

    payload = load_fixture_payload(fp)
    records = normalize(payload)

    heating = next(r for r in records if r["metric"] == "heating")
    cost = next(r for r in records if r["metric"] == "heating_cost")
    assert heating["value"] == 100.0
    assert cost["value"] == 50.0
    assert cost["unit"] == "EUR"
