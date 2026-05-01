from __future__ import annotations

import os
from collections.abc import Iterable
from typing import Any

from pyecotrend_ista import PyEcotrendIsta


def _safe_keys(value: object) -> list[str]:
    if isinstance(value, dict):
        return sorted(str(k) for k in value.keys())[:20]
    return []


def _preview(value: object, max_items: int = 3) -> object:
    if isinstance(value, dict):
        preview: dict[str, str] = {}
        for idx, (k, v) in enumerate(value.items()):
            if idx >= max_items:
                break
            preview[str(k)] = type(v).__name__
        return preview
    if isinstance(value, list):
        return [type(v).__name__ for v in value[:max_items]]
    return value


def _first(items: Iterable[str]) -> str | None:
    for item in items:
        return item
    return None


def extract_from_ista() -> dict[str, Any]:
    email = os.environ["ISTA_EMAIL"]
    password = os.environ["ISTA_PASSWORD"]

    client = PyEcotrendIsta(email, password)
    payload: dict[str, Any] = {}

    try:
        client.login()
        uuids = client.get_uuids() or []
        payload["uuids"] = uuids
        payload["items"] = {}

        for unit_uuid in uuids:
            consumption = client.get_consumption_data(unit_uuid)
            details = client.get_consumption_unit_details()
            payload["items"][unit_uuid] = {
                "consumption": consumption,
                "details": details,
            }
    finally:
        client.logout()

    debug_enabled = os.getenv("PIPELINE_DEBUG", "false").lower() in {"1", "true", "yes"}
    if debug_enabled:
        first_unit_uuid = _first(payload["items"].keys())
        first_item = payload["items"].get(first_unit_uuid) if first_unit_uuid else None
        first_consumption = first_item.get("consumption") if isinstance(first_item, dict) else None
        first_details = first_item.get("details") if isinstance(first_item, dict) else None

        print(
            "Extract diagnostics:",
            {
                "units_found": len(payload.get("uuids", [])),
                "first_unit_uuid": first_unit_uuid,
                "consumption_type": type(first_consumption).__name__,
                "consumption_keys": _safe_keys(first_consumption),
                "consumption_preview": _preview(first_consumption),
                "details_type": type(first_details).__name__,
                "details_keys": _safe_keys(first_details),
                "details_preview": _preview(first_details),
            },
        )

    return payload
