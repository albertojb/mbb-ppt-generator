# Layouts — Advanced Charts

> **Loaded on demand at S4 (Render).** Open this file when rendering `waterfall`, `pareto`, `stacked_area`, `bubble`, `kpi_tracker`, or `multi_bar_panel`. These are the more visually complex chart layouts; each has specific data shape requirements that are easy to get wrong.
>
> Capacity in [`../layout-matrix.yaml`](../layout-matrix.yaml).

---

## `waterfall`

Bridge chart from a starting value through positive / negative deltas to an ending value. Use when explaining how one figure becomes another (revenue bridge, margin bridge, headcount bridge, etc.).

### Signature

```python
eng.waterfall(title, items, max_val=None, legend_items=None,
              summary=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 60 | — |
| `items` | list of **3-tuples** `(label, value, type)` | yes | label ≤ 12 chars | `type` ∈ `'base'`, `'up'`, `'down'`. Up to 8 items; structure is typically: one `'base'` start, several `'up'`/`'down'` deltas, one final `'base'` end (the "total" bar). |
| `max_val` | int/float or `None` | no | — | Y-axis max. If `None`, computed from data × 1.3 (extra headroom for value labels above bars). |
| `legend_items` | list of `(name, color)` or `None` | no | — | Optional legend showing what `'up'` (green) and `'down'` (red) mean in your context. |
| `summary` | str (not tuple) | no | ≤ 80 | Plain summary string at the bottom. |
| `source` | str | yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Three drivers explain Q4 revenue gain                  ← title│
│ ─────────────────────────────────────────────────             │
│  Revenue bridge — Q3 to Q4                ■ Increase ■ Decrease│
│                                                               │
│        +18                                                    │
│         ▲          +12                                        │
│         │           ▲          -5                             │
│  +120   │           │           ▼          +145               │
│  ┌──┐   ▲           │           ▲          ┌──┐               │
│  │██│   ▲           │           │          │██│               │
│  │██│ ┌─▲─┐ ──── ┌──▲──┐ ──── ┌─▼─┐  ──── │██│               │
│  │██│ │GG│       │GGGG│       │RR│        │██│               │
│  │██│ └──┘       └────┘       └──┘        │██│               │
│  └──┘                                     └──┘               │
│   Q3   Premium    Channel    Cost          Q4                 │
│  base  bundles   expansion   churn        base                │
│                                                               │
│ ┌──────────────────────────────────────────────────────────┐  │
│ │ Premium and channel together added $30M; cost churn     │  │
│ │ took back $5M.                                          │  │
│ └──────────────────────────────────────────────────────────┘  │
│ Source: finance team                                     6/N  │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
from mbb_ppt.constants import NAVY, ACCENT_GREEN, ACCENT_RED

eng.waterfall(
    title='Three drivers explain Q4 revenue gain',
    items=[
        ('Q3 base',         120, 'base'),
        ('Premium bundles',  18, 'up'),
        ('Channel exp.',     12, 'up'),
        ('Cost churn',       -5, 'down'),
        ('Q4 base',         145, 'base'),
    ],
    legend_items=[('Increase', ACCENT_GREEN), ('Decrease', ACCENT_RED)],
    summary='Premium and channel together added $30M; cost churn took back $5M.',
    source='Source: finance team',
)
```

### Pitfalls

- **`type` typo.** Must be exactly `'base'`, `'up'`, or `'down'`. Anything else is treated as `'down'` (the else-branch in the engine). Validate before passing.
- **Math doesn't reconcile.** If your `'base'` start + ups − downs ≠ your `'base'` end, the chart still renders but the audience will spot the error. Compute the math before passing the items list.
- **Negative values for `'up'` or positive for `'down'`.** The engine uses `abs(value)` for `'down'` and the literal value for `'up'`. Pass positive numbers for both — `type` carries the sign.

---

## `pareto`

Descending-bars Pareto chart — used to show which few items account for most of the total. Bars are ranked left to right, with absolute value labels on top and percentage-of-total labels below those.

### Signature

