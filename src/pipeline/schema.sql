CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS consumption_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source TEXT NOT NULL,
    unit_uuid TEXT NOT NULL,
    meter_name TEXT NULL,
    metric TEXT NOT NULL,
    period_start TIMESTAMPTZ NULL,
    period_end TIMESTAMPTZ NULL,
    value NUMERIC NOT NULL,
    unit TEXT NOT NULL,
    raw_payload JSONB NOT NULL,
    collected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fingerprint TEXT NOT NULL UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_consumption_records_unit_uuid ON consumption_records (unit_uuid);
CREATE INDEX IF NOT EXISTS idx_consumption_records_metric ON consumption_records (metric);
CREATE INDEX IF NOT EXISTS idx_consumption_records_period_end ON consumption_records (period_end);
