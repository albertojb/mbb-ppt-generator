# Layouts — Bar and Line Charts

> **Loaded on demand at S4 (Render).** Open this file when rendering `grouped_bar`, `stacked_bar`, `horizontal_bar`, or `line_chart`.
>
> All four use pure rectangle drawing (no `python-pptx` chart objects), keeping the file lightweight and the visual style consistent with the rest of the deck. None of these support an action title >~ 60 characters before wrap; aim short.

---

## `grouped_bar`

Vertical bars grouped by category, multiple series side-by-side per group. Use for time-series or category comparisons across 2–3 series.

### Signature

```python
eng.grouped_bar(title, categories, series, data, max_val=None,
                y_ticks=None, summary=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 60 (chart layouts wrap badly above 60) | Conclusion-led. |
| `categories` | list[str] | yes | ≤ 8 chars per category label | x-axis labels. **Max 6 categories.** |
| `series` | list of 2-tuples `(name, color)` | yes | name ≤ 15 | **Max 3 series.** Beyond 3, bars get too narrow. |
| `data` | list[list[int]] | yes | — | Outer index = category, inner = series. `data[cat_idx][series_idx]`. Lengths must match `categories` and `series`. |
| `max_val` | int/float or `None` | no | — | Y-axis maximum. If `None`, engine computes `max(data) * 1.15`. Pass explicitly when comparing across slides for visual consistency. |
| `y_ticks` | list[int] or `None` | no | — | Optional y-axis tick values. If passed, engine renders gridlines and tick labels. |
| `summary` | tuple `(label, text)` or `None` | no | label ≤ 15, text ≤ 80 | Bottom gray bar with bold label + description. |
| `source` | str | yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Premium and partner channels lead growth              ← title│
│ ─────────────────────────────────────────────────            │
│  Premium and partner channels lead growth   ■ Premium ■ Partner
│                                                              │
│  200 ┤                                            ▆          │
│  150 ┤                       ▆                    ▆▆         │
│  100 ┤      ▆       ▆        ▆▆       ▆▆          ▆▆         │
│   50 ┤      ▆▆      ▆▆       ▆▆       ▆▆          ▆▆         │
│    0 ┤_____▆▆______▆▆_______▆▆_______▆▆__________▆▆__       │
│         Q1        Q2        Q3        Q4          Q5         │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ CAGR    +14% blended over period.                        │ │
│ └──────────────────────────────────────────────────────────┘ │
│ Source: finance team                                     5/N │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
from mbb_ppt.constants import NAVY, ACCENT_BLUE

eng.grouped_bar(
    title='Premium and partner channels lead growth',
    categories=['Q1', 'Q2', 'Q3', 'Q4'],
    series=[('Premium', NAVY), ('Partner', ACCENT_BLUE)],
    data=[
        [120,  80],
        [145,  95],
        [160, 110],
        [180, 130],
    ],
    max_val=200,
    y_ticks=[0, 50, 100, 150, 200],
    summary=('CAGR', '+14% blended over period.'),
    source='Source: finance team',
)
```

### Pitfalls

- **Too many categories or series.** > 6 categories or > 3 series → bar widths go negative or labels overlap. Hard caps. ([`experiences/chart-limits.md` Experience 002](../../experiences/chart-limits.md).)
- **Inconsistent `max_val` across slides.** If two grouped bars on adjacent slides have different `max_val`, the audience can't compare bar heights visually. Lock `max_val` deck-wide for any series comparison.
- **Numeric labels under 50.** The engine omits the in-bar value label for values < 50 (to avoid crowding short bars). If your data is in the 0–50 range, multiply your unit (e.g. show in hundreds of thousands instead of millions) so values land above 50.
- **Series in the wrong color order.** The first series renders behind / left of the second within each group. Put the *focal* series first (`NAVY`); put comparison series in accent colors.

---

## `stacked_bar`

100% stacked vertical bars showing composition over time. Use for share-of-total trends — the bar always sums to 100%.

### Signature

