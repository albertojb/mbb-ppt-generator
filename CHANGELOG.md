# Changelog

All notable changes to MBB PPT Generator are documented in this file. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This project is an Apache 2.0-licensed adaptation of [`Mck-ppt-design-skill`](https://github.com/likaku/Mck-ppt-design-skill) by Kaku Li / likaku. Versions before `0.1.0` of this fork correspond to upstream releases (most recently `v2.3.3-harness-v2`); see the upstream [CHANGELOG](https://github.com/likaku/Mck-ppt-design-skill/blob/main/CHANGELOG.md) for the engine's pre-fork history.

---

## [0.5.4] — 2026-05-09 (round out the v0.5.x layout catalog)

Closes the remaining four post-mortem § 4 layouts. Combined with v0.5.3, the engine now ships all eight new layouts the post-mortem requested.

### Added engine layouts

- **`pyramid_staircase(title, steps, source='')`** — 4-5 ascending steps, each wider and taller than the last, palette escalating gray → light blue → navy. Use for maturity progression, capability building, increasing scope.
- **`cycle_4stage(title, stages, center_label='', source='')`** — 2×2 grid with clockwise arrows (right / down / left / up). Replaces the legacy retired `cycle()` for continuous-improvement and learning-loop content.
- **`index_callout(title, items, callout, source='')`** — left numbered list (4-7 items) + right detail panel that fully expands a single anchor item. Use for "here are the optional items, and here's the one we're emphasizing."
- **`extension_rows(title, rows, source='')`** — horizontal rows with left vertical accent bar (palette rotates), title on the left, description on the right. Use for modular catalogs and scope extensions.

### Schema + gate

- All four new layouts entered in `api-schemas.yaml` (full per-param shape, char budgets, geometry notes such as "circle fits 14 chars" or "clockwise from top-left").
- `pyramid_staircase` and `cycle_4stage` added to `gate_check_content.py:VISUAL_LAYOUTS` so they count toward the visual-density floor.

### Tests

- 37/37 passing (was 35/35). Two new regression tests:
  - `test_v054_new_layouts_render_clean` — all four render without overflow or user-code errors.
  - `test_v054_layouts_pass_content_gate` — schema-driven structural validation accepts canonical inputs.

---

## [0.5.3] — 2026-05-09 (four new layouts to break the executive_summary monoculture)

The post-mortem flagged executive_summary at 9× in 30 slides. v0.5.0 added the cap; v0.5.3 adds the layouts the model can fall back to. Four of the eight layouts from post-mortem § 4 ship now; the remaining four (pyramid_staircase, cycle 4-stage, index_callout, extension_rows) are still on the v0.5.x roadmap.

### Added engine layouts

- **`ask(title, decisions, footer_text='Decisions sought', source='')`** — closing-slide layout for renewal decks. 3-5 numbered decisions with owner / deadline / status (status renders as a colored dot: pending / in_progress / agreed). Stops the pattern of faking a decision list inside `executive_summary`.
- **`numbered_tiles(title, tiles, source='')`** — 3 (or 4) tiered tiles with fill escalating left-to-right (gray → light blue → navy or gray → light blue → mid → navy). Use for tiered offers, phased rollouts, escalating commitment.
- **`concept_three(title, concepts, source='')`** — three large navy circles connected by arrows, with descriptions underneath. Use for 3-dimensional concepts (intent / cadence / value), 3-stage flows.
- **`journey_map(title, stages, source='')`** — chevron header (4-5 stages) with stakeholder cards (gray) and metric cards (navy) below each stage. Use for customer journeys and persona × metric crosswalks.

### Schema + cheatsheet

- All four new layouts have full entries in `api-schemas.yaml` (signature, family, requires/visual flags, params with tuple slot or dict-key shape, char budgets, and notes for non-obvious geometry like the 14-char circle limit in `concept_three`).
- Cheatsheet regenerated; now lists 71 layouts (66 active + 5 retired).
- `concept_three` and `journey_map` added to `gate_check_content.py:VISUAL_LAYOUTS` so they count toward the visual-density floor.

### Tests

- 35/35 passing (was 33/33). Two new regression tests:
  - `test_v053_new_layouts_render_clean` — all four render without overflow or user-code errors.
  - `test_v053_layouts_pass_content_gate` — schema-driven structural validation accepts canonical inputs.

### Known follow-ups (deferred to later v0.5.x)

- `pyramid_staircase` (proper ascending steps), `cycle` 4-stage loop, `index_callout`, `extension_rows`.
- Per-layout reference docs under `references/layouts/*.md` for the four new methods (post-mortem suggested a one-paragraph addition per family file).

---

## [0.5.2] — 2026-05-09 (cover redesign + chart-subtitle fix)

Layout-quality work continues. v0.5.2 ships the two engine-side fixes the post-mortem flagged: charts re-rendered the action title at 13pt below it (overflowed for any title >38 chars), and the cover only fit ~28 chars at 44pt. Both are gone.

### Added

- **`cover_centered()`** — preserves the v0.5.1 cover layout (44pt centered title, full-bleed image option). Use this when you need an image-overlay cover; otherwise prefer `cover()`.

### Changed

- **`cover()` redesigned** — navy left-block (4.5"×full height) + right text pane (~7.6" wide) at 36pt. Fits ~50 effective chars per title line. Schema's `cover.title` budget bumped from 28 → 50. Passing `cover_image=...` transparently delegates to `cover_centered()` so existing callers using image-overlays do not break.
- **`grouped_bar` and `stacked_bar`** no longer re-render the action title at 13pt under the legend. The chart-subtitle box was the documented overflow trigger for any title >38 chars (post-mortem § 3.5). The legend stays.

### Schema

- Added `cover_centered` entry. Updated `cover` summary and `cover.title.max_chars` to 50.

### Tests

- 33/33 passing (was 30/30). New regression tests:
  - Long action title on grouped_bar / stacked_bar passes the render gate.
  - 45-char cover title renders without overflow.
  - `cover_centered()` is callable and saves a non-empty .pptx.

---

## [0.5.1] — 2026-05-09 (api-schemas.yaml as single source of truth)

Per the post-mortem, the matrix + cheatsheet + gate were three sources for the same constraints, drifting in different directions. v0.5.1 collapses them into one schema. A single edit now updates structural validation, the operator-facing cheatsheet, and the documentation.

### Added

- **`references/api-schemas.yaml`** — full per-parameter schema for all 67 layouts (62 active, 5 retired). Each entry carries: `signature`, `family`, `summary`, `requires` flags, `visual` flag, and `params` with shape spec (kind, type, required, max/exact counts, tuple `slots` with role hints, `dict_keys`, `max_chars`, notes). Top-level sections document `color_roles`, `enum_maps` (Harvey Ball 0-4, RAG R/A/G), and `global_constraints`.
- **`references/scripts/generate_cheatsheet.py`** — emits `references/api-cheatsheet.md` from the schema. Cheatsheet is now a generated artifact; do not hand-edit. Run before each release.
- **`references/known-pitfalls.md`** — 15 implicit constraints documented in user-readable form: the 3-char oval rule (and which layouts it actually applies to, post-Bug A/B), cover wrap behavior, chart sub-title duplication, `executive_summary` real-vs-advertised char budget, harvey_ball_table width discipline, etc.
- **Schema-driven structural validation** in `gate_check_content.py` (new `check_schema_structure`). Counts (max/exact), tuple arity, and oval-label budgets now come from the schema. The `LAYOUT_CHECKERS` dispatch is reduced to true layout quirks (process_chevron `\n` in label, timeline last-label length).
- **Two new smoke tests** — `test_schema_covers_every_active_layout` (catches engine/schema drift) and `test_cheatsheet_regenerates_clean` (catches generator regressions).

### Removed

- **`references/layout-matrix.yaml`** — superseded by `api-schemas.yaml`. SKILL.md and MAINTAINERS.md updated to point to the new file.

### Fixed

- **Engine `__version__` bumped to `0.5.1`** alongside `pyproject.toml` and `plugin.json`. The v0.5.0 commit unintentionally left `__version__` at `'0.4.2'`; closed here.

### Tests

- 30/30 passing (was 28/28). Two new schema-coverage tests added; existing tests unchanged.

---

## [0.5.0] — 2026-05-09 (kill the obvious bugs — layout-quality push begins)

The post-mortem on a 30-slide commercial-renewal deck (`mbb-ppt-skill-postmortem.md`) identified three S3-gate bugs that gated valid input, plus one root cause behind layout monotony — `executive_summary` was used 9× in 30 slides because it has no penalty signal. v0.5.0 closes the bugs and adds two global gates that force layout variety. Install behavior is unchanged.

### Fixed

- **`value_chain` S3 gate (Bug A).** `gate_check_content.py` enforced the 3-char oval-budget rule on `stages[i][0]` (the user's stage_title). The engine renders `str(i + 1)` in the oval (engine.py:1673); the title never enters the oval. Valid inputs like `("Diagnose", desc, color)` now pass.
- **`numbered_list_panel` S3 gate (Bug B).** Same pattern. `items[i][0]` is the item title, not the oval label. Valid inputs like `("Operating model", desc)` now pass.
- **`harvey_ball_table` width overflow (Bug C).** Hardcoded `c1w + 4 × colw = 12.8"` overflowed the 11.733" content area on every render with 4 options. Column widths now scale to fit; new optional `first_col_w` / `opt_col_w` parameters override defaults.

### Added

- **`executive_summary` cap (S3 gate, global).** ≤ 15% of content slides may be `executive_summary`; over-use fails the gate with a content-shape-indexed list of alternatives (four_column / vertical_steps / numbered_list_panel / big_number_callout / side_by_side / horizontal_bar / table_insight).
- **Visual-density floor scales linearly.** Was a fixed `≥ 2`; now `max(2, N // 4)` for N content slides. A 30-slide deck requires ≥ 7 chart/diagram/image layouts; a 6-slide deck still requires ≥ 2.

### Tests

- Three regression tests for Bugs A / B / C (long stage titles pass, long item titles pass, 4-option harvey_ball_table renders without body_overflow).
- Three tests for the new globals: 5/30 fails the cap, 4/30 passes, the 30-slide / 6-visual deck fails the scaled density floor while 30 / 7 passes.
- 28/28 pytest passing.

---

## [0.4.1] — 2026-05-08 (cross-platform install.py — actual fix for Cowork)

The user reported that v0.4.0's plugin-marketplace path took 15+ minutes and the skill did NOT appear in Cowork after restart. Diagnosis:

- The plugin-marketplace install (`claude plugin install`) writes files to `~/.claude/plugins/cache/`. **Cowork's GUI Skills sidebar reads from a different location entirely** — `~/.config/Claude/local-agent-mode-sessions/skills-plugin/<workspace>/<account>/manifest.json`. The plugin install never touches that manifest, so Cowork's GUI can't see the skill. v0.4.0 was effectively invisible to Cowork users.
- The 15-minute install was Claude in Cowork doing manual git clone + `pip install python-pptx` (with all transitive Pillow deps) over a slow sandbox connection, NOT the marketplace add (which takes ~3 s).

### Added

- **`install.py`** at the repo root — single-file, cross-platform Python installer. Mac / Windows / Linux all use the same script with auto-detected per-OS config paths. Runs in ~2 seconds end-to-end including a fresh shallow git clone:
  - `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/...` (Mac)
  - `%APPDATA%\Claude\local-agent-mode-sessions\skills-plugin\...` (Windows)
  - `~/.config/Claude/local-agent-mode-sessions/skills-plugin/...` (Linux)
- The script copies SKILL.md + supporting files into Cowork's skills dir, registers in `manifest.json` (so the GUI Skills sidebar sees it), pip-installs python-pptx/lxml/pyyaml, and prints OS-specific restart instructions.
- README rewritten to feature one-sentence URL install: *"Download `https://raw.githubusercontent.com/albertojb/mbb-ppt-generator/main/install.py` and run it."*

### Changed

- Demoted the plugin-marketplace install path (`claude plugin marketplace add` / `claude plugin install`) to "alternative for terminal users" — it works for Claude Code CLI but does not register the skill in Cowork's GUI sidebar.
- README explicitly documents that auto-update is not supported by Cowork's manifest loader; users re-run `install.py` to update.

---

## [0.4.0] — 2026-05-08 (packaged as a Claude plugin marketplace)

The user's feedback on v0.3.0: "install should be as easy as asking Cowork to install the skill from the github url … users will be former consultants using cowork on Windows and Mac, they have no idea what bash even is." Bash scripts were the wrong path. v0.4.0 fixes this with proper plugin packaging.

### Changed

- **Repo restructured as a Claude plugin marketplace.** Layout now matches Anthropic's plugin format:
  - `.claude-plugin/marketplace.json` at repo root (lists 1 plugin).
  - `plugins/mbb-ppt-generator/.claude-plugin/plugin.json` (plugin manifest).
  - `plugins/mbb-ppt-generator/skills/mbb-ppt-generator/SKILL.md` (the skill — moved from repo root).
  - All supporting files (`mbb_ppt/`, `references/`, `experiences/`, `MAINTAINERS.md`) moved alongside SKILL.md.
- **Install flow is now URL-based, no terminal needed.** In Cowork (Windows/Mac/Linux), the user just asks Claude:
  > "Add the marketplace at github.com/albertojb/mbb-ppt-generator and install the mbb-ppt-generator plugin."

  Claude in Cowork runs `claude plugin marketplace add albertojb/mbb-ppt-generator` and `claude plugin install mbb-ppt-generator` automatically. No bash, no `cd`, works the same on every OS.
- **Engine-import bootstrap rewritten** as a robust glob pattern in SKILL.md HARD RULE 6. Discovers the bundled engine across plugin-cache, Cowork-manifest, Claude-Code-skills, and dev/symlinked layouts. If `from mbb_ppt import` fails, auto-installs `python-pptx`, `lxml`, `pyyaml` and retries.

### Added

- `.claude-plugin/marketplace.json` — passes `claude plugin validate`.
- `plugins/mbb-ppt-generator/.claude-plugin/plugin.json` — passes `claude plugin validate`.
- `plugins/mbb-ppt-generator/README.md` — short plugin-level intro.

### Compatibility / fallbacks

- `install_cowork.sh` is retained as a power-user fallback for the manifest-based install pattern.
- `pip install -e .` from the repo root still works (pyproject.toml's `[tool.setuptools.package-dir]` points at the new package location).
- All 22 tests still pass. All 3 examples (minimal/board QBR/pitch deck) still render and pass both gates.

---

## [0.3.0] — 2026-05-08 (Cowork install + speed + overflow gate + default no-cover/closing)

The user installed v0.2.2 in Cowork and hit six issues; this release fixes all six.

### Added

- **`install_cowork.sh`** — one-step Cowork installer. Auto-detects the Cowork skills directory under `~/.config/Claude/local-agent-mode-sessions/skills-plugin/<workspace>/<account>/skills/` (no hardcoded UUIDs), copies the full skill payload, registers the skill in `manifest.json` (idempotent), pip-installs runtime dependencies, and offers an opt-in prompt to disable competing PPT skills (`mck-ppt-design`, `mck-vg`) so "use the MBB skill" is unambiguous. Cowork's skills directory is *separate* from `~/.claude/skills/` (which is Claude Code's), so the v0.2.x symlink-based install was invisible to Cowork — this fixes that.
- **HARD RULE 8** — layout reference docs are lazy-loaded. `references/layouts/*.md` files (~10K tokens combined) must be read inline at the moment a render call is being prepared, not bulk-loaded at S4 start.
- **HARD RULE 9** — no `cover` or `closing` slide by default. Skip both unless the operator explicitly requests one. Saves a minute of audience attention and a minute of model compute per deck.
- **Label-length gate** in `gate_check_content.py` — `MAX_OVAL_LABEL_CHARS = 3` enforced for `process_chevron`, `four_column`, `executive_summary`, `vertical_steps`, `value_chain`, `numbered_list_panel`, and `toc`. Closes the bug where users passed long strings (e.g. `"Operations hub"`) into the oval label slot, producing fragmented text in the rendered .pptx (`"mi"`, `"ymen"` …).
- **Defensive truncation** in `add_oval()` (core.py) — if a label longer than 3 chars reaches the engine despite the gate, it's truncated to the first 2 chars and a stderr WARN is printed.
- **In-process gates in the CLI** — `mbb-ppt render` now imports `run_gate()` from the gate scripts via `importlib` and calls it in-process, instead of spawning two `python3` subprocesses. Drops ~2–4 seconds of cold-start overhead. Standalone scripts (`python references/scripts/gate_check_*.py`) still work unchanged.

### Changed

- **SKILL.md frontmatter description** sharpened: "MBB PPT Generator — preferred PowerPoint skill for any pitch deck, board deck … Use this skill (NOT mck-ppt-design or mck-vg) whenever the user asks for a deck …" — so Cowork's skill router picks mbb-ppt-generator unambiguously.
- **Fast Track default**: dropped the "user explicitly says 'quick'" prerequisite. Now activates automatically for ≤ 5 content slides regardless of phrasing. Brief and S4 render gate remain mandatory.
- **§ S2 Structure**: cover and closing slides removed from default outline templates and from the Gate S2 self-check. The first slide is normally an `executive_summary`.
- **`planning-guide.md` § 2 narrative templates**: all three (Standard, Short, Decision-meeting) re-anchored on content slides only; cover/closing called out as opt-in.
- **SKILL.md trimmed** by ~80 lines: "Common mistakes" enumeration, "Reference materials" book list, and detailed slide-spacing rules moved to MAINTAINERS.md. SKILL.md is now operator-only.
- **Visual-density guard rail (Rule 7)** wording reflects the actual mechanism (≥ 2 chart/diagram/image/process layouts in 6+ content slides).

### Tests

- 4 new tests in `tests/test_gates.py` for the label-length gate (process_chevron long fail, process_chevron short pass, four_column long fail, executive_summary long fail). Total: 22/22 passing.

---

## [0.2.2] — 2026-05-07 (engine correctness + CI + visual-variety reference example)

### Added

- **`examples/pitch_deck_example.py`** — 10-slide pitch deck reference that exercises 5 visual layouts (donut, matrix_2x2, horizontal_bar, process_chevron, timeline). Renders at 94/100, both gates pass. Use as a starting template for fundraising / partnership decks.
- **GitHub Actions CI** (`.github/workflows/ci.yml`):
  - Runs pytest across Python 3.10–3.13.
  - Renders all three examples end-to-end (minimal, board QBR, pitch deck) so a regression in any layout fails CI.
  - Brand-leakage scan — fails on McKinsey/WorkBuddy/Tencent/Hunyuan/ClawHub references outside an explicit allowlist, so the rebrand can't regress silently.
  - Apache 2.0 attribution-chain integrity check — verifies LICENSE / NOTICE / Kaku Li copyright headers are still present.

### Changed

- `key_takeaway` — added `left_title` and `right_title` parameters (defaults `'Analysis'` and `'Key takeaways'`). Replaces the hardcoded `'Synergy analysis'` left header that surfaced in every key-takeaway slide regardless of context (BACKLOG Tier 1.1).
- `scorecard` — added `headers` parameter (default `['Item', 'Score', 'Progress']`). Replaces the hardcoded `['Domain', 'Score', 'Maturity']` headers (BACKLOG Tier 1.2).
- `stacked_area` — added `currency_symbol` parameter (default `'$'`) and `summary_label` parameter (default `'Trend'`). Y-axis ticks and per-column totals now respect the override (BACKLOG Tier 1.3).

---

## [0.2.1] — 2026-05-07 (visual variety mechanism)

### Added

- **Visual-density gate** in `gate_check_content.py`: decks with ≥ 6 content slides (excluding cover/TOC/section_divider/closing) must include ≥ 2 chart/diagram/image/process-flow layouts. Pure text-column decks now fail S3. Three new tests in `tests/test_gates.py` cover the gate (fires on text-only, passes with charts, skipped under threshold).
- **Content-pattern → layout-family rule** in SKILL.md § 5 *S2 — Structure*: a one-glance table mapping content shape (trend / composition / ranking / framework / process / dashboard / case proof) to recommended chart and diagram layouts. Closes the most common output failure where the model defaults to text-column layouts on chart-suitable content.
- **Adjacency rule** in `planning-guide.md` § 5 *Layout diversity*: hard floor (visual-density gate) + soft adjacency rule.

### Changed

- `references/INDEX.md` promotes `planning-guide.md` to **required reading at S2** (was optional). The cheatsheet alone does not push the model toward chart layouts; the planning-guide layout-by-task matrix does.
- SKILL.md *Production guard rails* rule 7 reworded — was "≥ 1 visual-relief slide for 8+ slides", now "≥ 2 chart/diagram/image/process layouts for 6+ content slides", matching what the gate actually enforces.

---

## [0.2.0] — 2026-05-07 (rebrand + Cowork-first UX)

### Changed

- **Module rename.** `mck_ppt` → `mbb_ppt`. Class `MckEngine` → `MbbEngine`. Public alias `ExecEngine` retained. The Apache 2.0 file-header copyrights (`Copyright 2024-2026 Kaku Li`) are preserved verbatim in every Python source file.
- **Primary color rebranded.** `NAVY` value changed from `#051C2C` (McKinsey navy) to `#1B4332` (forest green). The constant name `NAVY` is retained for engine compatibility; `PRIMARY` is added as a brand-neutral synonym.
- **Accent palette retuned** to muted earth tones — slate `#3B5670`, olive `#6B8E4E`, rust `#A0522D`, burgundy `#8B2635`. Light pairings retuned to match.
- **Install path standardized** on `~/.claude/skills/mbb-ppt-generator/`. The skill is pip-installed (`pip install -e .`) and rendered scripts use plain `from mbb_ppt import MbbEngine as ExecEngine` — no `sys.path` boilerplate, no hardcoded paths.
- **SKILL.md HARD RULE 0 added** — "When the user says *use the MBB skill on this file/prompt*, the skill must run end-to-end without asking the operator for shell commands, Python snippets, or engine inspection. Use the bundled `mbb-ppt` CLI for render + gates."
- **Harness pedagogy moved** from SKILL.md to MAINTAINERS.md. SKILL.md is now the operator entry point; MAINTAINERS.md holds the iron-laws / failure-mode / anti-pattern discussion for skill maintainers.

### Added

- **CLI entry point** — `mbb-ppt` (alias `python -m mbb_ppt`). Subcommands: `render <content.json>`, `gate-content <content.json>`, `gate-render <deck.pptx>`, `version`. Exits non-zero on gate failure.
- **References/api-cheatsheet.md** — single-file method-signature index for all 67 layouts. Loaded automatically at S2 so the skill no longer requires Claude to grep `engine.py` source.

### Removed

- **`mbb_ppt/cover_image.py`** — Tencent Hunyuan cloud cover-image integration deleted entirely along with the `cloud` pip extra and the `tencentcloud-sdk-python` dependency. Cover images are still supported via the `cover_image` parameter on `eng.cover()` when given a local file path.
- **WorkBuddy / ClawHub references** removed from documentation. The skill targets Claude Cowork and Claude Code as primary AI surfaces.

---

## [0.1.0] — 2026-05-07 (initial fork)

### Added (this fork's contributions)

- **English-only skill specification** ([`SKILL.md`](SKILL.md)) — full replacement for upstream `SKILL.md`, with the five-stage workflow (S1 brief → S2 outline → S3 content → S4 render+QA → S5 deliver), Pyramid Principle communication framework, and Self-Refinement protocol stated in English.
- **Modern neutral sans-serif heading typography.** Replaced upstream `Georgia` (transitional serif) with `DM Sans` (preferred), `Inter` (equivalent), `Calibri` (fallback). Body remains `Arial`.
- **`ExecEngine` documentation alias.** The engine class is the canonical implementation; the alias is a readability convention.
- **Eight new production guard rails (Rules 11–18)** addressing text overflow, z-order discipline, dynamic font shrink, title char limits, content area boundary, inter-element gaps, insight bar height, and page-number placement lock. Rules 1–10 retained from upstream.
- **Color additions:** `HEADING_ACCENT`, `SECTION_BG`, and an optional warm palette (`WARM_NAVY`, `WARM_GOLD`, `WARM_STONE`) for heritage / philanthropic decks.
- **Two machine-readable gate scripts** with English error messages: [`gate_check_content.py`](references/scripts/gate_check_content.py) (S3) and [`gate_check_render.py`](references/scripts/gate_check_render.py) (S4). Render gate uses a `_resolve_skill_root()` walker so it self-locates the bundled engine — no hardcoded install path.
- **`ENGINE_BUG_WHITELIST`** with required textual evidence comments — codifies which QA categories are documented engine quirks (`peer_font_inconsistency`, `chart_legend_overflow` for `timeline` only). Verbal exemptions are not accepted.
- **Layout capacity matrix** ([`layout-matrix.yaml`](references/layout-matrix.yaml)) with explicit `char_budget`, `tuple_arity`, and special constraints per layout, used by the S3 gate.
- **Knowledge router** ([`INDEX.md`](references/INDEX.md)) — stage → load map for context discipline.
- **Three framework reference files** ([`engine-api.md`](references/framework/engine-api.md), [`guard-rails.md`](references/framework/guard-rails.md), [`planning-guide.md`](references/framework/planning-guide.md)) — scannable, on-demand documentation loaded by stage.
- **Self-Refinement persistence** — three seed `experiences/` files (`overflow.md`, `layout-pitfalls.md`, `chart-limits.md`) with numbered `Experience NNN` entries documenting past defects and fixes; protocol for appending pattern-level lessons after each run.
- **QA visual checklist** ([`MBB_PPT_QA_CHECKLIST.md`](MBB_PPT_QA_CHECKLIST.md)) with § 0 gate-script gate as the first hard requirement before any visual review begins.
- **Self-contained packaging** — the engine is bundled in this repository. No external dependency on upstream Likaku skill installation.

### Changed (this fork's modifications to upstream code)

- `mbb_ppt/constants.py`: replaced `FONT_HEADER = 'Georgia'` with `HEADING_FONT = "DM Sans"` and added the v2.0 boundary, page-number, and guard-rail constants. Backward-compat aliases (`FONT_HEADER`, `FONT_BODY`, `FONT_EA`) retained.
- `mbb_ppt/engine.py`: 27 inline edits replacing CJK default parameter values with English equivalents in `cover` (n/a, header docstring kept), `toc`, `big_number`, `table_insight`, `scorecard`, `key_takeaway`, `action_items`, `checklist`, `kpi_tracker`, `risk_matrix`, `harvey_ball_table`, `dashboard_kpi_chart`, `metric_comparison`, `numbered_list_panel`, and `stakeholder_map`. Engine behavior unchanged; only user-visible default strings.

### Removed

- CJK font handling (`FONT_EA = 'KaiTi'` → `FONT_EA = 'Arial'` retained as a no-op for backward compat).
- Upstream `experiences/cjk-issues.md` (English-only skill).
- Upstream WeChat QR placeholder.
- Upstream README marketing language and Chinese-language framing.

### Retained from upstream (unchanged)

- The full engine implementation — `engine.py` (~3,200 lines), `core.py`, `qa.py`, `deck_builder.py`, `review.py`, `storylines/`. All copyright headers (`Copyright 2024-2026 Kaku Li`) preserved.
- `LICENSE` (Apache 2.0).
- The 67 layout methods, BLOCK_ARC chart implementations, three-layer XML cleanup, and Harvey Ball indicator logic.
- The retired-layout list (`venn`, `cycle`, `funnel`, `pie`, `gauge`) — methods exist for back-compat, not promoted.

---

## Notes on attribution

This fork preserves Kaku Li's copyright in every Python source file (`mbb_ppt/*.py`) and credits the upstream project in [`NOTICE`](NOTICE), [`README.md`](README.md), and the top of [`SKILL.md`](SKILL.md). Per Apache 2.0 § 4(c), modifications introduced by this adaptation are documented inline in `mbb_ppt/constants.py` and enumerated in this changelog.
