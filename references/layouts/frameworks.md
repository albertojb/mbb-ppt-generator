# Layouts — Frameworks and Matrices

> **Loaded on demand at S4 (Render).** Open this file when rendering `matrix_2x2`, `swot`, `temple`, `pyramid`, `stakeholder_map`, or `risk_matrix`. These layouts encode classical strategic frameworks visually; pick the one whose semantic shape matches your argument.
>
> Capacity in [`../layout-matrix.yaml`](../layout-matrix.yaml).

---

## `matrix_2x2`

Classic 2×2 quadrant grid. Use for any framework that splits items along two binary axes (priority/difficulty, BCG growth/share, importance/urgency).

### Signature

```python
eng.matrix_2x2(title, quadrants, axis_labels=None, source='', bottom_bar=None)
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `quadrants` | list of **exactly 4 × 3-tuples** `(label, bg_color, description)` | yes | label ≤ 15, desc ≤ 80 | Order: **top-left, top-right, bottom-left, bottom-right** (reading order). Background colors should usually be from the LIGHT_* palette (`LIGHT_BLUE`, `LIGHT_GREEN`, etc.). |
| `axis_labels` | tuple `(x_label, y_label)` or `None` | no | ≤ 25 each | Optional axis annotations rendered along the bottom and left edges. |
| `source` | str | data → yes | — | — |
| `bottom_bar` | tuple `(label, text)` or `None` | no | — | Optional gray summary bar at the slide bottom. |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Quick wins and strategic bets diverge in our portfolio       │
│ ─────────────────────────────────────────────────             │
│      ┌─────────────────────┐  ┌─────────────────────┐         │
│ Hi   │ Strategic bets      │  │ Win zone            │         │
│ value│ ─────────────────── │  │ ─────────────────── │         │
│  ↑   │ Premium expansion;  │  │ Channel growth;     │         │
│      │ requires $20M cap   │  │ adds 12% in EMEA    │         │
│      └─────────────────────┘  └─────────────────────┘         │
│      ┌─────────────────────┐  ┌─────────────────────┐         │
│      │ Defer / drop        │  │ Quick wins          │         │
│      │ ─────────────────── │  │ ─────────────────── │         │
│      │ Legacy products;    │  │ Pricing optimization│         │
│      │ low growth, high op │  │ on top SKUs         │         │
│      └─────────────────────┘  └─────────────────────┘         │
│         Low effort →                  High effort →           │
│                                                               │
│ Source: portfolio review, Q1 2026                       6/N   │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
from mbb_ppt.constants import LIGHT_BLUE, LIGHT_GREEN, LIGHT_ORANGE, LIGHT_RED

eng.matrix_2x2(
    title='Quick wins and strategic bets diverge in our portfolio',
    quadrants=[
        ('Strategic bets', LIGHT_BLUE,
         'Premium expansion; requires $20M capex but $80M NPV'),
        ('Win zone',       LIGHT_GREEN,
         'Channel growth; adds 12% in EMEA at low marginal cost'),
        ('Defer / drop',   LIGHT_RED,
         'Legacy products; low growth, high op cost — divest or sunset'),
        ('Quick wins',     LIGHT_ORANGE,
         'Pricing optimization on top SKUs; +3pp margin within Q2'),
    ],
    axis_labels=('Effort →', 'Value ↑'),
    source='Source: portfolio review, Q1 2026',
)
```

### Pitfalls

- **Wrong quadrant count or arity.** Exactly 4 quadrants, each a 3-tuple. The S3 gate enforces both. ([`gate_check_content.py`](../scripts/gate_check_content.py).)
- **Wrong reading order.** Top-left → top-right → bottom-left → bottom-right. The first quadrant is in the upper-left corner — usually the "high-priority high-effort" cell. Switching the order produces a logically incoherent matrix.
- **All quadrants the same color.** Defeats the visual signal. Use different `LIGHT_*` backgrounds for each quadrant or at least signal the focal one.
- **Description longer than 80 chars.** Wraps and crowds the cell. Keep cell descriptions short — one sentence each.

---

## `swot`

SWOT analysis — 2×2 colored grid for Strengths / Weaknesses / Opportunities / Threats.

### Signature

