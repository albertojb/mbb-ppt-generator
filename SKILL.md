---
name: mbb-ppt-generator
description: >-
  MBB PPT Generator — create professional, executive-grade PowerPoint
  presentations from scratch using ExecEngine, a python-pptx-based
  presentation engine with MBB-style communication and design discipline.
  Use this skill for board decks, strategy reviews, quarterly business
  reviews, investment materials, operating updates, and other senior
  audiences. The engine provides high-level methods such as eng.cover(),
  eng.toc(), eng.big_number(), eng.timeline(), eng.grouped_bar(),
  eng.table_insight(), and eng.donut(), with strict typography, anti-
  corruption XML cleanup, native circular charts, spacing and overflow
  guard rails, machine-readable content and render gates, and a
  self-refinement loop that persists pattern-level fixes between runs.
  Communication architecture is grounded in Barbara Minto's Pyramid
  Principle.
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
6. **Engine import is plain.** The skill is pip-installed as part of setup (`pip install -e <skill-root>`), so render scripts use:

   ```python
   from mbb_ppt import MbbEngine as ExecEngine
   ```

   No `sys.path.insert(...)` boilerplate. No hardcoded install paths anywhere. If the import fails, the skill is not installed — instruct the user to run `pip install -e <skill-root>` and stop.

7. **Hard limits** from `references/layout-matrix.yaml` are authoritative. Never exceed them in `content.json` — the S3 gate enforces this.

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
| S2 — Structure | `references/framework/engine-api.md`, `references/layout-matrix.yaml` | per-layout files in `references/layouts/` |
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

**Read:** `references/api-cheatsheet.md`, `references/layout-matrix.yaml`, `references/framework/planning-guide.md` (sections 3 *Layout selection by task* and 5 *Layout diversity*).

**Visual-layout rule (mechanically enforced at S3):** for any deck with ≥ 6 content slides (excluding cover/TOC/section_divider/closing), pick at least 2 chart, diagram, image, or process-flow layouts. The S3 gate fails decks that are wall-to-wall text columns. Match the layout to the content shape:

- Trend / time series → `grouped_bar`, `line_chart`, `stacked_area`, `multi_bar_panel`
- Composition / share → `donut`, `stacked_bar`, `horizontal_bar`
- Ranking / outliers → `horizontal_bar`, `pareto`, `bubble`
- Two/four-way framework → `matrix_2x2`, `swot`, `risk_matrix`, `harvey_ball_table`
- Process / phased plan → `process_chevron`, `timeline`, `value_chain`
- Operating snapshot → `dashboard_kpi_chart`, `dashboard_table_chart`
- Case proof → `case_study`, `case_study_image`, `content_right_image`

**Tasks:**
1. Compute slide count from duration.
2. Choose a `layout` for each slide from the engine catalog.
3. Write a one-sentence `key_point` per slide — a complete clause, not a label.
4. Verify each layout against `layout-matrix.yaml` capacity limits.

**Produce:** `ppt-project-{slug}/outline.json`

```json
{
  "brief": {"audience": "Board", "goal": "Strategy review", "duration_minutes": 15},
  "slides": [
    {"idx": 1, "layout": "cover",         "title": "Q1 2026 strategy review", "key_point": ""},
    {"idx": 2, "layout": "toc",           "title": "Agenda",                  "key_point": ""},
    {"idx": 3, "layout": "table_insight", "title": "Three actions improve growth while protecting margin",
     "key_point": "Premium mix shift, channel expansion, and cost simplification compose the recommendation."}
  ]
}
```

**Gate S2 (self-check):**
- A `cover` slide is present.
- Slide count ≤ `duration_minutes × 1.2`.
- Every `layout` exists in `layout-matrix.yaml`.
- Every action title is a complete clause (length > 10, contains a verb).
- At most one `two_column_text` slide globally.

### S3 — Content

**Read:** `references/framework/guard-rails.md`, every file in `experiences/`

**Tasks:**
1. Fill in concrete copy, numbers, and chart data per slide.
2. Add a `source` line to every content slide.
3. Respect the `char_budget` for each field per `layout-matrix.yaml`.

