# HANDOFF — next-chat brief (layouts + variability + audit)

> **✅ COMPLETED — shipped as `v0.6.0` on 2026-06-11.** All three goals below landed (plus English-only hardening): see `CHANGELOG.md` § 0.6.0 and `reports/2026-06-11-v0.6.0-session-report.md` for what was done and the audit findings. The next milestone is **v0.7.0 — process discipline** (see `RESUME.md` § 4). This file is kept for historical context only.

> **Purpose.** Self-contained context for a fresh session continuing this skill. Read this first, then `RESUME.md` and `CHANGELOG.md`. Created 2026-05-09 after v0.5.4 shipped.

## What this project is
A self-contained Claude skill that generates executive-grade PowerPoint decks (`.pptx`) from scratch using **ExecEngine**, a python-pptx-based engine. MBB-consulting design discipline: forest-green palette, sans-serif typography, Minto pyramid structure, machine-readable QA gates. Apache 2.0 fork of likaku's Mck-ppt-design-skill — the attribution chain must stay intact (a CI job scans for brand leakage and verifies the LICENSE/NOTICE chain).

- **Project root:** `/home/ajb/Projects/MBB-PPT-2/`
- **Public repo:** https://github.com/albertojb/mbb-ppt-generator
- **Start by reading:** this file, then `RESUME.md`, then `CHANGELOG.md`.
- **Post-mortem driving the roadmap:** `/home/ajb/claude-cowork-linux/mbb-ppt-skill-postmortem.md`

## Current state
- **Latest release tag:** `v0.5.4`. **`main` HEAD:** `86d4d62` (or later). PC and GitHub fully in sync, working tree clean.
- **CI:** green on `main` (tests on Python 3.10–3.13 + a brand-leakage scan). The v0.5.x *tag* pages show a red X on the leakage-scan job only — a docs-allowlist oversight fixed in `86d4d62`; the test job passed on every tag. Cosmetic.
- **Tests:** 37/37 passing — `python3 -m pytest tests/`.

## What v0.5.x shipped
- **v0.5.0** — Fixed three S3-gate bugs (value_chain / numbered_list_panel oval-label false failures; harvey_ball_table width overflow). Added two global gates: `executive_summary` capped at ≤15% of content slides; visual-density floor scaling as `max(2, N // 4)`.
- **v0.5.1** — `references/api-schemas.yaml` is now the single source of truth for all 67 layouts (signature, family, param shapes, char budgets, visual flag). `generate_cheatsheet.py` emits the cheatsheet from it. `gate_check_content.py` validates structurally from it. New `references/known-pitfalls.md`. Deleted old `layout-matrix.yaml`.
- **v0.5.2** — Redesigned `cover()` (navy left-block + 36pt right pane, fits ~50 chars); `cover_centered()` keeps the legacy layout. Dropped the duplicate chart sub-title in `grouped_bar` / `stacked_bar`.
- **v0.5.3 + v0.5.4** — Eight new layouts: `ask`, `numbered_tiles`, `concept_three`, `journey_map`, `pyramid_staircase`, `cycle_4stage`, `index_callout`, `extension_rows`.

## Architecture facts for the next session
- **Engine:** `plugins/mbb-ppt-generator/skills/mbb-ppt-generator/mbb_ppt/engine.py` — ~70 layout methods, one per slide.
- **Schema (edit this, NOT the cheatsheet):** `.../references/api-schemas.yaml`. After editing, run `.../references/scripts/generate_cheatsheet.py` to regenerate `api-cheatsheet.md`.
- **Gates:** `.../references/scripts/gate_check_content.py` (S3, content) and `gate_check_render.py` (S4, render). The content gate reads the schema for structural validation; layout-specific quirks live in code.
- **Adding a layout:** engine method → schema entry → (add to `VISUAL_LAYOUTS` in `gate_check_content.py` if it's a chart/diagram) → regression test in `tests/test_gates.py` → regenerate cheatsheet. A smoke test fails if any engine method lacks a schema entry, so they can't silently drift.
- **Release ritual:** bump version in 4 places (`pyproject.toml`, `plugins/mbb-ppt-generator/.claude-plugin/plugin.json`, `mbb_ppt/__init__.py`, the assert in `tests/test_smoke.py`), update CHANGELOG, commit, tag, `git push && git push --tags`. **Always check CI after pushing** (`gh run list`) — local pytest alone is not enough (the leakage scan only runs in CI).
- **Do NOT touch install behavior** — settled and parked (GUI `.skill` drop-in + terminal one-liner). See `CLAUDE.md`.

## Goals for this next phase

### 1. Add new layouts
Specific layouts to be attached in the chat. Each follows the add-a-layout ritual above.

### 2. Add sensible structural variability to layout *usage* (not just availability)
- Don't over-use any single layout — the `executive_summary` ≤15% cap was a first step; **generalize the principle** to other permissive layouts.
- **Maintain consistency where it matters:** thematically similar pages should reuse the same template (e.g. every case-study slide looks the same). Variability and consistency must coexist — vary across themes, stay consistent within a theme.
- Add layouts closer to **what the user actually uses day-to-day** (examples coming in the chat).

### 3. Multi-dimensional audit of the skill
- **Speed / performance** — is rendering or gate-checking slower than necessary?
- **Token usage** — find unnecessary context loading, bloated references, redundant instructions (e.g. bulk-loading all layout docs when a deck uses three; duplicated guidance). Anything inflating AI cost per run.
- **Contradicting / redundant rules** — hunt for conflicting guidance across `SKILL.md`, the gates, the schema, and reference docs that could make the skill slow, confusing, or expensive.

### Note on the prior roadmap
The next planned milestone before this was **v0.6.0** (process discipline: S2 storyboarding gate, render-gate auto-fix, stronger section_divider). The audit + variability + new-layout work now takes priority; fold the audit findings into the v0.6.0 plan rather than treating them as separate.