```python
eng.swot(title, quadrants, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `quadrants` | list of **4 × 4-tuples** `(label, accent_color, light_bg, points)` | yes | label ≤ 15, point ≤ 50 | `points` is `list[str]` of bullets, ≤ 4 per quadrant. Conventional ordering: Strengths (top-left), Weaknesses (top-right), Opportunities (bottom-left), Threats (bottom-right). |
| `source` | str | data → yes | — | — |

Each quadrant gets a colored top strip in `accent_color` and a light-tinted background in `light_bg` matching the SWOT color convention (green/blue for positive, orange/red for cautionary).

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ SWOT — internal advantages vs. external risks                │
│ ─────────────────────────────────────────────────             │
│ ┌──────────────────────────┐  ┌──────────────────────────┐    │
│ │ ▌Strengths               │  │ ▌Weaknesses              │    │
│ │ • Premium brand recall   │  │ • Service capacity gaps  │    │
│ │ • Engineering bench      │  │ • Channel mix imbalance  │    │
│ │ • Recurring revenue mix  │  │ • Pricing inconsistency  │    │
│ └──────────────────────────┘  └──────────────────────────┘    │
│ ┌──────────────────────────┐  ┌──────────────────────────┐    │
│ │ ▌Opportunities           │  │ ▌Threats                 │    │
│ │ • EMEA distribution      │  │ • Low-cost entrants      │    │
│ │ • Premium tier expansion │  │ • Regulatory shift Q3    │    │
│ │ • API ecosystem          │  │ • Talent flight risk     │    │
│ └──────────────────────────┘  └──────────────────────────┘    │
│                                                               │
│ Source: strategy team                                    7/N  │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
from mbb_ppt.constants import (
    ACCENT_GREEN, LIGHT_GREEN, ACCENT_ORANGE, LIGHT_ORANGE,
    ACCENT_BLUE,  LIGHT_BLUE,  ACCENT_RED,    LIGHT_RED,
)

eng.swot(
    title='SWOT — internal advantages vs. external risks',
    quadrants=[
        ('Strengths',     ACCENT_GREEN,  LIGHT_GREEN,
         ['Premium brand recall', 'Engineering bench', 'Recurring revenue mix']),
        ('Weaknesses',    ACCENT_ORANGE, LIGHT_ORANGE,
         ['Service capacity gaps', 'Channel mix imbalance', 'Pricing inconsistency']),
        ('Opportunities', ACCENT_BLUE,   LIGHT_BLUE,
         ['EMEA distribution', 'Premium tier expansion', 'API ecosystem']),
        ('Threats',       ACCENT_RED,    LIGHT_RED,
         ['Low-cost entrants', 'Regulatory shift Q3', 'Talent flight risk']),
    ],
    source='Source: strategy team',
)
```

### Pitfalls

- **4-tuples, not 3.** Easy to confuse with `matrix_2x2`'s 3-tuples.
- **Imbalanced bullet counts.** A SWOT with 1 strength and 6 threats reads as defensive. Aim for 3–4 in each quadrant.
- **Point text too long.** > 50 chars wraps; the small cells crowd. Keep each point short — noun phrase + 2–3 word qualifier.
- **Wrong color convention.** Strengths and Opportunities should read as positive (green / blue); Weaknesses and Threats as cautionary (orange / red). Reversing this confuses the audience.

---

## `temple`

Temple / House framework — roof text on top, vertical pillars in the middle, foundation text on bottom. Use for "X supports Y on top of Z" structures (vision / pillars / foundation, mission / capabilities / values, etc.).

### Signature

```python
eng.temple(title, roof_text, pillar_names, foundation_text,
           pillar_colors=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `roof_text` | str | yes | ≤ 60 | The top-band statement. Usually the vision / mission / governing thought. White on navy. |
| `pillar_names` | list[str] | yes | each ≤ 20 | 3–5 pillars; each is a vertical column with a colored top accent and the name below it. |
| `foundation_text` | str | yes | ≤ 60 | The bottom-band statement — what the pillars rest on. White on navy. |
| `pillar_colors` | list[RGBColor] or `None` | no | — | One color per pillar. If `None`, all pillars get NAVY (modern v2.3.3 default). |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Three pillars support the FY26 strategic ambition            │
│ ─────────────────────────────────────────────────             │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│ ┃ Become the #1 premium provider in EMEA by FY28           ┃ ← roof
│ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│ │              │ │              │ │              │            │
│ │   Premium    │ │   Channel    │ │  Operating   │            │
│ │     mix      │ │   reach      │ │  excellence  │            │
│ │              │ │              │ │              │            │
│ └──────────────┘ └──────────────┘ └──────────────┘            │
│                                                               │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │
│ ┃ Talent + technology + culture as the foundation         ┃ ← foundation
│ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │
│ Source: FY26 strategy                                    8/N  │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.temple(
    title='Three pillars support the FY26 strategic ambition',
    roof_text='Become the #1 premium provider in EMEA by FY28',
    pillar_names=['Premium mix', 'Channel reach', 'Operating excellence'],
    foundation_text='Talent + technology + culture as the foundation',
    source='Source: FY26 strategy',
)
```

### Pitfalls

- **More than 5 pillars.** Pillars compress horizontally; names start wrapping. 3 is the visual sweet spot, 4 acceptable, 5 the maximum.
- **Roof or foundation too long.** > 60 chars wraps and the band looks crammed. Trim or restructure.
- **Generic pillar names.** "People", "Process", "Technology" is a tired triad — challenge whether your three pillars are really distinct strategic levers, not the consultant default.