**Produce:** `ppt-project-{slug}/content.json`

**Gate S3 (machine-readable, mandatory):**

```bash
python references/scripts/gate_check_content.py \
    ppt-project-{slug}/content.json  ppt-project-{slug}/
```

Read `ppt-project-{slug}/gate_content.json`. Advance only when `"passed": true`. If false, fix every item in `fail_items` and re-run.

### S4 — Render + QA

**Read:** the `references/layouts/*.md` files for the layouts you actually used.

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

### Fast Track — small decks

Skip S2 and S3 gates only when **all** of:
- Total slides ≤ 5.
- No data charts (donut, pie, gauge, bar, line, waterfall, pareto).
- The user explicitly says "quick" / "rough" / "rapid".

S1 brief, S4 gate, and S5 delivery are **never** skipped.

---

## 6. Layout capacity — hard limits

These are derived from `references/layout-matrix.yaml`. The S3 gate enforces them.

| Layout | Max items | Title chars | Body chars | Notes |
|---|---|---|---|---|
| `cover` | — | 40 | subtitle 60 | Title supports `\n`; height auto-computed |
| `toc` | 6 | 15 | desc 40 | — |
| `executive_summary` | 4 items | 40 | headline 60, item title 25, desc 80 | Items must be 3-tuples `(num, title, desc)` |
| `four_column` | **4 columns max** | 40 | col title 20, desc 120 | Items must be 3-tuples; > 4 cols overflows |
| `table_insight` | 6 rows | 40 | header 15, cell 40, insight 60 | — |
| `matrix_2x2` | 4 quadrants | 40 | label 15, desc 80 | Quadrants must be 3-tuples `(label, bg, desc)` |
| `process_chevron` | **5 steps max** | 40 | label 10, title 20, desc 50 | Step label cannot contain `\n`; > 5 steps shrinks below readable |
| `timeline` | 6 milestones | 40 | label 8, desc 40 | **Last** milestone label ≤ 6 chars (engine pins right edge) |
| `donut` / `pie` | **6 segments max** | 30 | segment label 15 | > 6 → labels collide; merge to top-N + "Other" |
| `grouped_bar` | **6 cats × 3 series** | 30 | category 8, series label 15 | > 6 → bar widths go negative |
| `stacked_bar` | 6 categories | 30 | category 8 | — |
| `horizontal_bar` | 8 items | 30 | label 20 | — |
| `two_column_text` | 2 × 5 bullets | 40 | bullet 60 | **At most one slide of this type globally** |

For the full matrix, see [`references/layout-matrix.yaml`](./references/layout-matrix.yaml).

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
eng = ExecEngine(total_slides=10)
eng.cover(title='Q1 2026 strategy review', subtitle='Board update',
          author='Strategy team', date='March 2026')
eng.toc(items=[('1', 'Executive summary', 'Recommendation and key evidence'),
               ('2', 'Market dynamics',  'Where pressure and opportunity are shifting')])
eng.executive_summary(
    title='Revenue can return to double-digit growth with three targeted actions',
    headline='Growth is concentrated in two channels and one product tier',
    items=[('1', 'Shift mix toward premium bundles',
                'Premium bundles drive higher margin with limited cost-to-serve impact'),
           ('2', 'Expand in underpenetrated channels',
                'Two distributor channels remain underdeveloped relative to peers')],
    source='Source: internal analysis, Q1 2026')
eng.closing(title='Thank you', message='Discussion and decision points')
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

**Data:** `big_number` · `two_stat` · `three_stat` · `data_table` · `metric_cards` · `metric_comparison` · `side_by_side` · `before_after` · `pros_cons` · `scorecard` · `rag_status` · `checklist` · `harvey_ball_table`

**Process:** `timeline` · `vertical_steps` · `process_chevron` · `value_chain` · `decision_tree` · `agenda` · `action_items`

**Frameworks:** `matrix_2x2` · `swot` · `temple` · `pyramid` · `stakeholder_map` · `risk_matrix` · `icon_grid`

**Charts:** `grouped_bar` · `stacked_bar` · `horizontal_bar` · `line_chart` · `waterfall` · `pareto` · `stacked_area` · `donut` · `bubble` · `kpi_tracker` · `multi_bar_panel`

