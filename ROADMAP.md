# ROADMAP — MBB PPT Generator

> **Draft.** Derived from actual shipped state as of v0.8.0 plus remaining work. Completed epics are marked done. Specs exist only for the first unfinished epic.

---

## ✅ Epic 1 — Foundation & rebrand (v0.1.0–v0.2.2)

Apache 2.0 fork of likaku's Mck-ppt-design-skill. Module renamed `mbb_ppt`, class `MbbEngine`, alias `ExecEngine`. Forest-green palette, sans-serif typography, English-only. Five-stage workflow (S1–S5). Two machine-readable gates (`passed: bool` in code, never a verbal claim). Self-refinement via append-only `experiences/`. CI on Python 3.10–3.13.

## ✅ Epic 2 — Install & surface support: Cowork (v0.3.0–v0.4.2)

GUI `.skill` drag-drop (primary) and terminal one-liner (secondary). Hard STOP directive in `CLAUDE.md` to prevent Cowork-sandbox install spirals. Plugin marketplace packaging (`claude plugin marketplace add`). Fast Track for ≤5 content slides.

## ✅ Epic 3 — Layout quality & engine correctness (v0.5.0–v0.5.4)

Gate bugs fixed (value_chain, numbered_list_panel, harvey_ball_table). `api-schemas.yaml` as single source of truth for all 67 layouts; cheatsheet generated from it. Cover redesigned (navy left-block, 36pt, fits ~50 chars). Eight archetype layouts added to break `executive_summary` monoculture: `ask`, `numbered_tiles`, `concept_three`, `journey_map`, `pyramid_staircase`, `cycle_4stage`, `index_callout`, `extension_rows`. Visual-density floor scales as `max(2, N // 4)`.

## ✅ Epic 4 — Variability, audit & hardening (v0.6.0)

Layout-share cap per deck. Theme-consistency gate (same layout for same-theme slides). Speed/token/contradiction audit with fixes applied. English-only hardening (CJK purge + CI scan). 44/44 tests passing.

---

## ✅ Epic 5 — Process discipline (v0.7.0)

S2 storyboarding gate (`gate_check_storyboard.py`), render-gate `--auto-fix` (font-shrink, max 1 round), `section_divider` redesign (full-width accent bar + numeral + centered title + italic subtitle), `add_text(italic=)` param. 48/48 tests. Version bumped in all 4 locations.

---

## 🔄 Epic 6 — Multi-surface support (v0.8.0 partial) ← in progress

**Foundation shipped in v0.8.0:**
- `mbb_ppt/gates.py` — clean importable seam over the three gate scripts; surfaces call this instead of path-hacking `references/scripts/`
- `mbb_ppt/surfaces/mcp_server.py` — MCP JSON-RPC 2.0 stdio server for GitHub Copilot; run `python3 -m mbb_ppt.surfaces.mcp_server --setup` to get config snippets

**Remaining in Epic 6:**
- End-to-end validation with a real GitHub Copilot session (test all four MCP tools: `gate_storyboard`, `gate_content`, `gate_render`, `render`)
- ZoComputer surface: determine file-write scope; if no local FS, document the API/prompt-injection integration pattern rather than a Python adapter
- Add an MCP setup section to SKILL.md or README so operators know how to connect GitHub Copilot
- Do not regress the Cowork or terminal paths

## Epic 7 — Adoption & discoverability

Screenshots and architecture diagram in README. AI-agent integration walkthrough. CONTRIBUTING and CODE_OF_CONDUCT. Deferred archetype layouts: `cost_curve`, survey waffle/rank-chips, eyebrow-tag primitive. Per-layout reference docs for v0.5.3/v0.5.4 additions.
