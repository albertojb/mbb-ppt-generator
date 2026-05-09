# ExecEngine — API Cheatsheet

> **Auto-generated from `references/api-schemas.yaml` by `references/scripts/generate_cheatsheet.py`.**
> Do not hand-edit this file — edit the schema and re-run the generator.
> Convention: `eng = ExecEngine(total_slides=N)` then call methods one per slide. `eng.save(outpath)` finalizes.

_Schema version: 1. 62 active layouts, 5 retired._

## Structure

| Method | Signature | One-liner | Param shapes |
|---|---|---|---|
| `cover` | `(title, subtitle='', author='', date='', cover_image=None)` | #1 Cover slide — title, subtitle, author, date, accent line. | subtitle=str(60), author=str(30), date=str(30), cover_image=path, … |
| `closing` | `(title, message='', source_text='')` | #36 Closing / thank-you slide. | message=str(60), source_text=str(80) |
| `section_divider` | `(section_label, title, subtitle='')` | #5 Section divider — primary left bar, large title. | section_label=str(8)*, subtitle=str(80) |
| `toc` | `(title='Table of Contents', items=None, source='')` | #6 Table of contents — numbered items with descriptions. | items=list[tuple3]≤6, source=str(80) |
| `appendix_title` | `(title, subtitle='')` | #7 Appendix title — centered title with accent lines. | subtitle=str(60) |

## Narrative

| Method | Signature | One-liner | Param shapes |
|---|---|---|---|
| `executive_summary` | `(title, headline, items, source='')` | #24 Executive summary — primary headline + numbered items. | headline=str(60)*, items=list[tuple3]≤4*, source=str(80) |
| `key_takeaway` | `(title, left_text, takeaways, source='', left_title='Analysis', right_title='Key takeaways')` | #25 Key takeaway — left analysis + right gray panel. | left_text=list[str]≤5, takeaways=list[str]≤3*, left_title=str(20), right_title=str(25), … |
| `quote` | `(quote_text, attribution='')` | #26 Quote slide — centered quote with accent lines. | quote_text=str(200)*, attribution=str(60) |
| `two_column_text` | `(title, columns, source='')` | #27 Two-column text — lettered columns with bullet lists. Max 1 per deck. | columns=list[dict]≤2*, source=str(80) |
| `four_column` | `(title, items, source='')` | #28 Four-column overview — 4 numbered vertical cards. | items=list[tuple3]≤4*, source=str(80) |

## Data

| Method | Signature | One-liner | Param shapes |
|---|---|---|---|
| `three_stat` | `(title, stats, detail_items=None, source='')` | #10 Three-stat — three big numbers in a row. | stats=list[tuple3]≤3*, detail_items=list[str]≤4, source=str(80) |
| `data_table` | `(title, headers, rows, col_widths=None, source='', bottom_bar=None)` | #11 Data table — header row + data rows with separators. | headers=list[str]*, rows=list[list]≤8*, col_widths=list[float], source=str(80), … |
| `metric_cards` | `(title, cards, source='')` | #12 Metric cards — 3-4 accent-colored cards. | cards=list[dict]≤4*, source=str(80) |
| `scorecard` | `(title, items, source='', headers=None)` | #23 Scorecard — items with progress bars. | items=list[tuple3]≤6*, headers=list[str], source=str(80) |
| `kpi_tracker` | `(title, kpis, summary=None, source='')` | #52 KPI tracker — progress bars with status dots. | kpis=list[dict]≤6*, summary=tuple2, source=str(80) |
| `metric_comparison` | `(title, metrics, source='')` | #62 Metric comparison — before/after row cards with delta badges. | metrics=list[dict]≤4*, source=str(80) |
| `table_insight` | `(title, headers, rows, insights, col_widths=None, insight_title='Insight:', source='', bottom_bar=None)` | Table + right insight panel — MBB-style editorial layout. | headers=list[str]*, rows=list[list]≤6*, insights=list[str]*, col_widths=list[float], … |
| `big_number` | `(title, number, unit='', description='', detail_items=None, source='', bottom_bar=None)` | #8 Big number — large stat with context. | number=str(10)*, unit=str(8), description=str(60), detail_items=list[str]≤4, … |
| `two_stat` | `(title, stats, detail_items=None, source='')` | #9 Two-stat comparison — two big numbers side by side. | stats=list[tuple2]≤2*, detail_items=list[str]≤4, source=str(80) |

