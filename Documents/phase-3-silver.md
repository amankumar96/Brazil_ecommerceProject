# Phase 3 — Silver

**Branch:** `phase-3-silver`

## Goal

Turn raw Bronze data into clean, trustworthy tables: correctly typed, deduplicated, and quality-checked.

## What you'll learn

- Casting and standardising columns (timestamps, currency fields, enums like order status).
- Deduplication by business key + a sequence/version column (important for out-of-order CDC data later).
- Lakeflow pipeline **expectations**: warn vs drop vs fail, and when production teams pick each.

## Olist entities/tables involved

All Bronze tables from Phase 2 (`brz_orders`, `brz_clickstream`), plus Bronze versions of `customers_cdc` and `products` once Phase 4 lands (Silver work on those can be revisited then, or stubbed here first).

## Steps

- [ ] Define `slv_orders`: cast types, standardise order status values, dedup by `order_id` + latest `order_purchase_timestamp`.
- [ ] Add expectations: e.g. `order_id` must not be null (fail), `price >= 0` (drop), `freight_value` present (warn).
- [ ] Define `slv_clickstream`: handle the `_rescued_data` column, standardise event types.
- [ ] Write a small pytest covering one pure dedup/cast function from `src/brazil_ecommerce/`.

## Done criteria

- `slv_orders` has zero duplicate `order_id`s and no null required fields.
- At least one expectation of each kind (warn/drop/fail) is demonstrated, and you can explain the production trade-off between them.
- pytest passes.

## My notes

_(fill in as you go)_