**Image / visual:** `content_right_image` · `three_images` · `image_four_points` · `full_width_image` · `case_study_image` · `two_col_image_grid` · `goals_illustration` · `quote_bg_image` · `quote` · `numbered_list_panel`

**Dashboards:** `dashboard_kpi_chart` · `dashboard_table_chart`

**Team / meta:** `meet_the_team` · `case_study` · `two_column_text` · `four_column`

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
| 15 | Content boundary `(0.5, 1.1)` to `(9.5, 6.9)` | render gate |
| 16 | ≥ 0.1" between vertically adjacent elements | render gate |
| 17 | Insight bar / footnote area ≥ 0.4" tall | render gate |
| 18 | Page numbers locked at `(9.3, 7.05, 0.5×0.25)` | code |

Rules numbered 1–10 originate in Likaku's upstream skill (`v1.9` and `v2.0`); 11–18 are added in this adaptation.

---

## 10. Slide content rules

- ≥ 0.15" gap between title separator line and the first content shape.
- Insight bars must not overlap the last row of a table or chart. Reserve 0.6" at the bottom of the content area for footnote/source before any insight bar.
- Bullet text inside a filled shape: ≥ 0.1" inset on all four sides.

### Mandatory slide elements

Every content slide (excluding Cover and Closing): action title, title separator line, content area, source attribution, page number.

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
6. ≥ 1 visual-relief slide in 8+ slide decks.
7. Disciplined typography and spacing.
8. Local-only unless integrations are explicitly approved.
9. `eng.save()` is the canonical output path.
10. Run both gates. If you didn't run them, you didn't pass them.

---

## 15. Common mistakes

- Topic-only slide titles.
- Bullet-heavy opening slides.
- Two-column text repeated across slides.
- Circular charts built from tiny rectangles.
- Legends whose colors do not match the chart.
- Text boxes touching shape edges.
- Fixed-size layouts for variable item counts.
- Action titles longer than 120 chars or shorter than 10 chars.
- Skipping the storyboard.
- **Verbal gate-pass.**
- **Verbal whitelist exemptions.**

---

## 16. Reference materials

**Communication:** Minto, *The Pyramid Principle* · Zelazny, *Say It with Charts* · Duarte, *Slide:ology* · Duarte blog (<https://www.duarte.com/blog>).

**Data viz:** Knaflic, *Storytelling with Data* · Tufte, *The Visual Display of Quantitative Information*.

**Slide execution:** Rasiel, *The McKinsey Way* · HBR, *Guide to Persuasive Presentations*.

**Design system:** Material Design typography (<https://m3.material.io/styles/typography>) · DM Sans specimen (<https://fonts.google.com/specimen/DM+Sans>).

**Engineering:** Likaku, [Mck-ppt-design-skill](https://github.com/likaku/Mck-ppt-design-skill) and [harness-skill-upgrader](https://github.com/likaku/harness-skill-upgrader). The five-stage workflow, gate scripts, and harness philosophy in this skill are adapted from those projects.

---

## 17. Example slide-title rewrites

| Weak | Strong |
|---|---|
| Market overview | Share is shifting to low-cost entrants while demand remains resilient |
| Financial analysis | Margin erosion is driven by fixed overhead rather than labor |
| Strategic options | The best path is to expand in Spain while simplifying support operations |
| Customer feedback | Customers value speed and reliability more than feature breadth |
| Implementation plan | A phased rollout reduces execution risk and accelerates learning |

---

## 18. Maintenance

This v2.1 specification is the entry point. Detailed knowledge lives in `references/`, `experiences/`, and the upstream `mbb_ppt/` Python package. When updating:

- Treat `experiences/` as append-only — never delete entries; mark superseded ones with `Superseded by NNN`.
- When adding a layout limit, update `references/layout-matrix.yaml` AND `gate_check_content.py` together.
- When adding a render check, update `gate_check_render.py` AND § 9 (Production guard rails) together.
- Keep credit upstream — this skill is built on Likaku's work and that attribution stays.