```python
eng.pareto(title, items, max_val=None, summary=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 60 | — |
| `items` | list of **2-tuples** `(label, value)` | yes | label ≤ 14 | Up to **8 items**. Pass in descending order — the engine does NOT auto-sort. |
| `max_val` | int/float or `None` | no | — | Y-axis max. If `None`, `max(values) * 1.15`. |
| `summary` | str | no | ≤ 80 | — |
| `source` | str | yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Two products account for 80% of returns                ← title│
│ ─────────────────────────────────────────────────             │
│                                                               │
│  4,200                                                        │
│  ──────                                                       │
│   53%                                                         │
│  ┌─▆─┐    2,100                                               │
│  │██│   ──────                                                │
│  │██│    27%       640      320      180     130              │
│  │██│   ┌─▆─┐    ──────   ──────   ──────  ──────             │
│  │██│   │██│      8%       4%       2%      2%                │
│  │██│   │██│    ┌─▆─┐    ┌─▆─┐    ┌─▆─┐  ┌─▆─┐                │
│  │██│   │██│    │██│      │██│      │██│   │██│                │
│  │██│   │██│    │██│      │██│      │██│   │██│                │
│  └──┘   └──┘    └──┘      └──┘      └──┘   └──┘                │
│  SKU-A  SKU-B   SKU-C    SKU-D     SKU-E   SKU-F              │
│                                                               │
│ ┌──────────────────────────────────────────────────────────┐  │
│ │ Top 2 SKUs drive 80% of returns; redesign focus is here. │  │
│ └──────────────────────────────────────────────────────────┘  │
│ Source: returns analysis FY25                            7/N  │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.pareto(
    title='Two products account for 80% of returns',
    items=[
        ('SKU-A', 4200),
        ('SKU-B', 2100),
        ('SKU-C',  640),
        ('SKU-D',  320),
        ('SKU-E',  180),
        ('SKU-F',  130),
    ],
    summary='Top 2 SKUs drive 80% of returns; redesign focus is here.',
    source='Source: returns analysis FY25',
)
```

### Pitfalls

- **Items not in descending order.** The engine renders in the order passed. A non-descending order looks broken visually and defeats the Pareto narrative. Sort before passing.
- **More than 8 items.** Bars become too narrow for the value labels. Cap at 8; aggregate the long tail into `'Other'`.
- **Pareto when ranking would do.** If the message is "rank these items" without a "few drive most" finding, use `horizontal_bar` (cleaner visual for ranking).

---

## `stacked_area`

Stacked column chart approximating an area chart. Use for cumulative composition over time when 3–4 series stack to a meaningful total.

### Signature

```python
eng.stacked_area(title, years, series_data, max_val=None,
                 summary=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 60 | — |
| `years` | list[str] | yes | short, e.g. `'FY24'` | x-axis labels. |
| `series_data` | list of 3-tuples `(name, values, color)` | yes | name ≤ 14 | `values` is a list[int], one per year. **Max 5 series.** |
| `max_val` | int/float or `None` | no | — | Y-axis max. If `None`, computed from row sums × 1.15. |
| `summary` | tuple `(label, text)` or `None` | no | — | Optional bottom summary bar. |
| `source` | str | yes | — | — |

The engine renders y-axis values and totals with a `$` currency prefix by default. The currency symbol is currently hardcoded; for non-USD decks, format your domain values in the units you want shown without expecting the currency to change.

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Total revenue grew $300M with mix shift to premium     ← title│
│ ─────────────────────────────────────────────────             │
│  Revenue mix — FY22 to FY26              ■ Premium ■ Std ■ Entry
│                                                               │
│  $1000 ┤                                          $850        │
│        │                                          ┌─░─┐       │
│   $750 ┤                          $640            │░░░│       │
│        │              $480        ┌─░─┐           │░░░│       │
│   $500 ┤   $320       ┌─░─┐       │░░░│           │▒▒▒│       │
│        │   ┌─░─┐      │░░░│       │░░░│           │▒▒▒│       │
│   $250 ┤   │░░░│      │▒▒▒│       │▒▒▒│           │███│       │
│        │   │▒▒▒│      │▒▒▒│       │███│           │███│       │
│      $0│   │███│      │███│       │███│           │███│       │
│         ───┴───┴──────┴───┴───────┴───┴───────────┴───┴       │
│         FY22         FY23          FY24            FY26       │
│                                                               │
│ Source: finance team                                     7/N  │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
from mbb_ppt.constants import NAVY, ACCENT_BLUE, ACCENT_GREEN

eng.stacked_area(
    title='Total revenue grew $300M with mix shift to premium',
    years=['FY22', 'FY23', 'FY24', 'FY25', 'FY26'],
    series_data=[
        ('Premium',  [ 80, 130, 200, 290, 380], NAVY),
        ('Standard', [120, 180, 230, 250, 280], ACCENT_BLUE),
        ('Entry',    [120, 170, 210, 200, 190], ACCENT_GREEN),
    ],
    summary=('Mix shift', 'Premium tripled while entry tier held flat.'),
    source='Source: finance team',
)
```

### Pitfalls

