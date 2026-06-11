# Layouts — Dashboards

> **Loaded on demand at S4 (Render).** Open this file when rendering `dashboard_kpi_chart` or `dashboard_table_chart`. These layouts compress multiple analytical views onto one slide; use them sparingly — typically as a section opener or a "state of the business" summary.
>
> Capacity in [`../api-schemas.yaml`](../api-schemas.yaml).

---

## `dashboard_kpi_chart`

Top row of KPI cards + middle bar-chart panel + bottom summary bar. Use when the audience needs to see a few headline metrics alongside a single supporting trend.

### Signature

```python
eng.dashboard_kpi_chart(title, kpi_cards, chart_data=None,
                        summary=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `kpi_cards` | list of **4-tuples** `(value, label, detail, accent_color)` | yes | value ≤ 8, label ≤ 16, detail ≤ 25 | 3–5 cards. Each card has a colored top accent, large value in `HEADING_FONT`, label, and a green-toned detail (typically a delta vs. plan / prior). |
| `chart_data` | dict or `None` | no | — | Bar chart in the middle band. Keys: `'labels'` (x-axis), `'actual'` (list of values), `'target'` (list of values), `'max_val'` (optional cap, default `max(actual+target) × 1.15`), `'legend'` (optional list of `(name, color)`, default `[('Actual', NAVY), ('Target', BG_GRAY)]`). |
| `summary` | str or list[str] | no | each line ≤ 80 | Bottom-bar takeaway. Single string or list[str] for multi-line. The label is fixed to `'Key findings'`. |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Q4 dashboard — three of four KPIs ahead of plan               │
│ ─────────────────────────────────────────────────             │
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐                   │
│ │■━━━━━━━│ │■━━━━━━━│ │■━━━━━━━│ │■━━━━━━━│                   │
│ │ $1.24B │ │ 31%    │ │ +8     │ │ -57%   │                   │
│ │ Revenue│ │ Margin │ │ NPS pts│ │ TTR    │                   │
│ │ +24%   │ │ +7pp   │ │ +2.2   │ │ vs Q1  │                   │
│ └────────┘ └────────┘ └────────┘ └────────┘                   │
│                                                               │
│ Actuals vs. target — by quarter                ■ Actual ■ Targ│
│ ────────────────────────────────                              │
│  Q1    ▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆░░░░░░░░░                              │
│  Q2    ▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆░░░░░░░                               │
│  Q3    ▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆░░░                                │
│  Q4    ▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆▆░                                │
│                                                               │
│ ┌──────────────────────────────────────────────────────────┐  │
│ │ Key findings  All KPIs ahead of plan; TTR improvement is │  │
│ │               the largest delta vs. Q1 baseline.         │  │
│ └──────────────────────────────────────────────────────────┘  │
│ Source: company financials                              12/N  │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
from mbb_ppt.constants import NAVY, ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, BG_GRAY

eng.dashboard_kpi_chart(
    title='Q4 dashboard — three of four KPIs ahead of plan',
    kpi_cards=[
        ('$1.24B', 'Revenue',   '+24% vs plan',   NAVY),
        ('31%',    'Margin',    '+7pp vs plan',   ACCENT_BLUE),
        ('+8',     'NPS pts',   '+2.2 vs Q1',     ACCENT_GREEN),
        ('-57%',   'Time-to-resolve', 'vs Q1',    ACCENT_ORANGE),
    ],
    chart_data={
        'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
        'actual': [220, 240, 285, 310],
        'target': [250, 250, 250, 280],
        'max_val': 350,
        'legend': [('Actual', NAVY), ('Target', BG_GRAY)],
    },
    summary='All KPIs ahead of plan; TTR improvement is the largest delta vs. Q1 baseline.',
    source='Source: company financials',
)
```

### Pitfalls

- **Tuple arity.** KPI cards are 4-tuples (value, label, detail, color). 3-tuples raise `ValueError`.
- **`chart_data` keys missing.** If `chart_data` is provided, `'labels'`, `'actual'`, and `'target'` are all expected. Missing keys default to empty lists and the chart renders blank.
- **Cards and chart telling different stories.** The KPI cards and the chart should reinforce each other. If cards say "+24% revenue growth" and the chart shows a flat trend, the slide is internally inconsistent.
- **Confusing with `kpi_tracker`.** `kpi_tracker` is for OKR-style progress bars with status. `dashboard_kpi_chart` is for big-number cards + a supporting chart. Different visual register, different use cases.

---

## `dashboard_table_chart`

Left column data table + right column mini bar chart + bottom row of factoid cards. Use for portfolio / regional dashboards where a table and a comparison chart are both needed alongside a few headline facts.