---

## `pyramid`

Staircase / evolution layout — ascending steps, each with a label, description, and optional icon. Originally designed for civilization / capability evolution narratives; works well for any "stage 1 → stage 2 → stage 3" progression.

### Signature

```python
eng.pyramid(title, levels, source='', bottom_bar=None,
            detail_rows=None, detail_headers=None)
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | Can be narrative-style (longer than typical action title). |
| `levels` | list of **3-tuples** `(label, description, icon)` | yes | label ≤ 20, desc ≤ 60 | 3–5 levels. `icon` is one of: a PNG file path (transparent background, white strokes recommended); a Unicode glyph (`'⚙'`, `'1'`, `'A'`); empty / `None` for auto-numbering. |
| `source` | str | data → yes | — | — |
| `bottom_bar` | tuple or `None` | no | — | Rare for `pyramid`. |
| `detail_rows` | list of `(row_label, [cell1, cell2, …])` or `None` | no | — | Optional structured detail table below the staircase. Cells are str or list[str]; multi-element list cells render as bullets. |
| `detail_headers` | list[str] or `None` | no | — | Optional headers for the detail table. |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ The journey from product company to platform              ← title│
│ ─────────────────────────────────────────────────             │
│                                                          ┌──┐ │
│                                                          │④ │ │
│                                                          │PL│ │
│                                              ┌──┐  ┌──── ┘──┘ │
│                                    ┌──┐      │③ │  │            │
│                                    │② │      │EC│  │            │
│                          ┌──┐      │MK│      │OS│  │            │
│                ┌──┐      │① │      │PL│      │YS│  │            │
│                │📦│      │PR│      │AC│      │TE│  │            │
│                │PR│      │OD│      │E │      │M │  │            │
│                │OD│      │  │      │  │      │  │  │            │
│                └──┘      └──┘      └──┘      └──┘   ← steps    │
│                                                                │
│ Stage 1 — Product. Stage 2 — Marketplace. Stage 3 — Ecosystem. │
│ Stage 4 — Platform.                                            │
│                                                                │
│ Source: strategy framework                                10/N │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.pyramid(
    title='The journey from product company to platform',
    levels=[
        ('Stage 1',   'Product company — sell single SKUs', '1'),
        ('Stage 2',   'Marketplace — bundle 3rd-party SKUs', '2'),
        ('Stage 3',   'Ecosystem — partners build on our APIs', '3'),
        ('Stage 4',   'Platform — partners depend on our infra', '4'),
    ],
    source='Source: strategy framework',
)
```

### Pitfalls

- **More than 5 levels.** Steps shrink below readable. Cap at 5; 4 is the visual sweet spot.
- **PNG icons not transparent.** A non-transparent icon shows a square box around the glyph. Use 200×200px PNG with transparent background and white strokes (~6px) for best fit on the navy circle.
- **`detail_rows` cell mixing single-line and multi-line.** Single-line cells render as plain text; lists with 2+ items get auto-bulleted. If you want bullets for one-item cells, pass `['only item']` as a list rather than just `'only item'` as a string.

---

## `stakeholder_map`

2×2 stakeholder grid (typically Influence × Interest), with each quadrant listing the stakeholder names that fall in it. Use for stakeholder analysis at the start of a change-management or comms-planning section.

### Signature

```python
eng.stakeholder_map(title, quadrants, x_label='Influence →',
                    y_label='Interest ↑', summary=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `quadrants` | list of **4 × 4-tuples** `(label_main, label_sub, bg_color, members)` | yes | labels ≤ 15 each, member name ≤ 30 | Quadrants in reading order (TL, TR, BL, BR). The first two strings are concatenated as `'{main} ({sub})'` for the quadrant header. `members` is `list[str]` of stakeholder names. The historical parameter name `label_cn`/`label_en` (now both English) reflects an earlier bilingual design — pass any two labels you want concatenated. |
| `x_label` | str | no | ≤ 25 | x-axis label, default `'Influence →'`. |
| `y_label` | str | no | ≤ 25 | y-axis label, default `'Interest ↑'`. |
| `summary` | str | no | ≤ 80 | Optional bottom summary bar. |
| `source` | str | data → yes | — | — |

### Example

```python
from mbb_ppt.constants import LIGHT_RED, LIGHT_BLUE, LIGHT_GREEN, LIGHT_ORANGE

