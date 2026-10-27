# Phase 9 — Own agents

**Branch:** `phase-9-own-agents`

## Goal

Go from *using* Claude Code to understanding and building the agentic pieces yourself: skills, subagents, hooks, and a from-scratch RAG agent over this project's own docs.

## What you'll learn

- The agent loop: LLM + tools + (decide → call tool → read result → repeat) + stop condition — building it by hand, not through a framework.
- When a Skill earns its own file vs just living in `CLAUDE.md` (on-demand procedure vs always-on context).
- When a Subagent is worth the isolated context vs just doing the work inline.
- Hooks: deterministic automation around tool calls, with no LLM involved.
- RAG fundamentals: chunk → embed → index → retrieve → generate with citations — built from scratch (no LangChain-style framework), with your own `search_docs` and `run_sql` tools.
- Evaluating an agent: writing a 20-question eval set and scoring against it, not just eyeballing a few answers.

## Olist entities/tables involved

The RAG corpus is `docs/` (data dictionary, runbook) plus the Gold schema for `run_sql` answers; no new Olist tables are added in this phase.

## Steps

- [ ] Write `docs/data_dictionary.md` and `docs/runbook.md` — these double as the RAG corpus.
- [ ] Build the RAG agent in `agents/rag_agent/`: chunking, embedding, a simple vector index, retrieval, and a hand-written agent loop (not a framework).
- [ ] Give it two tools: `search_docs` (RAG retrieval) and `run_sql` (query Gold via Databricks Connect).
- [ ] Write a 20-question eval set covering both tools; score the agent and iterate.
- [ ] Add at least one project Skill (`.claude/skills/`) for a repeated task in this repo, and explain in its own words why it's a Skill and not a `CLAUDE.md` section.
- [ ] Add at least one Subagent and one Hook, each with a one-paragraph justification of why that mechanism (vs the alternatives) fit the job.

## Done criteria

- The RAG agent answers at least 15/20 eval questions correctly, with citations back to `docs/`.
- You can explain, unprompted, the difference between a Skill, a Subagent, a Hook, and MCP — and why you picked each one you built.

## My notes

_(fill in as you go)_