```python
eng.stacked_bar(title, periods, series, data, summary=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 60 | — |
| `periods` | list[str] | yes | ≤ 8 chars each | x-axis labels (Q1, FY24, etc.). **Max 6 periods.** |
| `series` | list of 2-tuples `(name, color)` | yes | name ≤ 15 | **Max 5 series** (the segments that stack within each bar). |
| `data` | list[list[int]] | yes | values are percentages | `data[period_idx][series_idx]`. Each row should sum to 100. |
| `summary` | tuple `(label, text)` or `None` | no | — | Optional bottom summary bar. |
| `source` | str | yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Premium share rose from 30% to 47% in three quarters  ← title│
│ ─────────────────────────────────────────────────            │
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                              │
│ │ ███ │ │ ███ │ │ ███ │ │ ███ │  ■ Entry                     │
│ │ ███ │ │ ▓▓▓ │ │ ▒▒▒ │ │ ░░░ │  ■ Standard                  │
│ │ ▓▓▓ │ │ ▒▒▒ │ │ ░░░ │ │ ░░░ │  ■ Premium                   │
│ │ ▒▒▒ │ │ ░░░ │ │ ░░░ │ │ ░░░ │                              │
│ │ ░░░ │ │ ░░░ │ │ ░░░ │ │ ░░░ │                              │
│ └─────┘ └─────┘ └─────┘ └─────┘                              │
│   Q1      Q2      Q3      Q4                                 │
│                                                              │
│ Source: finance team                                     5/N │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
from mbb_ppt.constants import NAVY, ACCENT_BLUE, ACCENT_GREEN

eng.stacked_bar(
    title='Premium share rose from 30% to 47% in three quarters',
    periods=['Q1', 'Q2', 'Q3', 'Q4'],
    series=[
        ('Premium',  NAVY),
        ('Standard', ACCENT_BLUE),
        ('Entry',    ACCENT_GREEN),
    ],
    data=[
        [30, 50, 20],   # Q1: 30% premium, 50% std, 20% entry — sums to 100
        [37, 47, 16],
        [42, 45, 13],
        [47, 42, 11],
    ],
    summary=('Mix shift', 'Premium gained 17pp; entry tier compressed.'),
    source='Source: finance team',
)
```

### Pitfalls

- **Rows that don't sum to 100.** The bar still renders but has visible whitespace at the top. Validate before passing.
- **Too many series.** > 5 → segments become hairline thin and unreadable. Cap at 5 (the matrix sets this); below 4 is comfortable.
- **Stacked bar when grouped bar would be clearer.** If the audience cares about absolute values per series, use `grouped_bar`. Use `stacked_bar` only when the focus is *share*.

---

## `horizontal_bar`

Labeled horizontal bars with percentage values. Use for ranking — categories listed top-to-bottom in descending order, with bars showing share or percentage.

### Signature

```python
eng.horizontal_bar(title, items, summary=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 60 | — |
| `items` | list of **3-tuples** `(name, pct_int_0_to_100, bar_color)` | yes | name ≤ 20 | Up to **8 items**. Order matters — list in the order you want them displayed (typically descending). The **first item** is automatically rendered in bold navy text to signal "the takeaway"; pass the focal item first. |
| `summary` | tuple `(label, text)` or `None` | no | — | Bottom gray summary bar. |
| `source` | str | yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Service quality is the top driver of customer retention      │
│ ─────────────────────────────────────────────────            │
│  Service quality       │██████████████████████│  74%         │ ← navy bold (first item)
│ ─────────────────────────────────────────────────            │
│  Product breadth       │█████████████░░░░░░░░░│  52%         │
│ ─────────────────────────────────────────────────            │
│  Pricing               │██████████░░░░░░░░░░░░│  41%         │
│ ─────────────────────────────────────────────────            │
│  Brand reputation      │████████░░░░░░░░░░░░░░│  33%         │
│ ─────────────────────────────────────────────────            │
│  Distribution speed    │██████░░░░░░░░░░░░░░░░│  24%         │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Implication  Service investment yields ~3× the lift of   │ │
│ │              equivalent pricing changes.                 │ │
│ └──────────────────────────────────────────────────────────┘ │
│ Source: customer survey, n=2,400                         5/N │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
from mbb_ppt.constants import NAVY, ACCENT_BLUE, MED_GRAY

eng.horizontal_bar(
    title='Service quality is the top driver of customer retention',
    items=[
        ('Service quality',    74, NAVY),
        ('Product breadth',    52, ACCENT_BLUE),
        ('Pricing',            41, MED_GRAY),
        ('Brand reputation',   33, MED_GRAY),
        ('Distribution speed', 24, MED_GRAY),
    ],
    summary=('Implication',
             'Service investment yields ~3× the lift of equivalent pricing changes.'),
    source='Source: customer survey, n=2,400',
)
```

### Pitfalls

