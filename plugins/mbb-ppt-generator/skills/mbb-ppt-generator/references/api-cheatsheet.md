# ExecEngine — API Cheatsheet

> **One-page method index for the MBB PPT engine.** Auto-generated from `mbb_ppt/engine.py` docstrings; load this file at S2 to pick layouts. For full parameter docs and wireframes, see `references/layouts/*.md`. For the authoritative source, read `mbb_ppt/engine.py` directly.
>
> Convention: `eng = ExecEngine(total_slides=N)` then call methods one per slide. `eng.save(outpath)` finalizes.

## Structure layouts

| Method | Signature (positional + key kwargs) | One-liner |
|---|---|---|
| `cover` | `title, subtitle='', author='', date='', cover_image=None` | #1 Cover slide — title, subtitle, author, date, accent line. |
| `toc` | `title='Table of Contents', items=None, source=''` | #6 Table of contents — numbered items with descriptions. |
| `appendix_title` | `title, subtitle=''` | #7 Appendix title — centered title with accent lines. |
| `section_divider` | `section_label, title, subtitle=''` | #5 Section divider — primary left bar, large title. |
| `executive_summary` | `title, headline, items, source=''` | #24 Executive summary — primary headline + numbered items. |
| `key_takeaway` | `title, left_text, takeaways, source=''` | #25 Key takeaway — left analysis + right gray panel. |
| `table_insight` | `title, headers, rows, insights, col_widths=None, insight_title='Insight:', source='', bottom_bar=None` | Table + right insight panel — MBB-style editorial layout. |
| `closing` | `title, message='', source_text=''` | #36 Closing / thank-you slide. |

## Data layouts

| Method | Signature | One-liner |
|---|---|---|
| `big_number` | `title, number, unit='', description='', detail_items=None, source='', bottom_bar=None` | #8 Big number — large stat with context. |
| `two_stat` | `title, stats, detail_items=None, source=''` | #9 Two-stat comparison — two big numbers side by side. |
| `three_stat` | `title, stats, detail_items=None, source=''` | #10 Three-stat — three big numbers in a row. |
| `data_table` | `title, headers, rows, col_widths=None, source='', bottom_bar=None` | #11 Data table — header row + data rows. |
| `metric_cards` | `title, cards, source=''` | #12 Metric cards — 3-4 accent-colored cards. |
| `metric_comparison` | `title, metrics, source=''` | #62 Metric comparison — before/after row cards with delta badges. |
| `side_by_side` | `title, options, source=''` | #19 Side-by-side comparison — two columns with primary headers. |
| `before_after` | `title, before_title, before_points, after_title, after_points, source='', corner_label='', bottom_bar=None, left_summary='', right_summary='', right_summary_color=None` | #20 Before/after — vertical divider with arrow. |
| `pros_cons` | `title, pros_title, pros, cons_title, cons, conclusion=None, source=''` | #21 Pros/cons — two-column layout. |
| `scorecard` | `title, items, source=''` | #23 Scorecard — items with progress bars. |
| `rag_status` | `title, headers, rows, source=''` | #22 RAG status — table with red/amber/green status dots. |
| `checklist` | `title, columns, col_widths, rows, status_map=None, source='', bottom_bar=None` | #61 Checklist / status table. |
| `harvey_ball_table` | `title, criteria, options, scores, legend_text=None, summary=None, source=''` | #56 Harvey Ball table — matrix with circular fill indicators. |

## Process layouts

