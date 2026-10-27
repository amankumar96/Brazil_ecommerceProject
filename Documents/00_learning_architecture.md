# Learning Architecture — Brazil E-Commerce Lakehouse

This is the human-readable map of the project. `CLAUDE.md` is the always-on context Claude reads automatically; this folder is for *you* — read it, update it, and use it to track where you are.

## Starting point

- **Dataset:** real [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) data from Kaggle — 9 CSVs: orders, order items, payments, reviews, customers, products, sellers, geolocation, and a category-name translation table.
- **Repo state today:** `main` already contains `notebooks/01_collect_data_from_kaggle.py`, a Databricks notebook that uses `kagglehub` (`KaggleDatasetAdapter.PANDAS`) to pull every CSV and write it into a Unity Catalog Volume (`/Volumes/volumes/default/processing/Brazilian_E-Commerce_public_Data/`). That's the raw-data starting point every later phase builds on.
- **Gap to solve:** the real dataset is a one-time static snapshot — no streaming arrivals, no change-data-capture (CDC) feed, no clickstream. To still learn Auto Loader, schema evolution, SCD1/SCD2 and CDC hands-on, a small synthetic **generator** (built in Phase 1) layers simulated daily order arrivals, a customer CDC feed, and clickstream events on top of the real data. Gold modeling, performance tuning, Genie and the RAG agent all then work on the combined real + synthetic data.

## What you're learning, overall

- **Medallion architecture:** Bronze (raw, Auto Loader) → Silver (clean, deduped, historised) → Gold (star schema, business-ready).
- **Streaming ingestion:** Auto Loader, `cloudFiles`, schema evolution, checkpoints, `trigger(availableNow=True)`.
- **Change tracking:** SCD1 (overwrite) vs SCD2 (full history), done by hand with `MERGE INTO` first, then with Databricks' managed `AUTO CDC` feature — compare the two every time.
- **Data quality:** Lakeflow pipeline expectations (warn / drop / fail).
- **Performance:** Catalyst query plans, pushdown/pruning, shuffle vs broadcast, AQE and data skew, liquid clustering, time travel, `OPTIMIZE`/`VACUUM`.
- **Production practice:** Databricks Asset Bundles (dev/prod targets), Lakeflow Jobs, pytest, CI via GitHub Actions.
- **Serving & AI:** a Genie space over Gold tables, and a from-scratch RAG agent (no framework) with its own tools and eval.
- **Agentic tooling itself:** how CLAUDE.md, skills, subagents, hooks and MCP fit together — built and explained as you go, not just used.

## The branch-per-step convention

Every phase below gets:
1. **Its own branch**, named `phase-N-<topic>` (e.g. `phase-1-spark-delta-basics`).
2. **Its own doc** in this folder (`Documents/phase-N-<topic>.md`), containing the phase's goal, what you'll learn, the Olist tables involved, a steps checklist, done-criteria, and a free space for your own notes in your own words.
3. **A pull request into `main`** once the done-criteria in that phase's doc are met — `main` only ever holds finished, working phases.

Rule of thumb: don't start phase N+1's branch until phase N's PR is open (or merged). Keep work-in-progress to one phase at a time, matching the Databricks Free Edition's "1–2 workloads at a time" constraint in `CLAUDE.md`.

## Roadmap

| # | Phase | Branch | Doc | What you'll learn | Olist entities involved |
|---|---|---|---|---|---|
| 0 | Setup | `phase-0-setup` | [`phase-0-setup.md`](phase-0-setup.md) | Tooling, CLI auth, repo conventions, Claude Code | — (kagglehub notebook already in `main`) |
| 1 | Spark, Delta, Unity Catalog basics | `phase-1-spark-delta-basics` | [`phase-1-spark-delta-basics.md`](phase-1-spark-delta-basics.md) | Catalog/schema/Volume, Delta `_delta_log`, `DESCRIBE HISTORY`, `.explain()`; build the synthetic generator | orders, customers, products (seed for generator) |
| 2 | Auto Loader → Bronze | `phase-2-autoloader-bronze` | [`phase-2-autoloader-bronze.md`](phase-2-autoloader-bronze.md) | `cloudFiles`, schema evolution, `_rescued_data`, checkpoints, `availableNow` | orders, clickstream (both via generator output) |
| 3 | Silver | `phase-3-silver` | [`phase-3-silver.md`](phase-3-silver.md) | Casting/standardising, dedup by key+sequence, expectations | all Bronze tables |
| 4 | CDC and SCD | `phase-4-cdc-scd` | [`phase-4-cdc-scd.md`](phase-4-cdc-scd.md) | Hand-written `MERGE INTO` SCD2, then `AUTO CDC ... STORED AS SCD TYPE 2`; SCD1 via `AUTO CDC FROM SNAPSHOT`; out-of-order handling | customers_cdc, products |
| 5 | Gold | `phase-5-gold` | [`phase-5-gold.md`](phase-5-gold.md) | Star schema, point-in-time joins, materialized views | fact_orders, dim_customer, dim_product, dim_seller, dim_date |
| 6 | Performance / Catalyst | `phase-6-performance` | [`phase-6-performance.md`](phase-6-performance.md) | Query plans, pushdown, pruning, AQE + skew (São Paulo skew), liquid clustering, time travel, OPTIMIZE/VACUUM | fact_orders and friends |
| 7 | Production | `phase-7-production` | [`phase-7-production.md`](phase-7-production.md) | Asset Bundles dev/prod, Lakeflow Job, pytest, GitHub Actions CI | whole pipeline |
| 8 | Genie + Genie Code | `phase-8-genie` | [`phase-8-genie.md`](phase-8-genie.md) | Genie space over Gold, trusted SQL, sample questions, MCP connection | Gold star schema |
| 9 | Own agents | `phase-9-own-agents` | [`phase-9-own-agents.md`](phase-9-own-agents.md) | Skills, subagents, hooks; from-scratch RAG agent + 20-question eval | docs/ corpus + Gold |

## How to use this folder day to day

- Start a phase by reading its doc, creating its branch off `main`, and working through its checklist with Claude.
- When a concept surprises you or clicks, write it in that phase's "My notes" section — in your own words, not Claude's.
- When the done-criteria are met, open a PR to `main`, then move to the next phase's doc.