## Comparison

| Method | Signature | One-liner | Param shapes |
|---|---|---|---|
| `side_by_side` | `(title, options, source='')` | #19 Side-by-side comparison — two columns with primary headers. | options=list[dict]≤2*, source=str(80) |
| `before_after` | `(title, before_title, before_points, after_title, after_points, source='', corner_label='', bottom_bar=None, left_summary='', right_summary='', right_summary_color=None)` | #20 Before/after — vertical divider with arrow. | before_title=str(20)*, before_points=list[str]≤5*, after_title=str(20)*, after_points=list[str]≤5*, … |
| `pros_cons` | `(title, pros_title, pros, cons_title, cons, conclusion=None, source='')` | #21 Pros/cons — two-column layout. | pros_title=str(20)*, pros=list[str]≤5*, cons_title=str(20)*, cons=list[str]≤5*, … |
| `rag_status` | `(title, headers, rows, source='')` | #22 RAG status — table with red/amber/green status dots. | headers=list[str]*, rows=list[list]≤8*, source=str(80) |
| `harvey_ball_table` | `(title, criteria, options, scores, legend_text=None, summary=None, source='', first_col_w=None, opt_col_w=None)` | #56 Harvey Ball table — matrix with circular fill indicators. | criteria=list[str]≤7*, options=list[str]≤5*, scores=list[list]*, legend_text=list[str], … |
| `checklist` | `(title, columns, col_widths, rows, status_map=None, source='', bottom_bar=None)` | #61 Checklist / status table. | columns=list[str]*, col_widths=list[float]*, rows=list[list]≤7*, status_map=dict, … |

## Process

| Method | Signature | One-liner | Param shapes |
|---|---|---|---|
| `process_chevron` | `(title, steps, source='', bottom_bar=None)` | #16 Process chevron — horizontal step flow with arrows (≤ 5 steps). | steps=list[tuple3]≤5*, bottom_bar=tuple2, source=str(80) |
| `timeline` | `(title, milestones, source='', bottom_bar=None)` | #29 Timeline / roadmap — horizontal line with milestone nodes. | milestones=list[tuple2]≤6*, bottom_bar=tuple2, source=str(80) |
| `vertical_steps` | `(title, steps, source='', bottom_bar=None)` | #30 Vertical steps — top-down numbered steps. | steps=list[tuple3]≤5*, bottom_bar=tuple2, source=str(80) |
| `action_items` | `(title, actions, source='')` | #35 Action items — cards with timeline + owner. | actions=list[dict]≤4*, source=str(80) |
| `decision_tree` | `(title, root, branches, right_panel=None, source='')` | #60 Decision tree — root → L1 → L2 hierarchy with connector lines. | root=str(30)*, branches=list[dict]≤6*, right_panel=str(200), source=str(80), … |
| `agenda` | `(title, headers, items, footer_text='', source='')` | #66 Agenda — table-style meeting agenda. | headers=list[str]*, items=list[list]≤8*, footer_text=str(80), source=str(80), … |
| `value_chain` | `(title, stages, source='', bottom_bar=None)` | #67 Value chain — horizontal flow with arrows. | stages=list[tuple3]≤5*, bottom_bar=tuple2, source=str(80) |

## Frameworks

| Method | Signature | One-liner | Param shapes |
|---|---|---|---|
| `matrix_2x2` | `(title, quadrants, axis_labels=None, source='', bottom_bar=None)` | #13 2×2 matrix — four quadrants. | quadrants=list[tuple3]≤4*, axis_labels=tuple2, bottom_bar=tuple2, source=str(80), … |
| `pyramid` | `(title, levels, source='', bottom_bar=None, detail_rows=None, detail_headers=None)` | #15 Staircase / pyramid evolution — ascending steps. | levels=list[tuple2]≤5*, detail_headers=list[str], detail_rows=list[list], bottom_bar=tuple2, … |
| `temple` | `(title, roof_text, pillar_names, foundation_text, pillar_colors=None, source='')` | #18 Temple / house framework — roof + pillars + foundation. | roof_text=str(60)*, pillar_names=list[str]≤5*, foundation_text=str(60)*, pillar_colors=list[str], … |
| `risk_matrix` | `(title, grid_colors, grid_lights, risks, y_labels=None, x_labels=None, notes=None, source='')` | #54 Risk matrix — 3×3 heatmap with risk labels. | grid_colors=list[list]*, grid_lights=list[list]*, risks=list[dict]≤12*, y_labels=list[str], … |
| `stakeholder_map` | `(title, quadrants, x_label='Influence →', y_label='Interest ↑', summary=None, source='')` | #59 Stakeholder map — 2×2 with stakeholder lists. | quadrants=dict*, x_label=str(30), y_label=str(30), summary=str(120), … |
| `icon_grid` | `(title, items, cols=3, source='')` | #63 Icon grid — grid of icon cards. | items=list[tuple3]≤9*, cols=int, source=str(80) |
| `swot` | `(title, quadrants, source='')` | #65 SWOT analysis — 2×2 colored grid. | quadrants=dict*, source=str(80) |