- **Wrong tuple arity.** 3-tuples required: `(name, pct, color)`.
- **Sorting in the wrong order.** Items render top-to-bottom in the order passed. For a "ranking" message, pass in descending order. For a "categories alphabetical" message, pass alphabetically — but the first item still gets the navy emphasis, so make sure the first item is the focal one.
- **More than 8 items.** Rows compress vertically. Cap at 8.
- **Percentages over 100.** The engine assumes 0–100; passing 120 truncates the bar at 100% width. Reformat as an index (100 = baseline) and explain in the title.

---

## `line_chart`

Single-line trend chart with axis labels and gridlines. **Single series only** — for multi-series time trends, use `grouped_bar` or build via `multi_bar_panel`.

### Signature

```python
eng.line_chart(title, x_labels, y_labels, values,
               legend_label='', summary=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 60 | — |
| `x_labels` | list[str] | yes | short | x-axis tick labels. Up to **12 points**. |
| `y_labels` | list[str] | yes | short | y-axis tick labels. Top-down order: `['100', '75', '50', '25', '0']`. |
| `values` | list[float] | yes | each value 0.0–1.0 | **Caller-normalized.** The engine plots values as a fraction of chart height — so `0.0` = bottom of chart, `1.0` = top. You compute the normalization. (See pitfalls.) Length must equal `len(x_labels)`. |
| `legend_label` | str | no | ≤ 20 chars | Optional single-series label shown next to a navy swatch. |
| `summary` | str (not a tuple) | no | ≤ 80 chars | A *string*, not a `(label, text)` tuple — different from grouped_bar. |
| `source` | str | yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Revenue compounded at 14% over the past four years    ← title│
│ ─────────────────────────────────────────────────            │
│  Revenue trend                              ■ Revenue        │
│                                                              │
│ 100 ┤                                              ●         │
│  75 ┤                                       ●─────╱          │
│  50 ┤                              ●───────╱                 │
│  25 ┤                  ●──────────╱                          │
│   0 ┤    ●────────────╱                                      │
│      ────┴──────┴──────┴──────┴──────┴───────┴───────        │
│       FY21    FY22    FY23    FY24    FY25    FY26           │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ CAGR 14% over the period.                                │ │
│ └──────────────────────────────────────────────────────────┘ │
│ Source: finance team                                     6/N │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
# Caller normalization: revenue values 100 → 200 → 320 → 480 → 640 → 850
# Pick max = 1000; divide by it for normalized 0–1 range
revenue = [100, 200, 320, 480, 640, 850]
max_v = 1000
normalized = [v / max_v for v in revenue]   # [0.10, 0.20, 0.32, 0.48, 0.64, 0.85]

eng.line_chart(
    title='Revenue compounded at 14% over the past four years',
    x_labels=['FY21', 'FY22', 'FY23', 'FY24', 'FY25', 'FY26'],
    y_labels=['$1.0B', '$0.75B', '$0.5B', '$0.25B', '$0'],
    values=normalized,
    legend_label='Revenue',
    summary='CAGR 14% over the period.',
    source='Source: finance team',
)
```

### Pitfalls

- **Forgetting to normalize.** This is the single most common error with `line_chart`. The engine plots values directly as a fraction of chart height — passing `[100, 200, 320, …]` produces an off-screen line. Always divide by your max to get 0.0–1.0.
- **Multi-series request.** `line_chart` is single-series. If you need multiple lines, use `grouped_bar` (better for discrete time periods) or split into multiple `line_chart` slides side-by-side. The engine doesn't currently render multi-series line charts.
- **`summary` as a tuple.** Unlike `grouped_bar` and `horizontal_bar`, `line_chart`'s `summary` is a plain string, not a `(label, text)` tuple. Passing a tuple raises a type error.
- **Too few x-points.** A 2-point line is just a slope; the audience expects a trend. Aim for 4+ points minimum.
- **y_labels in wrong order.** Top-down: highest at top, zero at bottom. The engine plots `y_labels[0]` at the top of the chart.

---

## Cross-references

- **Method index:** [`../framework/engine-api.md`](../framework/engine-api.md).
- **Capacity matrix:** [`../layout-matrix.yaml`](../layout-matrix.yaml).
- **Past chart-capacity issues:** [`../../experiences/chart-limits.md`](../../experiences/chart-limits.md).
- **Rule 4 (legend color consistency):** [`../framework/guard-rails.md`](../framework/guard-rails.md).