- **Hardcoded `$` currency.** The engine prefixes y-axis ticks and column totals with `$`. If your numbers are not USD, either reformat your numbers (e.g. show "millions of euros" in the title and let `$120` be parsed as "120 of those units") or accept the cosmetic mismatch. (A `currency_symbol` parameter is on the backlog.)
- **Different-length values lists.** Each series's `values` list must equal `len(years)`. Mismatched lengths raise an `IndexError`.
- **Series ordered from top to bottom visually.** First series in the list goes at the *bottom* of the stack (rendered first, then later series stack on top). Order intentionally — typically place the focal series at the bottom (so it forms the "base" of the stack).

---

## `bubble`

Scatter / bubble plot on an XY plane. Each bubble is positioned by `x_pct` and `y_pct` (both 0.0–1.0 fractions of the chart axes), sized by `size_inches`, and labeled. Use for two-variable comparisons with a third dimension encoded in size.

### Signature

```python
eng.bubble(title, bubbles, x_label='', y_label='',
           legend_items=None, summary=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 60 | — |
| `bubbles` | list of **5-tuples** `(x_pct, y_pct, size_inches, label, color)` | yes | label ≤ 8 chars (rendered inside the bubble) | `x_pct` / `y_pct` are 0.0–1.0 fractions of the chart axes (caller normalizes). `size_inches` is the bubble diameter — typically 0.4–1.0. **Up to 10 bubbles.** |
| `x_label` | str | no | ≤ 25 chars | x-axis label (centered below). |
| `y_label` | str | no | ≤ 25 chars | y-axis label (centered to the left). |
| `legend_items` | list of `(name, color)` or `None` | no | — | Optional color legend at top-right. |
| `summary` | str | no | ≤ 80 | Bottom gray summary bar. |
| `source` | str | yes | — | — |

### Example

```python
from mbb_ppt.constants import NAVY, ACCENT_BLUE, ACCENT_GREEN, ACCENT_RED

