from __future__ import annotations

import os
from pathlib import Path

import psycopg


def main() -> None:
    database_url = os.environ["DATABASE_URL"]
    schema_path = Path(__file__).resolve().parent / "schema.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(schema_sql)
        conn.commit()

    print("Schema initialized successfully.")


if __name__ == "__main__":
    main()
