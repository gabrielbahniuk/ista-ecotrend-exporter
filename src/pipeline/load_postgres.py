from __future__ import annotations

import json
import os
from typing import Any

import psycopg


INSERT_SQL = """
INSERT INTO consumption_records (
    source,
    unit_uuid,
    meter_name,
    metric,
    period_start,
    period_end,
    value,
    unit,
    raw_payload,
    collected_at,
    fingerprint
)
VALUES (
    %(source)s,
    %(unit_uuid)s,
    %(meter_name)s,
    %(metric)s,
    %(period_start)s,
    %(period_end)s,
    %(value)s,
    %(unit)s,
    %(raw_payload)s::jsonb,
    %(collected_at)s,
    %(fingerprint)s
)
ON CONFLICT (fingerprint) DO NOTHING
"""


def write_records(records: list[dict[str, Any]]) -> int:
    if not records:
        return 0

    database_url = os.environ["DATABASE_URL"]
    inserted = 0

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            for record in records:
                params = dict(record)
                params["raw_payload"] = json.dumps(record["raw_payload"], ensure_ascii=True)
                cur.execute(INSERT_SQL, params)
                inserted += cur.rowcount
        conn.commit()

    return inserted
