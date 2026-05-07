# Changelog

All notable changes to MBB PPT Generator are documented in this file. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This project is an Apache 2.0-licensed adaptation of [`Mck-ppt-design-skill`](https://github.com/likaku/Mck-ppt-design-skill) by Kaku Li / likaku. Versions before `0.1.0` of this fork correspond to upstream releases (most recently `v2.3.3-harness-v2`); see the upstream [CHANGELOG](https://github.com/likaku/Mck-ppt-design-skill/blob/main/CHANGELOG.md) for the engine's pre-fork history.

---

## [0.1.0] — 2026-05-07 (initial fork)

### Added (this fork's contributions)

- **English-only skill specification** ([`SKILL.md`](SKILL.md)) — full replacement for upstream `SKILL.md`, with the five-stage workflow (S1 brief → S2 outline → S3 content → S4 render+QA → S5 deliver), Pyramid Principle communication framework, and Self-Refinement protocol stated in English.
- **Modern neutral sans-serif heading typography.** Replaced upstream `Georgia` (transitional serif) with `DM Sans` (preferred), `Inter` (equivalent), `Calibri` (fallback). Body remains `Arial`.
- **`ExecEngine` documentation alias.** The underlying class `mck_ppt.MckEngine` and module `mck_ppt` are unchanged for code-level Apache 2.0 compatibility, but documentation refers to the engine by its functional role: ExecEngine.
- **Eight new production guard rails (Rules 11–18)** addressing text overflow, z-order discipline, dynamic font shrink, title char limits, content area boundary, inter-element gaps, insight bar height, and page-number placement lock. Rules 1–10 retained from upstream.
- **Color additions:** `HEADING_ACCENT`, `SECTION_BG`, and an optional warm palette (`WARM_NAVY`, `WARM_GOLD`, `WARM_STONE`) for heritage / philanthropic decks.
- **Two machine-readable gate scripts** with English error messages: [`gate_check_content.py`](references/scripts/gate_check_content.py) (S3) and [`gate_check_render.py`](references/scripts/gate_check_render.py) (S4). Render gate uses a `_resolve_skill_root()` walker so it self-locates the bundled `mck_ppt/` package — no hardcoded install path.
- **`ENGINE_BUG_WHITELIST`** with required textual evidence comments — codifies which QA categories are documented engine quirks (`peer_font_inconsistency`, `chart_legend_overflow` for `timeline` only). Verbal exemptions are not accepted.
- **Layout capacity matrix** ([`layout-matrix.yaml`](references/layout-matrix.yaml)) with explicit `char_budget`, `tuple_arity`, and special constraints per layout, used by the S3 gate.
- **Knowledge router** ([`INDEX.md`](references/INDEX.md)) — stage → load map for context discipline.
- **Three framework reference files** ([`engine-api.md`](references/framework/engine-api.md), [`guard-rails.md`](references/framework/guard-rails.md), [`planning-guide.md`](references/framework/planning-guide.md)) — scannable, on-demand documentation loaded by stage.
- **Self-Refinement persistence** — three seed `experiences/` files (`overflow.md`, `layout-pitfalls.md`, `chart-limits.md`) with numbered `Experience NNN` entries documenting past defects and fixes; protocol for appending pattern-level lessons after each run.
- **QA visual checklist** ([`MBB_PPT_QA_CHECKLIST.md`](MBB_PPT_QA_CHECKLIST.md)) with § 0 gate-script gate as the first hard requirement before any visual review begins.
- **Self-contained packaging** — the `mck_ppt/` Python engine is bundled in this repository. No external dependency on upstream Likaku skill installation.

### Changed (this fork's modifications to upstream code)

- `mck_ppt/constants.py`: replaced `FONT_HEADER = 'Georgia'` with `HEADING_FONT = "DM Sans"` and added the v2.0 boundary, page-number, and guard-rail constants. Backward-compat aliases (`FONT_HEADER`, `FONT_BODY`, `FONT_EA`) retained.
- `mck_ppt/engine.py`: 27 inline edits replacing CJK default parameter values with English equivalents in `cover` (n/a, header docstring kept), `toc`, `big_number`, `table_insight`, `scorecard`, `key_takeaway`, `action_items`, `checklist`, `kpi_tracker`, `risk_matrix`, `harvey_ball_table`, `dashboard_kpi_chart`, `metric_comparison`, `numbered_list_panel`, and `stakeholder_map`. Engine behavior unchanged; only user-visible default strings.

### Removed

- CJK font handling (`FONT_EA = 'KaiTi'` → `FONT_EA = 'Arial'` retained as a no-op for backward compat).
- Upstream `experiences/cjk-issues.md` (English-only skill).
- Upstream WeChat QR placeholder.
- Upstream README marketing language and Chinese-language framing.

### Retained from upstream (unchanged)

- The full `mck_ppt/` engine implementation — `engine.py` (~3,200 lines), `core.py`, `qa.py`, `deck_builder.py`, `review.py`, `cover_image.py`, `storylines/`. All copyright headers (`Copyright 2024-2026 Kaku Li`) preserved.
- `LICENSE` (Apache 2.0).
- The 67 layout methods, BLOCK_ARC chart implementations, three-layer XML cleanup, and Harvey Ball indicator logic.
- The retired-layout list (`venn`, `cycle`, `funnel`, `pie`, `gauge`) — methods exist for back-compat, not promoted.

### Known issues / pending

- Twelve `references/layouts/*.md` per-layout reference files are not yet written. SKILL.md's routing table points at them; the model falls back to engine docstrings until they land.
- Two CJK files in the engine bundle remain untranslated: `mck_ppt/storylines/ai_enterprise.py` (full Chinese storyline, opt-in only) and `mck_ppt/cover_image.py` Tencent prompt strings (opt-in only).
- `references/team/{brand-guide,presentation-convention}.md` are not yet written in English; upstream Chinese versions are in the local `_likaku_may3/` extract for reference.
- No `examples/` directory yet.

---

## Notes on attribution

This fork preserves Kaku Li's copyright in every Python source file (`mck_ppt/*.py`) and credits the upstream project in [`NOTICE`](NOTICE), [`README.md`](README.md), and the top of [`SKILL.md`](SKILL.md). Per Apache 2.0 § 4(c), modifications introduced by this adaptation are documented inline in `mck_ppt/constants.py` and enumerated in this changelog.