### Signature

```python
eng.dashboard_table_chart(title, table_data, chart_data=None,
                          factoids=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `table_data` | dict | yes | — | Left-side table. Keys: `'headers'` (list[str]), `'col_widths'` (list[Inches]), `'rows'` (list of lists of str values, each row matching headers). 4–6 rows recommended. **The third column auto-greens any value containing `+`** (the engine assumes col 2 is a delta column). |
| `chart_data` | dict or `None` | no | — | Right-side mini bar chart. Keys: `'title'` (str), `'items'` (list of `(name, value)` 2-tuples). |
| `factoids` | list of **3-tuples** `(value, label, accent_color)` | no | value ≤ 8, label ≤ 18 | Bottom row of fact cards. 3–4 factoids. Each gets a colored vertical strip and a colored value. |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Regional performance — APAC led, EMEA recovered               │
│ ─────────────────────────────────────────────────             │
│ REGION    REVENUE   YOY                  Top growth markets   │
│ ─────────────────────                    ─────────────────    │
│ NA        $480M     +8%                   APAC ▆▆▆▆▆▆▆▆▆▆▆    │
│ ─────────────────────                     LATAM ▆▆▆▆▆▆▆▆      │
│ EMEA      $320M     +12%                  EMEA ▆▆▆▆▆▆▆▆       │
│ ─────────────────────                     NA   ▆▆▆▆▆          │
│ APAC      $280M     +18%                                       │
│ ─────────────────────                                          │
│ LATAM     $160M     +14%                                       │
│                                                                │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│ │ ▎+13%    │ │ ▎+22%    │ │ ▎18%     │ │ ▎4 of 4  │           │
│ │ Blended  │ │ APAC     │ │ Premium  │ │ regions  │           │
│ │ growth   │ │ standout │ │ share    │ │ ahead    │           │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│ Source: regional finance                               13/N   │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
from pptx.util import Inches
from mbb_ppt.constants import NAVY, ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE

eng.dashboard_table_chart(
    title='Regional performance — APAC led, EMEA recovered',
    table_data={
        'headers':    ['Region', 'Revenue', 'YoY'],
        'col_widths': [Inches(1.6), Inches(2.0), Inches(2.6)],
        'rows': [
            ['NA',    '$480M', '+8%'],
            ['EMEA',  '$320M', '+12%'],
            ['APAC',  '$280M', '+18%'],
            ['LATAM', '$160M', '+14%'],
        ],
    },
    chart_data={
        'title': 'Top growth markets',
        'items': [
            ('APAC',  18),
            ('LATAM', 14),
            ('EMEA',  12),
            ('NA',     8),
        ],
    },
    factoids=[
        ('+13%',    'Blended growth',  NAVY),
        ('+22%',    'APAC standout',   ACCENT_GREEN),
        ('18%',     'Premium share',   ACCENT_BLUE),
        ('4 of 4',  'regions ahead',   ACCENT_ORANGE),
    ],
    source='Source: regional finance',
)
```

### Pitfalls

- **Table column count mismatch.** Each row's length must equal `len(headers)`. Validate before passing.
- **Chart items > ~6.** The mini chart on the right has limited vertical space; 4–5 items fit comfortably. More than 6 → bar labels collide.
- **Forgetting `factoids`.** Without the bottom factoid row, the slide feels half-finished — the bottom 1.5" of the slide goes empty. Either add factoids or use a different layout.
- **Putting the same data in the table and the chart.** Redundancy wastes the slide. The table shows multiple dimensions per row (Revenue + YoY); the chart should highlight a single dimension across the same items (or the *same* dimension viewed differently).

---

## When to use a dashboard layout vs. multiple slides

A dashboard layout compresses multiple views onto one slide. The cost: each view has less space. The benefit: the audience sees the relationships in one glance.

Use a dashboard layout when:

- You have ≥ 3 dimensions to show and they're all roughly equally important.
- The audience's question is "how is the business doing overall?", not "tell me about X".
- The slide is at the start of a section ("here's the snapshot") or near the end ("here's the consolidated view").

Use multiple slides instead when:

- One of the dimensions is the headline and the others are supporting (use `big_number` + supporting slides).
- The audience will dig into each dimension individually (give each one its own slide).
- You don't have data for all the dashboard cells (a dashboard with empty quadrants reads as half-built).

---

## Cross-references

- **Method index:** [`../framework/engine-api.md`](../framework/engine-api.md).
- **Capacity matrix:** [`../api-schemas.yaml`](../api-schemas.yaml).
- **When to break a dashboard into multiple slides:** [`../framework/planning-guide.md`](../framework/planning-guide.md) § 3.
