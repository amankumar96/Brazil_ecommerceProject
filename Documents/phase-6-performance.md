# Phase 6 — Performance / Catalyst

**Branch:** `phase-6-performance`

## Goal

Understand how Spark actually executes your queries, and use that understanding to make the Gold layer fast.

## What you'll learn

- Reading `.explain("extended")` and `.explain("formatted")` physical plans.
- Predicate/column pushdown and partition pruning.
- Broadcast join vs shuffle join, and when Spark picks each.
- Adaptive Query Execution (AQE) and data skew — using Olist's **real** São Paulo-state order skew instead of an artificial knob.
- Liquid clustering vs traditional partitioning.
- Delta time travel, `OPTIMIZE` (file compaction, Z-ordering/clustering), and `VACUUM` (and why its retention default is a safety feature, not a bug).

## Olist entities/tables involved

`fact_orders` and its dimensions from Phase 5 — large enough (100k+ orders) to show real shuffle/skew behavior.

## Steps

- [ ] Run `.explain("formatted")` on a `fact_orders` join query; identify the join strategy Spark chose.
- [ ] Force a shuffle join where a broadcast would be better (or vice versa) and compare runtimes.
- [ ] Query `fact_orders` filtered by São Paulo state vs another state; observe the skew in the Spark UI's stage view.
- [ ] Apply liquid clustering to `fact_orders` on a high-cardinality, frequently-filtered column; compare query times before/after.
- [ ] Run `OPTIMIZE` and `VACUUM` (with an explicit, safe retention) on one table; confirm `DESCRIBE HISTORY` and time travel still work as expected.

## Done criteria

- You can read a physical plan and point to where a shuffle happens and why.
- You've measured (not just read about) a performance difference from AQE/skew handling, liquid clustering, or `OPTIMIZE`.
- You can explain, in your own words, why `VACUUM`'s default retention protects time travel.

## My notes

_(fill in as you go)_