eng.stakeholder_map(
    title='Stakeholder map for the FY26 reorg announcement',
    quadrants=[
        ('Manage closely', 'high inf, high int', LIGHT_RED,
         ['CEO', 'CFO', 'COO']),
        ('Keep informed',  'high inf, low int',  LIGHT_BLUE,
         ['Board chair']),
        ('Keep satisfied', 'low inf, high int',  LIGHT_GREEN,
         ['VP Engineering', 'VP Sales', 'VP HR']),
        ('Monitor',        'low inf, low int',   LIGHT_ORANGE,
         ['Finance team', 'Legal team']),
    ],
    summary='Closing alignment with manage-closely group is the gating step.',
    source='Source: change management workshop',
)
```

### Pitfalls

- **4-tuples, not 3.** The two-label structure is a vestige of the upstream bilingual design. Pass two English labels if you want both shown; pass the same string twice if you only have one label per quadrant.
- **Too many members per quadrant.** Each quadrant fits ~4 names before the list pushes past the cell. If you have more, group by team or aggregate.
- **Wrong quadrant order.** Reading order: top-left, top-right, bottom-left, bottom-right. The conventional Mendelow placement is "Manage closely" in the high-influence + high-interest corner (top-left in this layout's coordinate system).

---

## `risk_matrix`

3×3 risk heat map. Each cell has a background color (`grid_lights`) and a marker dot color (`grid_colors`). Risks are placed by `(row, col)` coordinates with their names rendered inside the cell.

### Signature

```python
eng.risk_matrix(title, grid_colors, grid_lights, risks,
                y_labels=None, x_labels=None, notes=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `grid_colors` | 3×3 `list[list[RGBColor]]` | yes | — | Marker dot color for each cell. Convention: green for low / yellow for medium / red for high risk cells. |
| `grid_lights` | 3×3 `list[list[RGBColor]]` | yes | — | Cell background color. Usually a lighter version of `grid_colors`. |
| `risks` | list of `(row, col, name)` 3-tuples | yes | name ≤ 28 | Each risk is placed in cell `(row, col)`. Multiple risks per cell allowed (they stack). |
| `y_labels` | list[str] or `None` | no | ≤ 18 each | Default `['High probability', 'Medium probability', 'Low probability']`. Top to bottom. |
| `x_labels` | list[str] or `None` | no | ≤ 14 each | Default `['Low impact', 'Medium impact', 'High impact']`. Left to right. |
| `notes` | list[str] or `None` | no | — | Optional bullet list in a `'Response'` panel below the matrix. |
| `source` | str | data → yes | — | — |

### Example

```python
from mbb_ppt.constants import ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED, LIGHT_GREEN, LIGHT_ORANGE, LIGHT_RED

# 3x3: row 0 = high probability (top), row 2 = low (bottom)
#      col 0 = low impact (left), col 2 = high impact (right)
greens  = [LIGHT_GREEN]  * 3
oranges = [LIGHT_ORANGE] * 3
reds    = [LIGHT_RED]    * 3

eng.risk_matrix(
    title='Top risks for the FY26 plan',
    grid_lights=[
        [LIGHT_ORANGE, LIGHT_RED,    LIGHT_RED],
        [LIGHT_GREEN,  LIGHT_ORANGE, LIGHT_RED],
        [LIGHT_GREEN,  LIGHT_GREEN,  LIGHT_ORANGE],
    ],
    grid_colors=[
        [ACCENT_ORANGE, ACCENT_RED,    ACCENT_RED],
        [ACCENT_GREEN,  ACCENT_ORANGE, ACCENT_RED],
        [ACCENT_GREEN,  ACCENT_GREEN,  ACCENT_ORANGE],
    ],
    risks=[
        (0, 2, 'Regulatory shift'),
        (1, 1, 'Talent flight'),
        (2, 0, 'Vendor renewal'),
    ],
    notes=[
        '• Regulatory: file pre-emptive whitepaper Q2.',
        '• Talent: retention bonuses for top 20% engineers.',
        '• Vendor: lock 3-year deal at FY25 prices.',
    ],
    source='Source: risk register, Q1 2026',
)
```

### Pitfalls

- **Grid arrays with wrong shape.** Both `grid_colors` and `grid_lights` must be exactly 3×3. Anything else raises an `IndexError` mid-render.
- **Risk row/col out of bounds.** `row` and `col` must be 0–2. Off-grid risks render outside the cells.
- **Forgetting to pair colors and lights.** A red marker on a green background reads as a contradiction. Pair them: light red background + accent red marker.
- **Too many risks per cell.** Names stack vertically inside the cell. 1–2 per cell is comfortable; 3+ overflows. If a cell has 3+ risks, summarize them as a single category.

---

## Cross-references

- **Method index:** [`../framework/engine-api.md`](../framework/engine-api.md).
- **Capacity matrix:** [`../layout-matrix.yaml`](../layout-matrix.yaml).
- **When to use a matrix vs. a list:** [`../framework/planning-guide.md`](../framework/planning-guide.md) § 3.
- **Past defects in these layouts:** [`../../experiences/`](../../experiences/).
