# ExecEngine API — Quick Reference

> **Loaded at S2 (Structure).** This file is a scannable index. Pick a layout method, then look up its capacity in [`layout-matrix.yaml`](../layout-matrix.yaml) and any layout-specific contract in `references/layouts/<category>.md`.
>
> The implementation lives in `mbb_ppt/engine.py`. Class is `MbbEngine`, documented as `ExecEngine`. All methods are instance methods on a single engine; each call adds one slide and increments the page counter.

---

## Engine lifecycle

```python
import sys, os
sys.path.insert(0, '/path/to/mbb-ppt-generator')   # skill root
from mbb_ppt import MbbEngine as ExecEngine
from mbb_ppt.constants import *

eng = ExecEngine(total_slides=N)        # N drives the page-number denominator
eng.cover(...)                          # one method = one slide
eng.executive_summary(...)
# ... more slides ...
eng.save('output/deck.pptx')            # runs full_cleanup() automatically
```

Constructor: `MbbEngine(total_slides=30)`. Pass the actual slide count from your outline so page numbers (`1/N`, `2/N`, …) are correct. Mismatched values render visibly wrong page numbers.

`eng.save(outpath)` performs three-layer XML cleanup (removes `p:style` from every shape, strips theme shadow / 3D effects, repacks the OOXML zip). Do not call `full_cleanup()` separately — `save()` does it.

---

## Method index

The numbers in the right column point to the entry in [`layout-matrix.yaml`](../layout-matrix.yaml) where capacity limits and `char_budget` live. **Always consult the matrix before filling content** — the S3 gate enforces those numbers.

### Structure (5)

| Method | Signature | Purpose | Matrix |
|---|---|---|---|
| `cover` | `(title, subtitle='', author='', date='', cover_image=None)` | Title slide — accent line top, big title, optional subtitle/author/date, optional full-bleed image. `cover_image` is `None` (default), `'auto'` (cloud), or a local path. | `cover` |
| `toc` | `(title='Table of Contents', items=None, source='')` | Numbered table of contents. `items` is a list of `(num, title, description)` 3-tuples. | `toc` |
| `section_divider` | `(section_label, title, subtitle='')` | Chapter break — navy left bar + label + large title. | `section_divider` |
| `appendix_title` | `(title, subtitle='')` | Centered title with accent lines, used to mark back-matter. | `appendix_title` |
| `closing` | `(title, message='', source_text='')` | Final slide — centered title + optional message + accent line. | `closing` |

### Data and statistics (8)

| Method | Signature | Purpose | Matrix |
|---|---|---|---|
| `big_number` | `(title, number, unit='', description='', detail_items=None, source='', bottom_bar=None)` | Single dominant statistic with right-side description and optional bullets. | `big_number` |
| `two_stat` | `(title, stats, detail_items=None, source='')` | Two side-by-side big numbers. `stats` is `[(number, label), (number, label)]`. | `two_stat` |
| `three_stat` | `(title, stats, detail_items=None, source='')` | Three big numbers in a row. | `three_stat` |
| `data_table` | `(title, headers, rows, col_widths=None, source='', bottom_bar=None)` | Header row + data rows with separators. | `data_table` |
| `metric_cards` | `(title, cards, source='')` | 3–4 accent-colored metric cards. `cards` is `[(label, value, desc), …]`. | `metric_cards` |
| `metric_comparison` | `(title, metrics, source='')` | Before/After row cards with delta badges. | (see `metric_comparison`) |
| `table_insight` ★ | `(title, headers, rows, insights, col_widths=None, insight_title='Insight:', source='', bottom_bar=None)` | **Editorial layout — left table + right gray insight panel.** Strongly preferred for opening analysis slides. | `table_insight` |
| `scorecard` | `(title, items, source='')` | Items with progress bars. | `scorecard` |

### Frameworks and matrices (6 active + 1 retired)

