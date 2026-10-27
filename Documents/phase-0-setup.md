# Phase 0 — Setup

**Branch:** `phase-0-setup`

## Goal

Get the tooling, repo and conventions in place so every later phase can focus purely on data engineering concepts, not environment friction.

## What you'll learn

- Databricks CLI auth (`databricks auth login`) and what a profile/token actually is.
- Unity Catalog basics: catalog vs schema vs Volume, and why Volumes (not DBFS) are the modern way to land files.
- Git branch-per-phase workflow and why each phase gets its own doc here.
- What Claude Code reads automatically (`CLAUDE.md`) vs what you read yourself (`Documents/`).

## Olist entities/tables involved

None directly — this phase is pure environment setup. The one piece of real data work already done is `notebooks/01_collect_data_from_kaggle.py` on `main`, which uses `kagglehub` to pull all 9 Olist CSVs into `/Volumes/volumes/default/processing/Brazilian_E-Commerce_public_Data/`.

## Steps

- [x] Initialize git repo, add GitHub remote.
- [x] Write `notebooks/01_collect_data_from_kaggle.py` (kagglehub ingestion) and merge it into `main`.
- [x] Write `CLAUDE.md` adapted to the Olist/Brazil E-Commerce project.
- [x] Write this `Documents/` learning architecture (master doc + per-phase docs).
- [ ] Install/confirm local tooling: VS Code + Databricks extension, Databricks Connect, Databricks CLI, Python 3.11+.
- [ ] Run `databricks auth login` against your workspace and confirm `databricks bundle validate` (once a `databricks.yml` exists in Phase 1) can authenticate.
- [ ] Create the Unity Catalog catalog/schemas you'll use: `brazil_ecommerce_dev` with `bronze`, `silver`, `gold`, `ops` schemas.
- [ ] Fill in "My level" and "Hours per week" at the bottom of `CLAUDE.md`.

## Done criteria

- `databricks auth login` succeeds and `databricks bundle validate` runs without an auth error.
- `brazil_ecommerce_dev` catalog exists with its four schemas.
- CLAUDE.md's "Current status" section reflects your real skill level/hours.
- This phase's doc and `Documents/00_learning_architecture.md` are merged to `main` via PR.

## My notes

_(fill in as you go — what tripped you up, what clicked, questions for next time)_