| Method | Signature | One-liner |
|---|---|---|
| `timeline` | `title, milestones, source='', bottom_bar=None` | #29 Timeline / roadmap — horizontal line with milestone nodes. (Last milestone label ≤ 6 chars — engine pins right edge.) |
| `vertical_steps` | `title, steps, source='', bottom_bar=None` | #30 Vertical steps — top-down numbered steps. |
| `process_chevron` | `title, steps, source='', bottom_bar=None` | #16 Process chevron — horizontal step flow with arrows (≤ 5 steps). |
| `value_chain` | `title, stages, source='', bottom_bar=None` | #67 Value chain — horizontal flow with arrows. |
| `decision_tree` | `title, root, branches, right_panel=None, source=''` | #60 Decision tree — root → L1 → L2 hierarchy. |
| `agenda` | `title, headers, items, footer_text='', source=''` | #66 Agenda — table-style meeting agenda. |
| `action_items` | `title, actions, source=''` | #35 Action items — cards with timeline + owner. |

## Frameworks

| Method | Signature | One-liner |
|---|---|---|
| `matrix_2x2` | `title, quadrants, axis_labels=None, source='', bottom_bar=None` | #13 2×2 matrix — four quadrants. |
| `swot` | `title, quadrants, source=''` | #65 SWOT analysis — 2×2 colored grid. |
| `temple` | `title, roof_text, pillar_names, foundation_text, pillar_colors=None, source=''` | #18 Temple / house framework — roof + pillars + foundation. |
| `pyramid` | `title, levels, source='', bottom_bar=None, detail_rows=None, detail_headers=None` | #15 Staircase / pyramid evolution — ascending steps. |
| `stakeholder_map` | `title, quadrants, x_label='Influence →', y_label='Interest ↑', summary=None, source=''` | #59 Stakeholder map — 2×2 with stakeholder lists. |
| `risk_matrix` | `title, grid_colors, grid_lights, risks, y_labels=None, x_labels=None, notes=None, source=''` | #54 Risk matrix — 3×3 heatmap with risk labels. |
| `icon_grid` | `title, items, cols=3, source=''` | #63 Icon grid — grid of icon cards. |

## Charts

| Method | Signature | Capacity / notes |
|---|---|---|
| `grouped_bar` | `title, categories, series, data, max_val=None, y_ticks=None, summary=None, source=''` | #37 Grouped bar — ≤ 6 categories × ≤ 3 series. |
| `stacked_bar` | `title, periods, series, data, summary=None, source=''` | #38 Stacked (100%) bar — ≤ 6 categories. |
| `horizontal_bar` | `title, items, summary=None, source=''` | #39 Horizontal bar — ≤ 8 items. |
| `line_chart` | `title, x_labels, y_labels, values, legend_label='', summary=None, source=''` | #50 Single-line trend. |
| `waterfall` | `title, items, max_val=None, legend_items=None, summary=None, source=''` | #49 Waterfall bridge from start to end. |
| `pareto` | `title, items, max_val=None, summary=None, source=''` | #51 Pareto — descending bars with cumulative %. |
| `stacked_area` | `title, years, series_data, max_val=None, summary=None, source=''` | #70 Stacked area approximation via stacked columns. |
| `donut` | `title, segments, center_label='', center_sub='', legend_x=None, summary=None, source=''` | #48 Donut — ≤ 6 segments. BLOCK_ARC native. |
| `bubble` | `title, bubbles, x_label='', y_label='', legend_items=None, summary=None, source=''` | #53 Bubble / scatter on XY plane. |
| `kpi_tracker` | `title, kpis, summary=None, source=''` | #52 KPI tracker — progress bars with status dots. |
| `multi_bar_panel` | `title, panels, connectors=None, footnotes=None, source=''` | #71 Multi-bar panel — 2-3 side-by-side bar charts. |

## Image / visual layouts

