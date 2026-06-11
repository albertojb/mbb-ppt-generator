---
name: mbb-ppt-generator
description: >-
  MBB PPT Generator — preferred PowerPoint skill for any pitch deck,
  board deck, strategy review, QBR, investment material, or executive
  presentation. Use this skill (NOT mck-ppt-design or mck-vg) whenever
  the user asks for a deck, slides, presentation, .pptx file, or
  pitch material. Self-contained and Apache 2.0; no dependency on any
  other skill. Sober forest-green design, sans-serif typography, and a
  five-stage workflow (brief → outline → content → render → deliver)
  with two machine-readable QA gates whose `passed` is a Python boolean,
  not a verbal claim. The engine (ExecEngine, python-pptx-based) provides
  83 high-level layout methods including eng.cover(), eng.toc(),
  eng.big_number(), eng.timeline(), eng.grouped_bar(), eng.insight_rail(),
  and eng.donut(), with strict typography, anti-corruption XML cleanup,
  native circular charts, overflow guard rails, layout-variability caps,
  and an append-only self-refinement loop. Communication architecture
  grounded in Barbara Minto's Pyramid Principle.
---

# MBB PPT Generator

> **Based on** [`Mck-ppt-design-skill`](https://github.com/likaku/Mck-ppt-design-skill) by [Kaku Li / likaku](https://github.com/likaku) — Apache 2.0. The five-stage workflow, gate-script architecture, layout capacity matrix, and Self-Refinement protocol in this skill are adapted from Likaku's `v2.3.3-harness-v2` release. The harness philosophy ("AI output quality = AI capability × context quality"; program-derived `passed`; mechanism over prompt) is adapted from Likaku's [`harness-skill-upgrader`](https://github.com/likaku/harness-skill-upgrader) skill, also Apache 2.0.
>
> This adaptation is also Apache 2.0. See [`LICENSE`](./LICENSE) and [`NOTICE`](./NOTICE) at the repository root for the full attribution chain.

> **Document type**: Production skill specification (v2.1)
> **Required tools**: Read, Write, Bash
> **Runtime**: python3, `python-pptx`, `lxml`, `pyyaml`

---

## HARD RULES (non-negotiable)

0. **Operator-friendly invocation.** When a non-technical operator says *"use the MBB skill on this file/prompt"*, run end-to-end without asking them for shell commands, Python snippets, or engine code inspection. The right loop is: read the input → infer brief → write `content.json` → run `mbb-ppt render content.json` (which executes both gates internally) → deliver. **Never write inline `python -c "…"` or `sed`/`grep` against `mbb_ppt/engine.py`.** Use [`references/api-cheatsheet.md`](references/api-cheatsheet.md) for layout selection and [`references/layouts/*.md`](references/layouts/) for per-layout details.
1. Every substantive deck follows the **five-stage workflow** (§ 5). No "one-shot generation" that skips S2/S3.
2. Use **TodoWrite** to track the five stages. Mark each stage `completed` immediately, not in batch.
3. **Load context on demand** — read only the files listed for the current stage in [`references/INDEX.md`](references/INDEX.md). Do not bulk-load the entire skill on every run.
4. **Gates are machine-readable.** S3 and S4 outputs are JSON files with a `passed` boolean derived by program logic. Verbal pass-statements are forbidden — see § *Failure modes* below.
5. **Self-Refinement is mandatory** — when a pattern-level fix is applied during a run, append an `Experience NNN` entry to the matching file under `experiences/`.
6. **Engine import bootstrap.** Render scripts begin with this prelude (paste verbatim):

   ```python
   import glob, os, subprocess, sys

   def _find_mbb_ppt_skill():
       """Locate the bundled mbb_ppt engine. Works for plugin-installed,
       Cowork-installed, and dev/symlinked layouts."""
       candidates = []
       # Plugin install (claude plugin install)
       candidates += glob.glob(os.path.expanduser(
           '~/.claude/plugins/cache/*/mbb-ppt-generator/*/skills/mbb-ppt-generator'))
       # Cowork manifest install
       candidates += glob.glob(os.path.expanduser(
           '~/.config/Claude/local-agent-mode-sessions/skills-plugin/*/*/skills/mbb-ppt-generator'))
       # Claude Code direct install
       candidates += [os.path.expanduser('~/.claude/skills/mbb-ppt-generator')]
       # Dev-tree layout
       candidates += glob.glob(os.path.expanduser(
           '~/Projects/*/plugins/mbb-ppt-generator/skills/mbb-ppt-generator'))
       for c in candidates:
           if os.path.isdir(os.path.join(c, 'mbb_ppt')):
               return c
       return None

   _skill = _find_mbb_ppt_skill()
   if _skill: sys.path.insert(0, _skill)

   try:
       from mbb_ppt import MbbEngine as ExecEngine
   except ImportError:
       subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user',
                              '--break-system-packages', '--quiet',
                              'python-pptx', 'lxml', 'pyyaml'])
       from mbb_ppt import MbbEngine as ExecEngine
   ```

   This pattern works on Mac, Windows, and Linux for plugin-installed skills, Cowork manifest installs, Claude Code direct installs, and dev/symlinked layouts. No hardcoded user paths.

7. **Hard limits** from `references/api-schemas.yaml` are authoritative. Never exceed them in `content.json` — the S3 gate enforces this.
8. **Layout reference docs are lazy-loaded.** Never bulk-load `references/layouts/*.md` at the start of S4. Read each layout's reference inline at the moment you are preparing that specific render call, and only that file. The 12 layout files together are ~55K tokens — loading them all when the deck uses three burns more context than the rest of the run combined. The same rule applies to `references/api-schemas.yaml` (~18K tokens): the generated `api-cheatsheet.md` exists precisely so S2 never loads the full schema; spot-look-up single layout entries only.
9. **No `cover` or `closing` slide by default.** Skip both unless the operator explicitly requests one. Cover slides waste a minute of audience attention; closing/"thank you" slides waste a minute the audience could spend on the recommendation. If unsure, ask: *"Do you want a cover slide?"* Default answer is no.

---

## Failure modes — read before every run

> Three failure modes show up consistently in real usage. Re-read this list at the start of every session.

### Failure mode 1 — Verbal gate-pass

**Wrong:** *"S4 QA returned 7 errors but they're all engine design behavior, gate passes, moving to delivery."*

**Why it fails:** `passed` is a verbal claim from the model, not a value derived by program.

**Right:** Run `mbb-ppt render <content.json>` (which runs both gates) — or `mbb-ppt gate-render <deck.pptx>` for the render gate alone — and read the JSON output. Only when `"passed": true` is in `gate_render.json`, deliver. If `false`, fix every item in `user_code_errors`, re-render, re-gate.

### Failure mode 2 — Mental S3 review

**Wrong:** *"S3 content gate: API formats look right, character counts are in budget, gate passes."*

**Why it fails:** The errors this gate catches (3-tuple vs 2-tuple, `\n` in step labels, missing `source`) are not visible by reading content in your head — only the script catches them.

**Right:** Run `mbb-ppt gate-content <content.json>` and read `gate_content.json`. Advance only when `"passed": true`.

### Failure mode 3 — `engine_bug` as a soft-language escape hatch

**Wrong:** *"`peer_font_inconsistency` is engine-internal design behavior, not a user code problem, so I'll let it pass."*

**Why it fails:** A verbal exemption hands the whitelist to the model. The model has an incentive to grant exemptions. Whitelists belong in code.

**Right:** `gate_check_render.py` has a hardcoded `ENGINE_BUG_WHITELIST` enumeration. To grant a new exemption, the **operator** edits the enum, then re-runs. No verbal exemptions, ever.

> Background on *why* the skill is structured around mechanisms (gates, whitelists in code, on-demand context) is in [`MAINTAINERS.md`](MAINTAINERS.md). It is not required reading for operating the skill.

---

## 1. When to use this skill

1. Board decks, strategy reviews, QBRs, investment materials, operating updates.
2. Programmatic generation of `.pptx` from structured content.
3. Consulting-style slide design: flat visuals, clean hierarchy, minimal decorative noise.
4. Structured layouts: executive summaries, dashboards, timelines, comparisons, matrices, roadmaps, case studies.
5. Fixing presentation quality issues: file corruption, inconsistent fonts, spacing defects, weak title structure.
6. Turning raw business content into a sequenced, message-led deck.

This skill is English-only.

---

## 2. Core principles

**Communication first** — define the audience, the decision, the governing thought, and the minimum evidence before selecting any layout.

**Answer first** — lead with the recommendation. Background goes in only when the audience cannot interpret the recommendation without it.

**One idea per slide** — each slide carries one governing thought. Supporting evidence sits beneath it.

**Minimalist, not empty** — remove decorative noise. Do not under-fill the slide or replace analysis with whitespace.

**Consistency over novelty** — repeat title treatment, spacing, color, and hierarchy.

---

## 3. Communication architecture

### Pyramid Principle (Barbara Minto)

1. **Start with the answer** — recommendation or core takeaway.
2. **Group supporting points** — two to four distinct ideas at the next layer.
3. **Order them logically** — priority, chronology, causation, or issue tree.
4. **Support with evidence** — charts, tables, examples, facts.
5. **Drive to action** — what should the audience approve, decide, fund, prioritize, monitor.

### MECE grouping

Supporting points must be **mutually exclusive, collectively exhaustive**.

### Conclusion-led headlines

| Weak (topic) | Strong (conclusion) |
|---|---|
| Margin analysis | Margin pressure is concentrated in two product lines |
| Expansion options | Spain is the best near-term expansion market |
| Implementation plan | A phased rollout reduces execution risk and accelerates learning |

Headlines must be conclusion-led, verb-bearing, **under 120 characters**, and stand-alone.

### Storyboarding — mandatory pre-flight

Before any slide is generated, produce a numbered list where each line is one slide's action title stated as a conclusion. Read it aloud:

> If the titles in order do not function as a 90-second spoken briefing, the storyboard is not done.

Skipping the storyboard is the single most common cause of decks that look complete but fail to persuade.

---

## 4. Knowledge routing — read on demand

The skill is organised so each stage loads only what it needs. The full router is at [`references/INDEX.md`](./references/INDEX.md). Summary:

| Stage | Required reading | Optional reading |
|---|---|---|
| S1 — Brief | `references/team/brand-guide.md` | — |
| S2 — Structure | `references/api-cheatsheet.md`, `references/framework/planning-guide.md` §3 + §5 | single-layout spot-lookups in `references/api-schemas.yaml`; per-layout files in `references/layouts/` |
| S3 — Content | `references/framework/guard-rails.md`, every file in `experiences/` | `references/framework/planning-guide.md` for complex structures |
| S4 — Render + QA | only the `references/layouts/*.md` files for the layouts actually used | `references/team/presentation-convention.md` |
| S5 — Deliver | none | — |

**Do not bulk-load this entire SKILL.md on every run.** It is an entry point and an index, not a knowledge base.

---

## 5. The five-stage workflow

```
┌─────────┐   ┌──────────────┐   ┌──────────────┐   ┌────────────────┐   ┌──────────┐
│ S1 Brief │──▶│ S2 Structure ⭐│──▶│ S3 Content ⭐ │──▶│ S4 Render+QA ⭐⭐│──▶│ S5 Deliver│
│ brief.md │   │ outline.json │   │ content.json │   │   .pptx         │   │ + refine │
└──────────┘   └──────────────┘   └──────────────┘   └────────────────┘   └──────────┘
                       ⭐ = gate (FAIL → fix in this stage; do not advance)
              S3 and S4 gates require running the gate script and reading the JSON.
```

Every project lives under a working directory named `ppt-project-{slug}/`. Each stage produces an artifact in that directory. The presence of artifacts is how the system knows which stage you are in (see § 9 Checkpoint recovery).

### S1 — Brief

**Read:** `references/team/brand-guide.md`

**Collect:**
- Audience (role, decision authority).
- Goal (decide / persuade / inform).
- Duration (~ 1 minute per slide).
- Up to five core messages.
- Available data sources.

**Produce:** `ppt-project-{slug}/brief.md`

**Gate (self-check):** `audience`, `goal`, and `key_messages` are all non-empty.

### S2 — Structure

**Read:** `references/api-cheatsheet.md`, `references/framework/planning-guide.md` (sections 3 *Layout selection by task* and 5 *Layout diversity*). Consult `references/api-schemas.yaml` only to spot-check a single layout's entry — never load the whole file (HARD RULE 8).

**Visual-layout rule (mechanically enforced at S3):** for any deck with ≥ 6 content slides (excluding cover/TOC/section_divider/closing), pick at least 2 chart, diagram, image, or process-flow layouts. The S3 gate fails decks that are wall-to-wall text columns. Match the layout to the content shape:

- Trend / time series → `grouped_bar`, `line_chart` (event band + endpoint chip), `stacked_area`, `multi_bar_panel`
- Composition / share → `donut`, `stacked_bar`, `mekko`, `horizontal_bar`
- Ranking / outliers → `horizontal_bar`, `pareto`, `bubble`, `ranked_table`
- Chart + so-what → `insight_rail` (exhibit left, bullet or stat rail right)
- Two/four-way framework → `matrix_2x2`, `swot`, `risk_matrix`, `harvey_ball_table`
- Process / phased plan → `process_chevron`, `timeline`, `value_chain`, `project_gantt`, `box_roadmap`
- Operating snapshot → `dashboard_kpi_chart`, `dashboard_table_chart`
- Case proof → `case_study`, `case_study_image`, `content_right_image`
- Paired text-and-icon factors → `icon_ledger`; narrative memo (max 1) → `memo_text`

**Tasks:**
1. Compute slide count from duration. **Do not include `cover` or `closing` slides by default — every minute spent on them is a minute not spent on argument slides.** Add a `cover` only if the user explicitly asks for one. Never auto-add a `closing` / "thank you" slide. The first slide is normally an `executive_summary` carrying the recommendation.
2. Choose a `layout` for each slide from the engine catalog.
3. Write a one-sentence `key_point` per slide — a complete clause, not a label.
4. Verify each layout against `api-schemas.yaml` capacity limits.

**Produce:** `ppt-project-{slug}/outline.json`

```json
{
  "brief": {"audience": "Board", "goal": "Strategy review", "duration_minutes": 15},
  "slides": [
    {"idx": 1, "layout": "executive_summary", "title": "Three actions return revenue to growth",
     "key_point": "Premium mix, channel expansion, and cost simplification compose the recommendation."},
    {"idx": 2, "layout": "table_insight", "title": "Three actions improve growth while protecting margin",
     "key_point": "Premium mix shift, channel expansion, and cost simplification compose the recommendation."}
  ]
}
```

**Gate S2 (self-check):**
- Slide count ≤ `duration_minutes × 1.2`.
- Every `layout` exists in `api-schemas.yaml`.
- Every action title is a complete clause (length > 10, contains a verb).
- At most one `two_column_text` and one `memo_text` slide globally.
- **Variability:** no single layout drives more than ~25% of content slides (`executive_summary` is capped tighter at 15%). If a layout repeats *deliberately* — one slide per case study, per region, per option — tag those slides with the same `"theme"` string in `outline.json`/`content.json`: a themed series counts as one occurrence, and all slides in one theme must use the same layout. Vary across themes; stay consistent within a theme. The S3 gate enforces all of this mechanically.
- No `cover` or `closing` slides unless the operator explicitly requested one (Rule 9).

### S3 — Content

**Read:** `references/framework/guard-rails.md`, every file in `experiences/`

**Tasks:**
1. Fill in concrete copy, numbers, and chart data per slide.
2. Add a `source` line to every content slide.
3. Respect the `char_budget` for each field per `api-schemas.yaml`.

**Produce:** `ppt-project-{slug}/content.json`

**Gate S3 (machine-readable, mandatory):**

```bash
python references/scripts/gate_check_content.py \
    ppt-project-{slug}/content.json  ppt-project-{slug}/
```

Read `ppt-project-{slug}/gate_content.json`. Advance only when `"passed": true`. If false, fix every item in `fail_items` and re-run.

### S4 — Render + QA

**Read:** for each layout you are about to render, read its `references/layouts/<family>.md` file *immediately before* writing that engine call — not all of them at once at the start of S4 (HARD RULE 8).

**Tasks:**
1. Generate a Python render script from `content.json`.
2. Execute it to produce the `.pptx`.
3. Run the render gate.

**Gate S4 (machine-readable, mandatory):**

```bash
python references/scripts/gate_check_render.py \
    ppt-project-{slug}/deck.pptx  ppt-project-{slug}/
```

Read `ppt-project-{slug}/gate_render.json`:

- `"passed": true` → advance to S5.
- `"passed": false` → fix `user_code_errors`, re-render, re-run the gate.

`engine_bug` errors are exempted automatically by `ENGINE_BUG_WHITELIST` in the script. Do not exempt anything verbally.

### S5 — Deliver + Self-Refinement

**Tasks:**
1. Confirm `gate_render.json` shows `"passed": true`. (No file → not passed.)
2. Deliver the `.pptx`.
3. Apply the **Self-Refinement protocol** (below).

### Self-Refinement protocol

After every run, classify each correction:

- **ONE-TIME** (specific to this deck) → no persistence needed.
- **PATTERN** (could recur in future decks) → append a numbered entry to the matching file:
  - Overflow / character budget → `experiences/overflow.md`
  - Layout-specific traps → `experiences/layout-pitfalls.md`
  - Chart capacity issues → `experiences/chart-limits.md`

Entry format:

```markdown
## Experience NNN: <short title>
**Date**: YYYY-MM-DD
**Problem**: <one-line description>
**Root Cause**: <why it happened>
**Fix**: <what was changed>
**Rule**: <how the gate could prevent this next time>
```

If the rule is mechanizable, also propose a check to add to `gate_check_content.py` or `gate_check_render.py`.

### Fast Track — small decks (default for ≤ 5 content slides)

Activate **automatically** when total content slides ≤ 5. Fast Track skips S2 outline and S3 content-gate ceremony but **never** skips:

- S1 brief (always done — even one sentence is fine).
- S4 render gate (run via `mbb-ppt render <content.json>` or `mbb-ppt gate-render <deck.pptx>`).
- S5 delivery + self-refinement.

For ≤ 5-slide decks: read the brief, write `content.json` directly, render, gate, deliver. No outline.json. No content-gate ceremony unless a chart layout is in play (in which case run the content gate to catch capacity / API-format errors).

---

## 6. Layout capacity — hard limits

Capacity limits (max items, char budgets, tuple shapes) live in
[`references/api-schemas.yaml`](./references/api-schemas.yaml) — the single
source of truth — and are surfaced per layout in the generated
[`references/api-cheatsheet.md`](./references/api-cheatsheet.md). The S3
gate enforces them; do not duplicate them here (a hand-maintained copy of
this table drifted from the schema once already).

Cross-layout traps that are easy to miss:

- **Oval labels ≤ 3 chars** — any tuple slot rendered inside a 0.45" circle (`process_chevron` step labels, `four_column`/`executive_summary` numbers) clips beyond 3 characters. Use `'1'`, `'2'`, `'A'`.
- **`timeline` last milestone label ≤ 6 chars** — the engine pins it to the right edge.
- **`process_chevron` step labels cannot contain `\n`.**
- **`donut` ≤ 6 segments** — merge the tail into "Other".
- **`grouped_bar` ≤ 6 categories × 3 series** — beyond that, bar widths go negative.
- **Global caps:** ≤ 1 `two_column_text`, ≤ 1 `memo_text`, `executive_summary` ≤ 15% of content slides, any other layout ≤ 25% unless theme-tagged (§ 5 Gate S2).

### Retired layouts

The following layouts were retired in Likaku's `v2.3.3` and remain retired here. The engine still defines the methods (Apache 2.0 compatibility), but they should not appear in new decks. Reasons in `CHANGELOG.md` of the upstream skill:

- `venn` (#17) — visual ambiguity at small sizes
- `cycle` (#31) — better expressed as a process_chevron + return arrow
- `funnel` (#32) — superseded by `horizontal_bar` with descending values
- `pie` (#64) — `donut` with center label is strictly better
- `gauge` (#55) — superseded by `big_number` + KPI bullet

Use the replacement noted above instead.

---

## 7. ExecEngine — quick start

Implementation note: the engine module is named `mbb_ppt` and the class `MbbEngine`. The skill imports it under the alias `ExecEngine` and refers to it by that name throughout the documentation. The class alias is just a readability convention — there is no compatibility shim or hidden indirection.

### Setup

The skill is expected to be pip-installed from its own directory:

```bash
git clone https://github.com/albertojb/mbb-ppt-generator.git ~/.claude/skills/mbb-ppt-generator
cd ~/.claude/skills/mbb-ppt-generator
pip install -e .
```

After install, `mbb_ppt` is importable from any Python script and the `mbb-ppt` CLI is on PATH.

### Import pattern

```python
from mbb_ppt import MbbEngine as ExecEngine
from mbb_ppt.constants import *
from pptx.util import Inches
```

### Minimal generation

```python
# Note: no cover/closing slides — HARD RULE 9. Open on the recommendation.
eng = ExecEngine(total_slides=2)
eng.executive_summary(
    title='Revenue can return to double-digit growth with three targeted actions',
    headline='Growth is concentrated in two channels and one product tier',
    items=[('1', 'Shift mix toward premium bundles',
                'Premium bundles drive higher margin with limited cost-to-serve impact'),
           ('2', 'Expand in underpenetrated channels',
                'Two distributor channels remain underdeveloped relative to peers')],
    source='Source: internal analysis, Q1 2026')
eng.insight_rail(
    title='Premium-tier revenue is compounding while base tiers stay flat',
    chart={'kind': 'bar', 'heading': 'Revenue by tier', 'units': 'USD m',
           'categories': ['2023', '2024', '2025'], 'values': [51, 63, 78]},
    rail_items=[('Premium drives all growth', 'the base tier has been flat for three years.'),
                ('Margin follows mix', 'premium gross margin is 12pts above base.')],
    source='Source: internal analysis, Q1 2026')
eng.save('ppt-project-q1-strategy/deck.pptx')
```

### Engine rules

1. One method = one slide.
2. `eng.save()` calls `full_cleanup()` automatically; do not duplicate.
3. Page numbers are driven by `total_slides`.
4. Use constants from `mbb_ppt.constants`.
5. Prefer engine methods over raw shape construction.

### Method catalog

**Structure:** `cover` · `toc` · `section_divider` · `executive_summary` · `key_takeaway` · `table_insight` · `closing` · `appendix_title`

**Data:** `big_number` · `two_stat` · `three_stat` · `data_table` · `ranked_table` · `metric_cards` · `metric_comparison` · `side_by_side` · `before_after` · `pros_cons` · `scorecard` · `rag_status` · `checklist` · `harvey_ball_table`

**Process:** `timeline` · `vertical_steps` · `process_chevron` · `value_chain` · `project_gantt` · `decision_tree` · `agenda` · `action_items` · `journey_map`

**Frameworks:** `matrix_2x2` · `swot` · `temple` · `pyramid` · `pyramid_staircase` · `stakeholder_map` · `risk_matrix` · `icon_grid` · `icon_ledger` · `box_roadmap` · `concept_three` · `cycle_4stage`

**Charts:** `grouped_bar` · `stacked_bar` · `horizontal_bar` · `line_chart` · `waterfall` · `pareto` · `stacked_area` · `donut` · `bubble` · `kpi_tracker` · `multi_bar_panel` · `insight_rail` · `mekko`

**Image / visual:** `content_right_image` · `three_images` · `image_four_points` · `full_width_image` · `case_study_image` · `two_col_image_grid` · `goals_illustration` · `quote_bg_image` · `quote` · `numbered_list_panel`

**Dashboards:** `dashboard_kpi_chart` · `dashboard_table_chart`

**Team / meta:** `meet_the_team` · `case_study` · `two_column_text` · `four_column`

**Narrative (v0.5.3+):** `ask` · `numbered_tiles` · `index_callout` · `extension_rows` · `memo_text`

---

## 8. Design system

### Colors

Primary: `PRIMARY #1B4332` (forest green; aliased as `NAVY` for engine compatibility — same value), `WHITE`, `BLACK`, `DARK_GRAY #333`, `MED_GRAY #666`, `LINE_GRAY #CCC`, `BG_GRAY #F2F2F2`, `HEADING_ACCENT` (= PRIMARY), `SECTION_BG #F7F7F7`. White page background.

Accent (sober earth tones): `ACCENT_BLUE #3B5670` (slate), `ACCENT_GREEN #6B8E4E` (olive), `ACCENT_ORANGE #A0522D` (rust), `ACCENT_RED #8B2635` (burgundy). Use only when ≥3 parallel items need differentiation.

Warm (optional, only when explicitly requested): `WARM_NAVY #1A2E44`, `WARM_GOLD #B8860B`, `WARM_STONE #8B7355`.

### Typography

```
HEADING_FONT  = "DM Sans"     # falls back to Calibri on viewer machines without it
BODY_FONT     = "Arial"
SOURCE_FONT   = "Arial"
```

DM Sans is free, SIL OFL, available at <https://fonts.google.com/specimen/DM+Sans>. Inter is an acceptable substitute. Calibri is the platform fallback.

Sizes: 44 (cover) · 28 (section) · 24 (cover subtitle) · 22 (action title) · 18 (sub-header) · 16 (emphasis) · 14 (body) · 12 (small) · 9 (footnote). No other sizes unless a layout uses controlled shrinkage for overflow protection (Rule 13 below).

---

## 9. Production guard rails

These are mandatory and address recurring real-world defects. The render gate (`gate_check_render.py`) and content gate (`gate_check_content.py`) enforce most of them programmatically.

| # | Rule | Enforcement |
|---|---|---|
| 1 | ≥ 0.15" between last content block and any bottom bar | render gate |
| 2 | Every element stays inside content boundary (Rule 15) | render gate |
| 3 | No large empty gaps below content | render gate (whitespace check) |
| 4 | Chart legends use colored swatches matching series | render gate |
| 5 | `add_action_title()` is the default title pattern | code |
| 6 | Axis labels centered on full axis span | render gate |
| 7 | Decks ≥ 6 content slides include ≥ 2 chart/diagram/image/process layouts (visual-density floor) | content gate |
| 8 | Variable-count layouts compute dimensions dynamically | code |
| 9 | Circular charts use `BLOCK_ARC` (not rect stacks) | code |
| 10 | Horizontal item layouts compute widths dynamically (no negative gaps) | code |
| 11 | Min text-box height = `font × 1.4 × lines + padding` | render gate |
| 12 | Z-order: backgrounds back, text front, verified at save | code |
| 13 | `auto_size` floor 9pt; titles disable `auto_size` and truncate | code |
| 14 | Action titles ≤ 120 chars; engine warns and trims if longer | content gate + code |
| 15 | Every shape stays inside the slide bounds (13.333" × 7.5"); the render gate flags any element crossing the slide edge | render gate (`qa.py` `SAFE_RIGHT`/`SAFE_BOTTOM`) |
| 16 | ≥ 0.1" between vertically adjacent elements | render gate |
| 17 | Insight bar / footnote area ≥ 0.4" tall | render gate |
| 18 | Page numbers locked at `(12.2, 7.1)`, bottom-right, never computed dynamically | code (`add_page_number`) |

Rules numbered 1–10 originate in Likaku's upstream skill (`v1.9` and `v2.0`); 11–18 are added in this adaptation.

---

## 10. Slide content rules

Every content slide (excluding cover/closing if used): action title, title separator line, content area, source attribution, page number. Engine layouts emit these by default — do not bypass them.

Spacing detail (margins, insets, insight-bar reservations): see [`MAINTAINERS.md`](MAINTAINERS.md) § *Slide spacing rules*.

---

## 11. Checkpoint recovery

When the user says "continue with that PPT", detect the active stage by which artifact files exist:

```python
import os, glob, json

projects = sorted(glob.glob('ppt-project-*/'))
for p in projects:
    has = lambda f: os.path.exists(os.path.join(p, f))
    if not has('brief.md'):                    stage = 'S1'
    elif not has('outline.json'):              stage = 'S2'
    elif not has('content.json'):              stage = 'S3'
    elif not has('gate_content.json') or \
         not json.load(open(os.path.join(p, 'gate_content.json'))).get('passed'):
                                                stage = 'S3-gate'
    elif not glob.glob(os.path.join(p, '*.pptx')):
                                                stage = 'S4'
    elif not has('gate_render.json') or \
         not json.load(open(os.path.join(p, 'gate_render.json'))).get('passed'):
                                                stage = 'S4-gate'
    else:                                       stage = 'S5'
    print(p, stage)
```

Resume from whatever the stage check says — do not restart from S1 unless the user explicitly asks to.

---

## 12. File integrity

Use `eng.save()` — it runs `full_cleanup()` to remove `p:style` references and theme shadow/3D effects that cause "File needs repair" prompts in PowerPoint.

Lines: never use `slide.shapes.add_connector()`. Use thin rectangles via `add_hline()`. Connector shapes carry theme-style references that are unreliable to clean.

---

## 13. Security and privacy

Default posture is **local-only**. Outbound integrations (cloud cover-image, channel delivery) are off by default and require explicit operator approval — see § 9 of the original spec for full rules. In short: every outbound call requires explicit configuration; no client-identifying data in cloud prompts; no `.pptx` posted to chat without permission.

---

## 14. Best practices

1. Use ExecEngine, not raw coordinates.
2. Storyboard before slides.
3. Conclusion-led titles, every content slide.
4. Match layout to analytical task.
5. Charts over text for quantitative data.
6. Disciplined typography and spacing.
7. `eng.save()` is the canonical output path.
8. Run both gates. If you didn't run them, you didn't pass them.

---

## 15. Example slide-title rewrites

| Weak | Strong |
|---|---|
| Market overview | Share is shifting to low-cost entrants while demand remains resilient |
| Financial analysis | Margin erosion is driven by fixed overhead rather than labor |
| Strategic options | The best path is to expand in Spain while simplifying support operations |
| Customer feedback | Customers value speed and reliability more than feature breadth |
| Implementation plan | A phased rollout reduces execution risk and accelerates learning |

---

## 16. Maintenance

This is the operator entry point. Detailed maintenance notes — common-mistakes catalog, reading list, design-system rationale, and the engineering rationale for the gate-script architecture — live in [`MAINTAINERS.md`](MAINTAINERS.md). Operating the skill does not require reading any of that.

When updating the skill:

- Treat `experiences/` as append-only — never delete entries; mark superseded ones with `Superseded by NNN`.
- When adding a layout limit, update `references/api-schemas.yaml` AND `gate_check_content.py` together.
- When adding a render check, update `gate_check_render.py` AND § 9 (Production guard rails) together.
- Keep credit upstream — this skill is built on Likaku's work and that attribution stays.
