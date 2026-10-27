# Phase 4 — CDC and SCD

**Branch:** `phase-4-cdc-scd`

## Goal

Learn change-data-capture and slowly-changing-dimension patterns by building SCD2 by hand first, then comparing it to Databricks' managed `AUTO CDC` feature.

## What you'll learn

- SCD2 by hand: `MERGE INTO` with `valid_from`/`valid_to`/`is_current` columns.
- The managed equivalent: `AUTO CDC ... STORED AS SCD TYPE 2` (`__START_AT`/`__END_AT`) — same result, far less code; understand what it's doing under the hood.
- SCD1 (overwrite, no history) via `AUTO CDC FROM SNAPSHOT`, applied to the daily product snapshot.
- Handling out-of-order events using the `seq` column from the synthetic CDC feed.

## Olist entities/tables involved

`customers_cdc` (synthetic change feed from Phase 1, derived from `olist_customers_dataset`), `products` (daily snapshot from Phase 1, derived from `olist_products_dataset`).

## Steps

- [ ] Hand-write SCD2 for `dim_customer` using `MERGE INTO` against the `customers_cdc` Bronze/Silver table, including `valid_from`/`valid_to`/`is_current`.
- [ ] Deliberately replay a CDC batch out of order; confirm your hand-written MERGE handles (or mishandles) it, and fix using `seq`.
- [ ] Re-implement the same `dim_customer` using `AUTO CDC ... STORED AS SCD TYPE 2`; compare row-for-row with the hand-written version.
- [ ] Implement `dim_product` as SCD1 via `AUTO CDC FROM SNAPSHOT` against the daily product snapshot.

## Done criteria

- Hand-written and managed SCD2 versions of `dim_customer` produce identical history for the same input batches.
- You can explain, without looking it up, the difference between SCD1 and SCD2 and when you'd choose each.
- An out-of-order CDC event is handled correctly (doesn't silently overwrite a newer record with an older one).

## My notes

_(fill in as you go)_