eng.bubble(
    title='Premium accounts cluster in high-growth, high-margin quadrant',
    bubbles=[
        # (x_pct, y_pct, size_inches, label, color)
        (0.85, 0.78, 0.9, 'Acme',     NAVY),
        (0.72, 0.81, 0.7, 'BetaCo',   NAVY),
        (0.55, 0.45, 0.5, 'Gamma',    ACCENT_BLUE),
        (0.30, 0.65, 0.6, 'Delta',    ACCENT_GREEN),
        (0.15, 0.20, 0.4, 'Epsilon',  ACCENT_RED),
    ],
    x_label='Margin (%) →',
    y_label='Growth (%) →',
    legend_items=[('Premium', NAVY), ('Standard', ACCENT_BLUE)],
    summary='Top-right cluster represents 60% of profitable growth.',
    source='Source: account-level analysis',
)
```

### Pitfalls

- **Wrong tuple arity.** 5-tuples required. Easy to forget the color.
- **`x_pct` / `y_pct` outside 0.0–1.0.** Bubbles plot off the chart axes. Always normalize. To compute: `x_pct = (value - min_x) / (max_x - min_x)`.
- **Overlapping bubbles.** The engine doesn't avoid collisions. If two bubbles overlap, the second is drawn on top and the first label may be obscured. Adjust `x_pct` / `y_pct` slightly to disambiguate, or shrink one bubble.
- **Label too long for bubble size.** A 0.4" bubble with `'Epsilon'` (7 chars) is illegible. Either shorten labels or increase `size_inches`.

---

## `kpi_tracker`

OKR / KPI dashboard — list of KPIs with progress bars, percentages, and color-coded status (`'on'` / `'risk'` / `'off'`).

### Signature

```python
eng.kpi_tracker(title, kpis, summary=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 60 | — |
| `kpis` | list of **4-tuples** `(name, pct_float, detail, status_key)` | yes | name ≤ 30 | `pct_float` is 0.0–1.0 (fraction of progress). `detail` is unused by the current renderer (placeholder for future). `status_key` ∈ `'on'`, `'risk'`, `'off'`. Up to 6 KPIs. |
| `summary` | str | no | ≤ 80 | Bottom gray summary bar. |
| `source` | str | yes | — | — |

The status map is fixed:

| status_key | Color | Label rendered |
|---|---|---|
| `'on'` | `ACCENT_GREEN` | `'On track'` |
| `'risk'` | `ACCENT_ORANGE` | `'Watch'` |
| `'off'` | `ACCENT_RED` | `'Behind'` |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Q4 KPI tracker — 4 of 5 on plan, one at risk          ← title│
│ ─────────────────────────────────────────────────             │
│  KPI                Progress                Attainment Status │
│ ─────────────────────────────────────────────────             │
│  Revenue growth     ████████████████░░░░     85%      ● On    │
│ ─────────────────────────────────────────────────             │
│  Margin expansion   ██████████░░░░░░░░░░     55%      ● Watch │
│ ─────────────────────────────────────────────────             │
│  Customer NPS       ██████████████░░░░░░     72%      ● On    │
│ ─────────────────────────────────────────────────             │
│  Cost reduction     ████████████░░░░░░░░     63%      ● On    │
│ ─────────────────────────────────────────────────             │
│  New product launch ████░░░░░░░░░░░░░░░░     20%      ● Behind│
│                                                               │
│ ┌──────────────────────────────────────────────────────────┐  │
│ │ Summary  Margin and product launch are at risk; rest are│  │
│ │          on plan.                                       │  │
│ └──────────────────────────────────────────────────────────┘  │
│ Source: PMO dashboard, Q4                                7/N  │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.kpi_tracker(
    title='Q4 KPI tracker — 4 of 5 on plan, one at risk',
    kpis=[
        ('Revenue growth',     0.85, '+12% vs target', 'on'),
        ('Margin expansion',   0.55, '+1pp vs plan',   'risk'),
        ('Customer NPS',       0.72, '+8 pts',         'on'),
        ('Cost reduction',     0.63, '-$3M vs plan',   'on'),
        ('New product launch', 0.20, 'Slipped to Q1',  'off'),
    ],
    summary='Margin and product launch are at risk; rest are on plan.',
    source='Source: PMO dashboard, Q4',
)
```

### Pitfalls

- **Wrong tuple arity.** 4-tuples required.
- **`pct_float` > 1.0 or < 0.0.** The engine clamps with `min(pct, 1.0)` before drawing the bar but the label shows the raw percentage. A KPI at 120% of target shows as a full-width bar with "120%" label — visually fine, but inconsistent. Decide a convention.
- **Invalid `status_key`.** Anything other than `'on'`, `'risk'`, `'off'` falls back to MED_GRAY with a `?` label. Validate before passing.

---

## `multi_bar_panel`

Editorial chart with 2–3 side-by-side bar-chart panels, each with its own data and CAGR / trend annotation. Use for "decompose this trend into N segments and show each separately" — typically the most complex chart layout in the engine.

### Signature

```python
eng.multi_bar_panel(title, panels, connectors=None, footnotes=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 60 | — |
| `panels` | list of dicts | yes | — | 2–3 panels. Each panel dict supports keys: `'subtitle'`, `'unit'`, `'years'` (list), `'values'` (list), `'cagr'`, `'legend'`, etc. See implementation in `engine.py` for the full key set; this layout is highly configurable. |
| `connectors` | list or `None` | no | — | Optional arrows between panels showing relationships (e.g. "Q1 panel feeds Q4 panel"). |
| `footnotes` | list[str] or `None` | no | — | Footnote text below the panels. |
| `source` | str | yes | — | — |

### When to use

`multi_bar_panel` is the engine's most editorial chart — modeled after MBB-firm "exhibit" charts that decompose a finding into 2–3 supporting sub-views. Use it when a single chart cannot carry the argument and a side-by-side breakdown clarifies.

For most decks, use `grouped_bar` instead — it's simpler. Reach for `multi_bar_panel` only when the analytical structure genuinely requires multiple sub-charts on one slide.

### Pitfalls

- **Too many panels.** 2–3 is the sweet spot. 4+ shrinks each panel below readable.
- **Inconsistent units across panels.** All panels should use the same unit so the audience can compare visually. If one panel shows revenue and another shows units, the slide is harder to read than two separate slides would be.
- **Missing CAGR.** The visual hook of `multi_bar_panel` is the trend arrow + CAGR annotation per panel. If you don't have CAGR data, this layout is overkill.

---

## Cross-references

- **Method index:** [`../framework/engine-api.md`](../framework/engine-api.md).
- **Capacity matrix:** [`../layout-matrix.yaml`](../layout-matrix.yaml).
- **Past chart-capacity issues:** [`../../experiences/chart-limits.md`](../../experiences/chart-limits.md).
- **Rule 4 (legend color consistency):** [`../framework/guard-rails.md`](../framework/guard-rails.md).
- **Rule 9 (BLOCK_ARC for circular charts):** Not applicable to layouts in this file (these are bar/scatter); see [`charts-circular.md`](charts-circular.md) for the rule's coverage.
