# CLAUDE.md — Brazil E-Commerce Lakehouse

## Who I am and how to help me

I am **learning data engineering** through this project. Teaching matters more than speed.

- **Explain before you write.** For any new concept (Auto Loader, SCD2, Catalyst, etc.), give a short plain-English explanation first, then the code.
- **Let me write first when I ask to learn.** If I say "I'll try", review my code instead of rewriting it. Point out issues and explain why; don't silently fix.
- **Show trade-offs.** When there are two reasonable approaches, show both briefly and say which production teams usually choose.
- **No magic.** When you use a Databricks managed feature, tell me in 1–3 lines what it does under the hood.
- **End each completed task with 2–3 check-your-understanding questions** for me.
- Keep answers short and concrete. Use small datasets. Don't over-engineer.

## Project in one paragraph

This project is built on the real **Olist Brazilian E-Commerce** dataset from Kaggle (orders, order items, payments, reviews, customers, products, sellers, geolocation — 9 CSVs), fetched via `kagglehub` into a Unity Catalog Volume. Because the real dataset is a static one-time snapshot with no natural streaming or change-feed, a small companion **synthetic generator** layers simulated daily order arrivals, a customer change-data-capture (CDC) feed, and clickstream events on top of the real data, so streaming/CDC/SCD lessons still have something real to practice on. A Lakeflow Spark Declarative Pipeline ingests the result with Auto Loader into **Bronze**, cleans and historises it in **Silver** (expectations, dedup, SCD1, SCD2), and models a star schema in **Gold**. Gold is served to a Genie space, dashboards and a from-scratch RAG agent. Everything is deployed from Git with Databricks Asset Bundles.

**Learning rule:** important concepts are built twice — first by hand (PySpark/SQL, e.g. SCD2 with `MERGE INTO`), then with the managed feature (e.g. `AUTO CDC ... STORED AS SCD TYPE 2`) — and the results are compared.

## Environment and constraints

