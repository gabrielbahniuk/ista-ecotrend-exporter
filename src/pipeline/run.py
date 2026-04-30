from __future__ import annotations

import os

from dotenv import load_dotenv

from src.pipeline.extract import extract_from_ista
from src.pipeline.load_postgres import write_records
from src.pipeline.normalize import normalize


def main() -> None:
    load_dotenv()
    source = os.getenv("PIPELINE_SOURCE", "ista")

    payload = extract_from_ista()
    records = normalize(payload, source=source)
    inserted = write_records(records)

    print(
        "Pipeline completed:",
        {
            "units": len(payload.get("uuids", [])),
            "records_generated": len(records),
            "records_inserted": inserted,
        },
    )


if __name__ == "__main__":
    main()
