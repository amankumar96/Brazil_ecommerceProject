# Phase 7 — Production

**Branch:** `phase-7-production`

## Goal

Make the whole pipeline deployable and testable like a real production data engineering project, not just a pile of notebooks.

## What you'll learn

- Databricks Asset Bundles: `databricks.yml` dev/prod targets, variables (so the catalog is never hard-coded).
- Lakeflow Jobs: orchestrating Bronze → Silver → Gold as a scheduled/triggered job.
- pytest for the pure functions in `src/brazil_ecommerce/` and `src/generator/`.
- GitHub Actions CI: lint (`ruff`), test (`pytest`), and `databricks bundle validate` on every PR.

## Olist entities/tables involved

The whole pipeline built in Phases 1–5, now wrapped for deployment rather than extended with new data.

## Steps

- [ ] Flesh out `databricks.yml` with real `dev` and `prod` targets (prod untouched without explicit permission, per `CLAUDE.md` safety rules).
- [ ] Write `resources/job.yml` orchestrating the Bronze → Silver → Gold pipeline end to end.
- [ ] Ensure `pytest -q` covers the generator and transform functions, and passes cleanly.
- [ ] Write `.github/workflows/ci.yml`: ruff check/format, pytest, `databricks bundle validate` on PRs.
- [ ] Run `databricks bundle deploy -t dev` and `databricks bundle run -t dev <job>` end to end.

## Done criteria

- `databricks bundle validate` and `deploy -t dev` succeed with no hard-coded catalog names.
- CI runs lint + tests + bundle validate on every PR and is green.
- The end-to-end job run produces fresh Gold tables from a clean dev catalog.

## My notes

_(fill in as you go)_