## Charts

| Method | Signature | One-liner | Param shapes |
|---|---|---|---|
| `grouped_bar` | `(title, categories, series, data, max_val=None, y_ticks=None, summary=None, source='')` | #37 Grouped bar — ≤ 6 categories × ≤ 3 series. | categories=list[str]≤6*, series=list[tuple2]≤3*, data=list[list]*, max_val=float, … |
| `stacked_bar` | `(title, periods, series, data, summary=None, source='')` | #38 Stacked (100%) bar — ≤ 6 categories. | periods=list[str]≤6*, series=list[tuple2]≤5*, data=list[list]*, summary=tuple2, … |
| `horizontal_bar` | `(title, items, summary=None, source='')` | #39 Horizontal bar — ≤ 8 items. | items=list[tuple3]≤8*, summary=tuple2, source=str(80) |
| `donut` | `(title, segments, center_label='', center_sub='', legend_x=None, summary=None, source='')` | #48 Donut — ≤ 6 segments. BLOCK_ARC native shape. | segments=list[tuple3]≤6*, center_label=str(8), center_sub=str(25), legend_x=float, … |
| `waterfall` | `(title, items, max_val=None, legend_items=None, summary=None, source='')` | #49 Waterfall bridge from start to end. | items=list[tuple3]≤8*, max_val=float, legend_items=list[tuple2], summary=tuple2, … |
| `line_chart` | `(title, x_labels, y_labels, values, legend_label='', summary=None, source='')` | #50 Single-line trend. | x_labels=list[str]≤12*, y_labels=list[str]*, values=list[float]*, legend_label=str(25), … |
| `pareto` | `(title, items, max_val=None, summary=None, source='')` | #51 Pareto — descending bars with cumulative %. | items=list[tuple2]≤8*, max_val=float, summary=tuple2, source=str(80), … |
| `bubble` | `(title, bubbles, x_label='', y_label='', legend_items=None, summary=None, source='')` | #53 Bubble / scatter on XY plane. | bubbles=list[dict]≤10*, x_label=str(30), y_label=str(30), legend_items=list[tuple2], … |
| `stacked_area` | `(title, years, series_data, max_val=None, summary=None, source='', currency_symbol='$', summary_label='Trend')` | #70 Stacked area approximation via stacked columns. | years=list[str]*, series_data=list[dict]≤5*, max_val=float, currency_symbol=str(3), … |
| `multi_bar_panel` | `(title, panels, connectors=None, footnotes=None, source='')` | #71 Multi-bar panel — 2-3 side-by-side bar charts. | panels=list[dict]≤3*, connectors=list[str], footnotes=list[str], source=str(80), … |

## Image / visual layouts

