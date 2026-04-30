# ista-pipeline

Private, low-cost pipeline to extract data from ISTA, normalize it, and load it into Postgres for Grafana dashboards.

## Architecture

- **Extract**: `pyecotrend-ista` client
- **Transform**: normalize records into a canonical table shape
- **Load**: upsert into Postgres with idempotency
- **Schedule**: GitHub Actions cron or local execution

## Quick start

### 1) Create virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
```

### 2) Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3) Configure environment

```bash
cp .env.example .env
# Fill values in .env
set -a; source .env; set +a
```

### 4) Run schema migration

```bash
python -m src.pipeline.init_db
```

### 5) Run pipeline

```bash
python -m src.pipeline.run
```

## Environment variables

- `ISTA_EMAIL`: ISTA account email
- `ISTA_PASSWORD`: ISTA account password
- `DATABASE_URL`: PostgreSQL DSN, including `sslmode=require` for hosted DBs

Optional:

- `PIPELINE_SOURCE`: defaults to `ista`
- `PIPELINE_TIMEZONE`: defaults to `UTC`

## Data model

The pipeline writes to table `consumption_records` with:

- identifiers (`unit_uuid`, `meter_name`, `metric`)
- time fields (`period_start`, `period_end`, `collected_at`)
- values (`value`, `unit`)
- idempotency key (`fingerprint`, unique)
- `raw_payload` for traceability/debugging

## GitHub Actions

Workflow file: `.github/workflows/daily.yml`

- Manual run: `workflow_dispatch`
- Scheduled run: once daily (UTC)

Required repository secrets:

- `ISTA_EMAIL`
- `ISTA_PASSWORD`
- `DATABASE_URL`

## Security notes

- Never commit `.env` or credentials.
- Rotate credentials if exposed.
- Keep DB user scoped to least privilege needed.