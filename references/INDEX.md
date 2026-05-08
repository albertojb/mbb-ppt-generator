# Knowledge Index — MBB PPT Generator

> Routing table for the model. Each stage of the five-stage workflow loads only the files in its row. Do not bulk-load.
>
> Adapted from Likaku's `Mck-ppt-design-skill v2.3.3-harness-v2`. Apache 2.0.

## Stage → Load Map

| Stage | Required reading | Optional reading |
|---|---|---|
| **S1 — Brief** | `references/team/brand-guide.md` | — |
| **S2 — Structure** | `references/api-cheatsheet.md`, `references/layout-matrix.yaml`, `references/framework/planning-guide.md` (§ 3 *Layout selection by task* and § 5 *Layout diversity / visual-density floor*) | `references/framework/engine-api.md`, per-layout files in `references/layouts/` when a specific layout's contract matters |
| **S3 — Content** | `references/framework/guard-rails.md`, every file in `experiences/` | — |
| **S4 — Render + QA** | only the `references/layouts/*.md` files for layouts actually used | `references/team/presentation-convention.md` for margin/source rules |
| **S5 — Deliver** | none | — |

The model **must read** the required files at the start of each stage. Do not carry context from S2 into S3 implicitly — re-read the S3 row.

## Directory layout

```
references/
├── INDEX.md                       # this file
├── api-cheatsheet.md              # one-page method index — load at S2 first
├── layout-matrix.yaml             # capacity matrix — single source of truth
│
├── team/                          # most stable layer (rarely changes)
│   ├── brand-guide.md             # color, font, design principles
│   └── presentation-convention.md # margins, mandatory elements, file delivery
│
├── framework/                     # framework layer (medium-frequency change)
│   ├── engine-api.md              # ExecEngine method quick reference
│   ├── guard-rails.md             # production rules 1–18
│   └── planning-guide.md          # layout selection logic, content density
│
├── layouts/                       # per-layout reference (load on demand)
│   ├── structure.md               # cover, toc, section_divider, closing
│   ├── data-stats.md              # big_number, two_stat, three_stat, ...
│   ├── frameworks.md              # matrix_2x2, table_insight, process_chevron, ...
│   ├── comparison.md              # side_by_side, before_after, pros_cons, ...
│   ├── narrative.md               # executive_summary, key_takeaway, quote, ...
│   ├── timeline.md                # timeline, vertical_steps, value_chain, ...
│   ├── charts-circular.md         # donut (BLOCK_ARC rules)
│   ├── charts-bar-line.md         # grouped_bar, stacked_bar, line_chart, ...
│   ├── charts-advanced.md         # waterfall, pareto, bubble, risk_matrix, ...
│   ├── dashboards.md              # dashboard_kpi, dashboard_table
│   ├── images.md                  # content_right_image, three_images, ...
│   └── special.md                 # stakeholder_map, decision_tree, icon_grid, swot
│
├── color-palette.md               # quick reference (legacy, kept for browsing)
├── layout-catalog.md              # 72-layout index (legacy, kept for browsing)
│
└── scripts/                       # gate scripts — machine-readable, not AI-evaluated
    ├── gate_check_content.py      # S3 gate: API format, count limits, source, title
    └── gate_check_render.py       # S4 gate: post-render QA, with engine_bug whitelist

experiences/                       # Self-Refinement persistence (append-only)
├── overflow.md
├── layout-pitfalls.md
└── chart-limits.md
```

## Quick load cheatsheet

| Situation | Load |
|---|---|
| Cover-only deck | `team/brand-guide.md` only |
| Full 10+ slide deck | S2 → `engine-api.md` + `layout-matrix.yaml`; S3 → `guard-rails.md` + `experiences/`; S4 → only the `layouts/*.md` you actually use |
| Has charts | S4 also load `layouts/charts-*.md` for the chart types in play |
| Same topic ran into errors before | S3 always re-read `experiences/` — that is where past fixes live |