| Method | Signature | One-liner | Param shapes |
|---|---|---|---|
| `content_right_image` | `(title, subtitle, bullets, takeaway='', image_label='Image', source='')` | #40 Content + right image. | subtitle=str(60), bullets=list[str]≤5*, takeaway=str(100), image_label=str(30), … |
| `three_images` | `(title, items, source='')` | #42 Three images — image+caption columns. | items=list[tuple3]≤3*, source=str(80) |
| `image_four_points` | `(title, image_label, points, source='')` | #43 Image + 4 points (center image + 4 corner cards). | image_label=str(30)*, points=list[tuple2]≤4*, source=str(80) |
| `full_width_image` | `(title, image_label, overlay_text='', attribution='', source='')` | #44 Full-width image with text overlay. | image_label=str(30)*, overlay_text=str(100), attribution=str(60), source=str(80), … |
| `case_study_image` | `(title, sections, image_label, kpis=None, source='')` | #45 Case study with image — text + image + KPIs. | sections=list[tuple2]≤3*, image_label=str(30)*, kpis=list[tuple2]≤4, source=str(80), … |
| `quote_bg_image` | `(image_label, quote_text, attribution='', source='')` | #46 Quote with background image — image top + quote bottom. | image_label=str(30)*, quote_text=str(200)*, attribution=str(60), source=str(80), … |
| `goals_illustration` | `(title, goals, image_label, source='')` | #47 Goals with illustration — numbered goals + image. | goals=list[tuple2]≤5*, image_label=str(30)*, source=str(80) |
| `two_col_image_grid` | `(title, items, source='')` | #68 Two-column image + text grid (2×2). | items=list[tuple3]≤4*, source=str(80) |
| `numbered_list_panel` | `(title, items, panel=None, source='')` | #69 Numbered list + side accent panel. | items=list[tuple2]≤5*, panel=dict, source=str(80) |

## Dashboards

| Method | Signature | One-liner | Param shapes |
|---|---|---|---|
| `dashboard_kpi_chart` | `(title, kpi_cards, chart_data=None, summary=None, source='')` | #57 Dashboard — top KPI cards + bottom mini chart. | kpi_cards=list[dict]≤4*, chart_data=dict, summary=tuple2, source=str(80), … |
| `dashboard_table_chart` | `(title, table_data, chart_data=None, factoids=None, source='')` | #58 Dashboard — left table + right mini chart + facts. | table_data=dict*, chart_data=dict, factoids=list[str]≤3, source=str(80), … |

## Team / case studies

| Method | Signature | One-liner | Param shapes |
|---|---|---|---|
| `meet_the_team` | `(title, members, source='')` | #33 Meet the team — profile cards in a row. | members=list[dict]≤4*, source=str(80) |
| `case_study` | `(title, sections, result_box=None, source='')` | #34 Case study — S/A/R or custom sections. | sections=list[tuple2]≤3*, result_box=dict, source=str(80) |

## Retired (kept for back-compat — do not use in new decks)

| Method | Replacement | Reason |
|---|---|---|
| `cycle` | `process_chevron` | Better expressed as process_chevron + return arrow. |
| `funnel` | `horizontal_bar` | Superseded by horizontal_bar. |
| `gauge` | `big_number` | Superseded by big_number + KPI bullet. |
| `pie` | `donut` | donut is strictly better. |
| `venn` | `side_by_side` | Visual ambiguity at small sizes. |

## Global gate constraints (deck-level)

**two_column_text**
- max_per_deck: 1
- rationale: Two columns of unbroken prose is the most monotonous layout.

**executive_summary**
- max_pct_of_content_slides: 0.15
- rationale: Most permissive layout; over-using produces visually identical decks.

**visual_density_floor**
- formula: max(2, N // 4)
- triggers_at_n_content_slides: 6
- rationale: Decks need a chart/diagram/image floor that scales with deck length.

## Color conventions

Slots with `role: color` accept a named constant from `mbb_ppt.constants`, an `RGBColor`, or a `'#RRGGBB'` string.

- **primary** — PRIMARY (= NAVY alias) — forest green #1B4332. Use for headlines, accents.
- **accent** — Any of ACCENT_BLUE / ACCENT_GREEN / ACCENT_ORANGE / ACCENT_RED.
- **neutral** — DARK_GRAY / MED_GRAY / LINE_GRAY / BG_GRAY for backgrounds and rule lines.
- **bg_light** — Light pair color (LIGHT_BLUE/LIGHT_GREEN/LIGHT_ORANGE/LIGHT_RED) for fills.
- **hex_string** — Any '#RRGGBB' string — engine converts to RGBColor automatically.

## Enum value maps

### `harvey_ball`
Fill mapping for harvey_ball_table.scores (int 0-4).
- `0` → empty
- `1` → quarter
- `2` → half
- `3` → three_quarters
- `4` → full

### `rag_status`
Status indicator for rag_status row cells.
- `R` → red
- `A` → amber
- `G` → green

---

For full per-parameter shape detail (tuple slots, dict keys, role hints), read `references/api-schemas.yaml` directly. For implicit constraints not surfaced in tables, see `references/known-pitfalls.md`.