- **Databricks Free Edition**: serverless compute only (no custom clusters, no GPUs), fair-use daily quota, non-commercial.
  - Run at most 1–2 workloads at a time (notebook + pipeline together is the limit).
  - Streams use `trigger(availableNow=True)`, never always-on.
  - Keep data small: thousands to low millions of rows (Olist's real tables are already in this range).
- Local dev: VS Code + Databricks extension, Databricks Connect, Databricks CLI, Python 3.11+.
- Version control: Git + GitHub; Databricks Git folders for workspace sync.
- AI tools: Claude Code (you) locally; Genie Code in the workspace.
- Databricks features change fast. If you are unsure whether syntax or a feature is current, say so and check the docs (docs.databricks.com) rather than guessing.

## Naming conventions

- Catalogs: `brazil_ecommerce_dev`, `brazil_ecommerce_prod`
- Schemas: `bronze`, `silver`, `gold`, `ops`
- Landing Volume: `/Volumes/brazil_ecommerce_<env>/bronze/raw/<source>/`
- Checkpoints / schema locations: `/Volumes/brazil_ecommerce_<env>/ops/checkpoints/<table>/`
- Tables: `snake_case`. Bronze `brz_<source>`, Silver `slv_<entity>`, Gold `fact_<process>` / `dim_<entity>` / `mv_<metric>`
- SCD2 columns: `__START_AT`, `__END_AT` (AUTO CDC); hand-written version uses `valid_from`, `valid_to`, `is_current`
- Never hard-code the catalog; read it from bundle variables / pipeline config.

## Repo structure

```
Brazil_ecommerceProject/
├── databricks.yml              # Asset Bundle: dev + prod targets
├── notebooks/
│   └── 01_collect_data_from_kaggle.py   # kagglehub ingestion: Olist CSVs -> Volume (already on main)
├── resources/
│   ├── pipeline.yml            # Lakeflow Declarative Pipeline
│   └── job.yml                 # Orchestration job
├── src/
│   ├── generator/              # Synthetic layer on top of real Olist data: daily arrival batches,
│   │                           # customer CDC feed, clickstream, product snapshot w/ injected changes
│   ├── learn/                  # Hand-written learning notebooks (Auto Loader, MERGE SCD2, explain())
│   ├── pipeline/
│   │   ├── bronze/             # Auto Loader ingestion (.py)
│   │   ├── silver/             # Cleaning, expectations, AUTO CDC (.sql / .py)
│   │   └── gold/               # Star schema + materialized views (.sql)
│   └── brazil_ecommerce/       # Reusable Python package (pure transform functions)
├── tests/                      # pytest unit tests
├── agents/rag_agent/           # From-scratch RAG agent (Phase 9)
├── docs/                       # Data dictionary, runbook (also the RAG corpus)
├── Documents/                  # Human-readable learning architecture + one doc per phase/branch
│   ├── 00_learning_architecture.md
│   └── phase-0-setup.md ... phase-9-own-agents.md
├── .claude/
│   ├── skills/                 # Project skills (SKILL.md folders)
│   ├── agents/                 # Subagents
│   └── settings.json
├── .mcp.json
├── CLAUDE.md
└── .github/workflows/ci.yml
```

## Data sources

| Source | Format | Arrives | Origin | Used to learn |
| --- | --- | --- | --- | --- |
| orders | JSON, many small files | every run | Real: `olist_orders_dataset` + `olist_order_items_dataset` + `olist_order_payments_dataset` + `olist_order_reviews_dataset`, split by `generator/` into daily arrival batches | Auto Loader, dedup, late data, facts |
| clickstream | JSON, schema grows (`coupon_code` added mid-project), some malformed rows | every run | Synthetic (Olist has no clickstream): Faker-generated events referencing real `product_id`/`customer_id` | schema evolution, `_rescued_data` |
| customers_cdc | JSON change feed: `op` (INSERT/UPDATE/DELETE), `seq`, `customer_id`, city, tier… | every run, sometimes out of order | Synthetic change feed derived from real `olist_customers_dataset` + `olist_geolocation_dataset` | SCD2, MERGE, AUTO CDC |
| products | CSV full snapshot | daily | Real `olist_products_dataset`, replayed daily with occasional synthetic price/category changes | SCD1, AUTO CDC FROM SNAPSHOT |

Skew note: Olist has real geographic skew (São Paulo state dominates order volume) — use this directly for the AQE/skew lesson instead of an artificial knob.

## Phases (current phase is tracked at the bottom)

0. **Setup** — tools, CLI auth, repo, Claude Code. *(`notebooks/01_collect_data_from_kaggle.py` already covers the Kaggle→Volume ingestion piece.)*
1. **Spark, Delta, Unity Catalog basics** — catalog/schemas/Volume, `src/generator/`, `_delta_log`, `DESCRIBE HISTORY`, `.explain()`.
2. **Auto Loader → Bronze** — `cloudFiles`, `schemaLocation`, checkpoints, `availableNow`, schema evolution, rescued data; notebook first, then pipeline.
3. **Silver** — casting, standardising, dedup by key + sequence, expectations (warn / drop / fail).
4. **CDC and SCD** — SCD2 by hand with `MERGE INTO`, then `AUTO CDC ... STORED AS SCD TYPE 2`; products SCD1 via `AUTO CDC FROM SNAPSHOT`; out-of-order test.
5. **Gold** — `fact_orders`, `dim_customer` (SCD2), `dim_product` (SCD1), `dim_seller`, `dim_date`; point-in-time joins; materialized views.
6. **Performance / Catalyst** — `explain("extended"/"formatted")`, pushdown, pruning, broadcast vs shuffle, AQE + skew, liquid clustering, time travel, `OPTIMIZE`, `VACUUM`.
7. **Production** — Asset Bundle dev/prod, Lakeflow Job, pytest, GitHub Actions (lint, test, `bundle validate`).
8. **Genie + Genie Code** — Genie space over Gold (comments, trusted SQL, sample questions); MCP connection to Databricks.
9. **Own agents** — skills, subagents, hooks; from-scratch RAG agent (`search_docs`, `run_sql` tools, hand-written loop) + 20-question eval.

Each phase: own branch (`phase-N-<topic>`), its own doc in `Documents/`, PR to `main` when done criteria pass.

## Coding standards

- Python: type hints, small pure functions in `src/brazil_ecommerce/` so they can be unit-tested without Spark where possible; `ruff` for lint/format.
- PySpark: DataFrame API, no `collect()` on large data, no Python UDFs unless explained why.
- SQL: uppercase keywords, one column per line in SELECTs for Gold models, comment every Gold table and column (Genie depends on it).
- Pipelines: every Silver table has at least one expectation.
- Tests: `pytest -q` must pass before suggesting a commit.
- Commits: small, imperative messages (`Add Auto Loader ingestion for orders`).

## Commands

```bash
databricks auth login                  # authenticate CLI
databricks bundle validate             # check bundle config
databricks bundle deploy -t dev        # deploy to dev
databricks bundle run -t dev <job>     # run job/pipeline
pytest -q                              # unit tests
ruff check . && ruff format .          # lint + format
```

## Safety rules

- Never run anything against `brazil_ecommerce_prod` or `-t prod` without me explicitly asking.
- Never `DROP`, `TRUNCATE`, `VACUUM` with low retention, or delete checkpoints without asking first and explaining the consequence.
- Never commit secrets or tokens; use Databricks secrets / environment variables.
- Ask before deploying, deleting files or force-pushing.

## AI concepts I am learning (use these terms consistently)

- **Agent** = LLM + tools + a loop (decide → call tool → read result → repeat) + stop condition.
- **CLAUDE.md** = always-on context · **Skill** = on-demand procedure/knowledge · **Subagent** = isolated context for a focused job · **MCP** = connection to external systems · **Hook** = deterministic automation, no LLM.
- **RAG** = chunk → embed → index → retrieve → generate with citations.
- **Taxonomy** = consistent naming/categorisation (catalog → schema → table → column, plus comments and tags); it is what makes Genie and RAG accurate.

When I build skills/subagents, explain why each one exists and what problem it solves versus putting the same text in CLAUDE.md.

## Current status

- Current phase: **0 — Setup**
- My level: _(fill in: Python / SQL — beginner / comfortable / strong)_
- Hours per week: _(fill in)_
- Notes: `main` already has `notebooks/01_collect_data_from_kaggle.py` (kagglehub → Volume ingestion), which gets Phase 1/2's "real data available in a Volume" groundwork done early.
