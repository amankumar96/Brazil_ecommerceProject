# Phase 8 — Genie + Genie Code

**Branch:** `phase-8-genie`

## Goal

Serve the Gold star schema to business users through a Genie space, and understand what makes Genie's answers trustworthy vs wrong.

## What you'll learn

- How Genie uses table/column comments and sample questions to generate SQL — and why Phase 5's comments matter.
- Trusted SQL: curating known-good queries so Genie prefers them over ad-hoc generation for common questions.
- Writing good sample questions that cover the star schema's real use cases (sales by state, top sellers, SCD2 history questions).
- Connecting to Databricks via MCP from Genie Code / Claude Code.

## Olist entities/tables involved

The full Gold star schema from Phase 5 (`fact_orders`, `dim_customer`, `dim_product`, `dim_seller`, `dim_date`, plus any materialized views).

## Steps

- [ ] Create a Genie space pointed at the Gold schema.
- [ ] Write 5-10 sample questions covering facts, dimensions, and at least one SCD2 history question ("what tier was customer X at the time of their first order?").
- [ ] Add 2-3 trusted SQL queries for the most common question types.
- [ ] Set up the MCP connection from Claude Code / Genie Code to this Databricks workspace.
- [ ] Ask Genie a question it gets wrong; diagnose why (missing comment? ambiguous column name? missing sample question?) and fix it.

## Done criteria

- Genie answers at least 5 real business questions correctly without manual SQL editing.
- You've found and fixed at least one Genie failure by improving metadata (comments/sample questions), not by hand-writing the answer.

## My notes

_(fill in as you go)_