| Method | Signature | One-liner |
|---|---|---|
| `content_right_image` | `title, subtitle, bullets, takeaway='', image_label='Image', source=''` | #40 Content + right image. |
| `three_images` | `title, items, source=''` | #42 Three images — image+caption columns. |
| `image_four_points` | `title, image_label, points, source=''` | #43 Image + 4 points (center + corners). |
| `full_width_image` | `title, image_label, overlay_text='', attribution='', source=''` | #44 Full-width image with text overlay. |
| `case_study_image` | `title, sections, image_label, kpis=None, source=''` | #45 Case study with image — text + image + KPIs. |
| `two_col_image_grid` | `title, items, source=''` | #68 Two-column image + text grid. |
| `goals_illustration` | `title, goals, image_label, source=''` | #47 Goals with illustration — numbered goals + image. |
| `quote_bg_image` | `image_label, quote_text, attribution='', source=''` | #46 Quote with background image. |
| `quote` | `quote_text, attribution=''` | #26 Quote slide — centered quote. |
| `numbered_list_panel` | `title, items, panel=None, source=''` | #69 Numbered list + side accent panel. |

## Dashboards

| Method | Signature | One-liner |
|---|---|---|
| `dashboard_kpi_chart` | `title, kpi_cards, chart_data=None, summary=None, source=''` | #57 Dashboard — top KPI cards + bottom mini chart. |
| `dashboard_table_chart` | `title, table_data, chart_data=None, factoids=None, source=''` | #58 Dashboard — left table + right mini chart + facts. |

## Team / meta

| Method | Signature | One-liner |
|---|---|---|
| `meet_the_team` | `title, members, source=''` | #33 Meet the team — profile cards in a row. |
| `case_study` | `title, sections, result_box=None, source=''` | #34 Case study — S/A/R or custom sections. |
| `two_column_text` | `title, columns, source=''` | #27 Two-column text — at most one slide of this type globally. |
| `four_column` | `title, items, source=''` | #28 Four-column overview — exactly 4 vertical cards. |

## Retired (kept for back-compat — do not use in new decks)

| Method | Replacement |
|---|---|
| `venn` | Express the overlap in `executive_summary` items or a `matrix_2x2`. |
| `cycle` | `process_chevron` + closing return arrow described in `summary` text. |
| `funnel` | `horizontal_bar` with descending values. |
| `pie` | `donut` (with optional `center_label`) is strictly better. |
| `gauge` | `big_number` + KPI bullet, or `kpi_tracker` for multiple gauges. |

## Engine plumbing

| Method | Purpose |
|---|---|
| `ExecEngine(total_slides=N)` | Constructor — sets the page-number denominator. |
| `eng.save(outpath)` | Finalize, run `full_cleanup()` for file-integrity, write `.pptx`. |

## Color constants (from `mbb_ppt.constants`)

- Primary: `PRIMARY` (=`NAVY` alias) — forest green `#1B4332`
- Neutrals: `WHITE`, `BLACK`, `DARK_GRAY`, `MED_GRAY`, `LINE_GRAY`, `BG_GRAY`, `SECTION_BG`, `HEADING_ACCENT`
- Accents: `ACCENT_BLUE` (slate), `ACCENT_GREEN` (olive), `ACCENT_ORANGE` (rust), `ACCENT_RED` (burgundy)
- Light pairs: `LIGHT_BLUE`, `LIGHT_GREEN`, `LIGHT_ORANGE`, `LIGHT_RED` (use via `ACCENT_PAIRS`)
- Warm (optional): `WARM_NAVY`, `WARM_GOLD`, `WARM_STONE`

## Type contract reminders

- `four_column.items`: list of **3-tuples** `(num, title, desc)` — exactly 4.
- `executive_summary.items`: list of **3-tuples** `(num, title, desc)` — ≤ 4.
- `matrix_2x2.quadrants`: list of **3-tuples** `(label, bg_color, desc)` — exactly 4.
- `process_chevron.steps`: list of **3-tuples** `(label, title, desc)` — ≤ 5; label cannot contain `\n`.
- `donut.segments`: list of **3-tuples** `(percent, color, label)` — ≤ 6.
- `timeline.milestones`: list of **2-tuples** `(label, desc)` — last label ≤ 6 chars.

For the full machine-readable contract, see `references/layout-matrix.yaml` (this is what the S3 gate validates against).