| Method | Signature | Purpose | Matrix |
|---|---|---|---|
| `matrix_2x2` | `(title, quadrants, axis_labels=None, source='', bottom_bar=None)` | 2×2 grid. `quadrants` is **exactly 4** `(label, bg_color, desc)` 3-tuples. | `matrix_2x2` |
| `swot` | `(title, quadrants, source='')` | 2×2 colored SWOT grid. | `swot` |
| `temple` | `(title, roof_text, pillar_names, foundation_text, pillar_colors=None, source='')` | Roof + pillars + foundation framework. | (see `temple`) |
| `pyramid` | `(title, levels, source='', bottom_bar=None, detail_rows=None, detail_headers=None)` | Staircase evolution — ascending steps with optional detail table. PNG icons supported (200×200 transparent, white strokes). | (see `pyramid`) |
| `stakeholder_map` | `(title, quadrants, x_label='Influence →', y_label='Interest ↑', summary=None, source='')` | Stakeholder 2×2 with member lists per quadrant. | (see `stakeholder_map`) |
| `risk_matrix` | `(title, grid_colors, grid_lights, risks, y_labels=None, x_labels=None, notes=None, source='')` | 3×3 heat-map grid with risk labels. | (see `risk_matrix`) |
| `venn` | `(title, circles, overlap_label='', right_text=None, source='')` | **⚠️ Retired.** Use `side_by_side` instead. | retired |

### Comparison (5)

| Method | Signature | Purpose | Matrix |
|---|---|---|---|
| `side_by_side` | `(title, options, source='')` | Two columns with navy headers. | `side_by_side` |
| `before_after` | `(title, before_title, before_points, after_title, after_points, source='', corner_label='', bottom_bar=None, left_summary='', right_summary='', right_summary_color=None)` | Vertical divider with circle-arrow transition. | `before_after` |
| `pros_cons` | `(title, pros_title, pros, cons_title, cons, conclusion=None, source='')` | Two-column Pros / Cons with optional conclusion. | `pros_cons` |
| `rag_status` | `(title, headers, rows, source='')` | Table with red/amber/green status dots. | `rag_status` |
| `metric_comparison` | `(title, metrics, source='')` | Before / After with delta badges. | (see `metric_comparison`) |

### Narrative (6)

| Method | Signature | Purpose | Matrix |
|---|---|---|---|
| `executive_summary` ★ | `(title, headline, items, source='')` | Navy headline band + numbered items. **Use early in deck.** `items` is `[(num, title, desc), …]`. | `executive_summary` |
| `key_takeaway` | `(title, left_text, takeaways, source='')` | Left analysis (3 paragraphs) + right gray takeaway panel. | `key_takeaway` |
| `four_column` | `(title, items, source='')` | Four parallel cards. `items` is `[(num, col_title, desc), …]`, max **4 columns**. | `four_column` |
| `two_column_text` | `(title, columns, source='')` | Lettered columns with bullet lists. **Max 1 per deck** — use sparingly. | `two_column_text` |
| `quote` | `(quote_text, attribution='')` | Centered quote with accent lines. | (see `quote`) |
| `numbered_list_panel` | `(title, items, panel=None, source='')` | Left numbered list + right accent panel. | (see `numbered_list_panel`) |

### Process and timeline (7)

| Method | Signature | Purpose | Matrix |
|---|---|---|---|
| `timeline` | `(title, milestones, source='', bottom_bar=None)` | Horizontal line with milestone nodes. **Last milestone label ≤ 6 chars** (engine pins it right). | `timeline` |
| `vertical_steps` | `(title, steps, source='', bottom_bar=None)` | Top-down numbered step list. | `vertical_steps` |
| `process_chevron` | `(title, steps, source='', bottom_bar=None)` | Horizontal chevrons. **≤ 5 steps**, step label cannot contain `\n`, desc ≤ 50 chars. | `process_chevron` |
| `value_chain` | `(title, stages, source='', bottom_bar=None)` | Stages joined by arrows. | `value_chain` |
| `decision_tree` | `(title, root, branches, right_panel=None, source='')` | Root → L1 → L2 hierarchy with connector lines. | (see `decision_tree`) |
| `agenda` | `(title, headers, items, footer_text='', source='')` | Time-allocated meeting agenda table. | (see `agenda`) |
| `action_items` | `(title, actions, source='')` | Numbered actions with timeline + owner. | `action_items` |
| `cycle` | `(title, phases, right_panel=None, source='')` | **⚠️ Retired.** Use `process_chevron` + return arrow. | retired |
| `funnel` | `(title, stages, source='')` | **⚠️ Retired.** Use `horizontal_bar` with descending values. | retired |

### Charts — circular (3, 1 active)

