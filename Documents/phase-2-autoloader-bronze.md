# Phase 2 — Auto Loader → Bronze

**Branch:** `phase-2-autoloader-bronze`

## Goal

Ingest the generator's output files into Bronze Delta tables incrementally, using Auto Loader, instead of re-reading everything on every run.

## What you'll learn

- `cloudFiles` format, `schemaLocation`, and why Auto Loader tracks schema separately from the table.
- Schema evolution: what happens when `clickstream` gains a `coupon_code` column mid-project.
- `_rescued_data`: how malformed/unexpected columns get captured instead of silently dropped.
- Checkpoints: what's actually stored there, and why deleting one is dangerous (see Safety Rules in `CLAUDE.md`).
- `trigger(availableNow=True)` vs an always-on stream, and why Free Edition requires the former.
- Doing this first in a plain notebook, then as a Lakeflow Declarative Pipeline (`resources/pipeline.yml`).

## Olist entities/tables involved

Generator output from Phase 1: `orders` (daily batches), `clickstream` (schema grows mid-phase).

## Steps

- [ ] Write a notebook-based Auto Loader stream for `orders` → `brz_orders`, with its own checkpoint + schema location under `/Volumes/brazil_ecommerce_dev/ops/checkpoints/`.
- [ ] Run it over 2-3 days of generator output; confirm only new files are processed on the second run.
- [ ] Add `clickstream` → `brz_clickstream`; mid-way, add `coupon_code` to the generator's clickstream schema and confirm Auto Loader picks up the new column.
- [ ] Deliberately write a malformed clickstream row; confirm it lands in `_rescued_data` rather than failing the stream.
- [ ] Re-implement both streams as a Lakeflow Declarative Pipeline in `src/pipeline/bronze/` + `resources/pipeline.yml`.

## Done criteria

- `brz_orders` and `brz_clickstream` exist and only process new files on repeat runs (verified via `DESCRIBE HISTORY` showing incremental commits, not full rewrites).
- You can point to a row in `_rescued_data` and explain why it's there.
- The same ingestion works both as a standalone notebook and as a Lakeflow pipeline — and you can explain the difference between the two approaches.

## My notes

_(fill in as you go)_
