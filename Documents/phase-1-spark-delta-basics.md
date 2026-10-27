# Phase 1 — Spark, Delta, Unity Catalog basics

**Branch:** `phase-1-spark-delta-basics`

## Goal

Get comfortable with Spark DataFrames, Delta Lake's transaction log, and Unity Catalog object model — then build the synthetic generator this whole project depends on for streaming/CDC lessons.

## What you'll learn

- Reading the real Olist CSVs out of the Volume into Spark DataFrames.
- Writing them as managed Delta tables; what `_delta_log` actually contains (JSON commit files, add/remove actions).
- `DESCRIBE HISTORY` and Delta time travel (`VERSION AS OF`).
- `.explain()` on a simple query — first look at a physical plan, before Phase 6 goes deep.
- Why `src/generator/` exists: the real Olist dataset is a static snapshot, so this script reads it and *emits* simulated daily order-arrival batches, a synthetic customer CDC feed, and clickstream events, so later phases have something to stream.

## Olist entities/tables involved

`olist_orders_dataset`, `olist_order_items_dataset`, `olist_order_payments_dataset`, `olist_order_reviews_dataset`, `olist_customers_dataset`, `olist_products_dataset` — read as the seed data for the generator.

## Steps

- [ ] Create `databricks.yml` (Asset Bundle skeleton, dev target only for now).
- [ ] Read the 9 CSVs from the Volume into Spark DataFrames; write each as a managed Delta table in a scratch schema.
- [ ] Inspect `_delta_log` for one table; run `DESCRIBE HISTORY`.
- [ ] Build `src/generator/` (pure Python, testable without Spark):
  - Split orders by `order_purchase_timestamp` into daily batch files (JSON).
  - Derive a synthetic `customers_cdc` feed from `olist_customers_dataset` (INSERT on first appearance, then synthesized UPDATE/DELETE events with an `op` + `seq` column).
  - Generate synthetic `clickstream` events (Faker) referencing real `product_id`/`customer_id`.
  - Replay `olist_products_dataset` as a daily snapshot, injecting occasional price/category changes.
- [ ] Write a couple of pytest unit tests for the generator's pure functions.

## Done criteria

- `src/generator/` can be run to produce at least 3 days of simulated orders/clickstream/CDC/product-snapshot files into the landing Volume.
- You can explain, in your own words, what a Delta `_delta_log` entry contains and what `DESCRIBE HISTORY` is reading.
- pytest passes for the generator's unit tests.

## My notes

_(fill in as you go)_