| Method | Signature | Purpose | Matrix |
|---|---|---|---|
| `donut` | `(title, segments, center_label='', center_sub='', legend_x=None, summary=None, source='')` | BLOCK_ARC ring segments + center label. **≤ 6 segments** — beyond that, top-5 + Other. | `donut` |
| `pie` | `(title, segments, legend_x=None, summary=None, source='')` | **⚠️ Retired.** Use `donut`. | retired |
| `gauge` | `(title, score, benchmarks=None, source='')` | **⚠️ Retired.** Use `big_number` + KPI bullet. | retired |

### Charts — bar and line (5)

| Method | Signature | Purpose | Matrix |
|---|---|---|---|
| `grouped_bar` | `(title, categories, series, data, max_val=None, y_ticks=None, summary=None, source='')` | Vertical bars grouped by category. **≤ 6 categories × 3 series.** | `grouped_bar` |
| `stacked_bar` | `(title, periods, series, data, summary=None, source='')` | 100% stacked vertical bars. | `stacked_bar` |
| `horizontal_bar` | `(title, items, summary=None, source='')` | Labeled horizontal bars with value/% labels. | `horizontal_bar` |
| `line_chart` | `(title, x_labels, y_labels, values, legend_label='', summary=None, source='')` | Single line via dot approximation. | `line_chart` |
| `multi_bar_panel` | `(title, panels, connectors=None, footnotes=None, source='')` | 2–3 side-by-side bar-chart panels with CAGR arrows. Editorial style. | `multi_bar_panel` |

### Charts — advanced (5)

| Method | Signature | Purpose | Matrix |
|---|---|---|---|
| `waterfall` | `(title, items, max_val=None, legend_items=None, summary=None, source='')` | Bridge from start to end with cumulative connectors. | `waterfall` |
| `pareto` | `(title, items, max_val=None, summary=None, source='')` | Descending bars + cumulative line + 80% threshold. | `pareto` |
| `stacked_area` | `(title, years, series_data, max_val=None, summary=None, source='')` | Cumulative stacked columns approximating an area chart. | `stacked_area` |
| `bubble` | `(title, bubbles, x_label='', y_label='', legend_items=None, summary=None, source='')` | Positioned circles on XY plane with size encoding. | `bubble` |
| `kpi_tracker` | `(title, kpis, summary=None, source='')` | Progress bars with status dots, OKR-style. | `kpi_tracker` |

### Dashboards (2)

| Method | Signature | Purpose | Matrix |
|---|---|---|---|
| `dashboard_kpi_chart` | `(title, kpi_cards, chart_data=None, summary=None, source='')` | Top KPI cards + middle chart + bottom summary. | `dashboard_kpi_chart` |
| `dashboard_table_chart` | `(title, table_data, chart_data=None, factoids=None, source='')` | Left table + right chart + bottom factoid cards. | `dashboard_table_chart` |

### Image / visual (8)

| Method | Signature | Purpose | Matrix |
|---|---|---|---|
| `content_right_image` | `(title, subtitle, bullets, takeaway='', image_label='Image', source='')` | Text left, image placeholder right. | (see `images.md`) |
| `three_images` | `(title, items, source='')` | Three image+caption columns. | (see `images.md`) |
| `image_four_points` | `(title, image_label, points, source='')` | Center image with 4 corner cards. | (see `images.md`) |
| `full_width_image` | `(title, image_label, overlay_text='', attribution='', source='')` | Edge-to-edge hero image with text overlay. | (see `images.md`) |
| `case_study_image` | `(title, sections, image_label, kpis=None, source='')` | Left text sections + right image + KPI boxes. | (see `images.md`) |
| `quote_bg_image` | `(image_label, quote_text, attribution='', source='')` | Image top + quote bottom (keynote-style). | (see `images.md`) |
| `goals_illustration` | `(title, goals, image_label, source='')` | Left numbered goals + right illustration. | (see `images.md`) |
| `two_col_image_grid` | `(title, items, source='')` | 2×2 image-text catalog grid. | (see `images.md`) |

### Special (5)

| Method | Signature | Purpose | Matrix |
|---|---|---|---|
| `icon_grid` | `(title, items, cols=3, source='')` | Grid of icon cards (3×3 max, also 4×2). | `icon_grid` |
| `checklist` | `(title, columns, col_widths, rows, status_map=None, source='', bottom_bar=None)` | Status table with progress bar across the bottom. | `checklist` |
| `harvey_ball_table` | `(title, criteria, options, scores, legend_text=None, summary=None, source='')` | Multi-criteria evaluation matrix with quarter / half / three-quarter / full Harvey Balls. | (see `harvey_ball_table`) |
| `meet_the_team` | `(title, members, source='')` | Profile cards in a row. | `meet_the_team` |
| `case_study` | `(title, sections, result_box=None, source='')` | Situation / Action / Result narrative. | `case_study` |

★ = high-impact opening layouts. Strongly preferred on slides 2–5 of any substantive deck.

---

## Common parameter contracts

A handful of parameter names recur. Get these right once and most other layouts follow the same pattern.

| Parameter | Contract | Example |
|---|---|---|
| `title` | Action title — conclusion-led clause, ≤ 120 chars (Rule 14). Validated by S3 gate. | `'Margin pressure is concentrated in two product lines'` |
| `source` | Bottom-left attribution. Required on every content slide (S3 gate). Format: `Source: <origin>, <date>`. | `'Source: internal analysis, Q1 2026'` |
| `items` | Layout-dependent tuple list. **3-tuples** for `four_column`, `executive_summary`, `toc`. Check the matrix. | `[('1', 'Title', 'Desc'), …]` |
| `headers` | List of column header strings. | `['Action', 'Mechanism', 'Expected impact']` |
| `rows` | List of row lists, each matching `headers` arity. | `[['Premium', '+12%', '…'], …]` |
| `bottom_bar` | Optional `(label, text)` tuple. Triggers gray bar at bottom. Min height 0.4" (Rule 17). | `('Implication', 'Funds growth …')` |
| `summary` | Optional bottom-line text under charts. | `'CAGR 14% over the period'` |
| `segments` | For `donut`: list of `(percent, color, label)` 3-tuples. **≤ 6**. | `[(0.42, NAVY, 'Premium'), …]` |
| `series` | For `grouped_bar` / `stacked_bar`: list of `(label, color)`. **≤ 3** for `grouped_bar`. | `[('Premium', NAVY), ('Partner', ACCENT_BLUE)]` |
| `data` | For `grouped_bar`: list of lists, outer = categories, inner = series values. | `[[120, 80], [145, 95], …]` |
| `cover_image` | `None` (text-only cover) or `'/path/to/local.png'` (full-bleed background). | `None` |
| `total_slides` | Constructor — drives page-number denominator. | `MbbEngine(total_slides=10)` |

---

## Color constants

Available from `mbb_ppt.constants`:

- Primary: `NAVY`, `WHITE`, `BLACK`, `DARK_GRAY`, `MED_GRAY`, `LINE_GRAY`, `BG_GRAY`, `HEADING_ACCENT`, `SECTION_BG`
- Accent: `ACCENT_BLUE`, `ACCENT_GREEN`, `ACCENT_ORANGE`, `ACCENT_RED` (paired with `LIGHT_*` backgrounds via `ACCENT_PAIRS`)
- Warm (optional): `WARM_NAVY`, `WARM_GOLD`, `WARM_STONE`

Use accents only when ≥ 3 parallel items need differentiation. Never replace `NAVY` as the primary anchor.

---

## Font constants

`HEADING_FONT` (= `"DM Sans"`, fallback Calibri) for cover titles and large display text. `BODY_FONT` (= `"Arial"`) for body text. `SOURCE_FONT` (= `"Arial"`) for footnotes. Sizes from `COVER_TITLE_SIZE` (44pt) down to `FOOTNOTE_SIZE` (9pt).

Backward-compat aliases retained: `FONT_HEADER` ≡ `HEADING_FONT`, `FONT_BODY` ≡ `BODY_FONT`, `FONT_EA` (Latin font, no-op for English text — kept so existing engine call sites keep running).

---

## Where to go next

- **Capacity check before writing content:** [`../layout-matrix.yaml`](../layout-matrix.yaml).
- **Production rules to validate against:** `guard-rails.md` (this directory).
- **Layout-specific examples and wireframes:** `../layouts/<category>.md` (per layout family).
- **Past defects and fixes:** `../../experiences/*.md` — read at S3 to avoid recurring traps.
- **Source code (authoritative truth):** `../../mbb_ppt/engine.py`. Every method has a docstring; consult it when this index does not answer.
