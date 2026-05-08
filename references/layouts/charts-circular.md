# Layouts — Circular Charts

> **Loaded on demand at S4 (Render).** Open this file when rendering a `donut` chart, or when checking why `pie` / `gauge` are no longer recommended.
>
> The `BLOCK_ARC` mechanism that powers circular charts is documented at the bottom of this file.

---

## `donut` (active)

A ring chart with up to 6 segments and a center label. Use for share-of-total / composition where 2–6 categories sum to 100%.

### Signature

```python
eng.donut(title, segments, center_label='', center_sub='',
          legend_x=None, summary=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 (Rule 14); aim for ≤ 60 for charts | Conclusion-led action title. |
| `segments` | list of **3-tuples** `(pct_float, color, label)` | yes | label ≤ 15 chars | Each `pct_float` is 0–1 (not a percentage). Colors are typically `NAVY` + accents. **Max 6 segments.** Beyond 6, merge top-5 + `'Other'`. |
| `center_label` | str | no | ≤ 10 chars | 24pt navy bold. Often the total ($ amount, count) or a focal percentage. |
| `center_sub` | str | no | ≤ 18 chars | Small `MED_GRAY` text under the center label. Use for a unit / context (`'FY26 revenue'`, `'of customers'`). |
| `legend_x` | Inches or `None` | no | — | Override legend horizontal position. Default: `LM + Inches(6.4)` (right of the donut). |
| `summary` | str | no | ≤ 80 chars | Optional gray summary bar below the legend. |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Premium tier drives 42% of revenue from 18% of volume  ← title│
│ ─────────────────────────────────────────────────             │
│                                                               │
│         ╭─────────╮             ■ Premium     42%             │
│        ╱  ┌─────┐  ╲            ■ Standard    31%             │
│       │   │ 42% │   │           ■ Entry       18%             │
│       │   │revenue│ │           ■ Other        9%             │
│        ╲  └─────┘  ╱                                          │
│         ╰─────────╯             ┌──────────────────────────┐  │
│                                 │ Mix shift toward premium │  │
│                                 │ would lift margin ~3pp.  │  │
│                                 └──────────────────────────┘  │
│                                                               │
│ Source: finance team, Q1 close                          5/N   │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
from mbb_ppt.constants import NAVY, ACCENT_BLUE, ACCENT_GREEN, MED_GRAY

eng.donut(
    title='Premium tier drives 42% of revenue from 18% of volume',
    segments=[
        (0.42, NAVY,         'Premium'),
        (0.31, ACCENT_BLUE,  'Standard'),
        (0.18, ACCENT_GREEN, 'Entry'),
        (0.09, MED_GRAY,     'Other'),
    ],
    center_label='42%',
    center_sub='revenue from premium',
    summary='Mix shift toward premium would lift margin ~3pp.',
    source='Source: finance team, Q1 close',
)
```

### Pitfalls

- **More than 6 segments.** Hard cap. Beyond 6, label rows overflow the legend area. Merge to top-5 + `'Other'` ([`experiences/chart-limits.md` Experience 001](../../experiences/chart-limits.md)):
  ```python
  if len(segments) > 6:
      top5 = sorted(segments, key=lambda x: x[0], reverse=True)[:5]
      rest_pct = 1.0 - sum(s[0] for s in top5)
      segments = top5 + [(rest_pct, MED_GRAY, 'Other')]
  ```
  The S3 gate enforces this.
- **Percentages that don't sum to 1.0.** The donut still renders but the ring has a gap or overlap. Validate `sum(pcts) ≈ 1.0` before passing.
- **center_label too long.** 24pt at the donut center has ~1.5" width. Anything over ~10 chars wraps and overlaps the ring. Reformat: `'$1,200,000'` → `'$1.2M'`.
- **Conflicting message in title and center_label.** If the title says "Premium drives 42%" and the center says "29%", the audience is confused. Pick one focal number and reinforce it in both places.

### Cross-references

- Capacity: `donut` row in [`../layout-matrix.yaml`](../layout-matrix.yaml).
- Why circular charts use `BLOCK_ARC`: § "BLOCK_ARC mechanism" below.
- Past donut sizing issues: [`../../experiences/chart-limits.md`](../../experiences/chart-limits.md).

---

## `pie` ⚠️ Retired

`pie` is a retired layout — kept in the engine for backward compatibility but **not recommended for new decks**. Replacement: `donut`.

### Why retired

- A `pie` and a `donut` carry the same information; the donut's center label gives the design an additional anchor (a focal percentage, total $, etc.) that pure pie can't.
- `donut` reads better at executive audiences (the center label is the takeaway).
- Maintaining two near-identical layouts adds engine complexity for no audience benefit.

The S3 content gate does not block `pie` for legacy decks, but the planning guide directs all new decks to `donut`. ([`experiences/chart-limits.md` Experience 003](../../experiences/chart-limits.md).)

---

## `gauge` ⚠️ Retired

`gauge` is a retired layout — kept in the engine for backward compatibility but **not recommended for new decks**. Replacement: `big_number` plus a KPI bullet.

### Why retired

- A gauge implies a quantitative target that the audience must reverse-engineer from the dial position. A `big_number` ("82% of plan") is more direct.
- The horizontal-vs-vertical orientation has historically caused engine bugs (the v2.0 fix added explicit angle handling, but the underlying readability problem remains).
- For health / status indicators with discrete states, `harvey_ball_table` or `kpi_tracker` are clearer.

---

## BLOCK_ARC mechanism

All active circular charts (`donut`, plus the retired `pie` and `gauge`) use native PowerPoint `BLOCK_ARC` shapes via the `add_block_arc()` helper in `mbb_ppt/core.py`. This is **Rule 9** — see [`../framework/guard-rails.md`](../framework/guard-rails.md) for the rationale.

### Why this matters

The pre-v2.0 implementation simulated arcs by drawing hundreds of tiny rectangles around the circumference. That approach:

- Generated 2,000+ shapes per pie chart (vs. 3–4 for `BLOCK_ARC`).
- Produced jagged rendering at any zoom level.
- Caused 30 second to 2 minute generation times for chart-heavy decks.
- Inflated `.pptx` file size proportional to the number of arc shapes.

`BLOCK_ARC` is a single OOXML shape per segment with three adjustment values (`adj1`, `adj2`, `adj3`) controlling start angle, end angle, and inner radius ratio. Smaller files, sharper rendering, faster generation.

### Angle convention

PowerPoint measures angles **clockwise from 12 o'clock**:

| Position | Degrees |
|---|---|
| Top | 0° |
| Right | 90° |
| Bottom | 180° |
| Left | 270° |

The internal helper `add_block_arc()` converts from a math convention (counter-clockwise from 3 o'clock) to PPT clockwise via:

```python
ppt_start = (90 - start_deg - sweep_deg) % 360
ppt_end   = (90 - start_deg) % 360
```

Operator-level code rarely calls `add_block_arc()` directly — `donut` and the retired `pie` / `gauge` handle the angle math internally. Only reach for the helper when building a custom circular chart pattern not covered by the engine.

### `inner_ratio` parameter

`inner_ratio` controls the inner radius as a fraction of `50000` (the OOXML scale):

| inner_ratio | Effect |
|---|---|
| `0` | Solid pie wedge (no hole) |
| `5200` | Thin ring — used for `donut` |
| `25000` | Medium ring (50% inner radius) |
| `45000` | Very thin ring (90% inner radius) — gauge style |

`donut` uses `5200` (a relatively thin ring) by default, leaving room for a center label.

### Cross-references

- **Rule 9 in full:** [`../framework/guard-rails.md`](../framework/guard-rails.md).
- **Implementation:** `mbb_ppt/core.py` → `add_block_arc()`.

---

## Cross-references

- **Method index:** [`../framework/engine-api.md`](../framework/engine-api.md).
- **Capacity matrix:** [`../layout-matrix.yaml`](../layout-matrix.yaml).
- **Past chart-capacity issues:** [`../../experiences/chart-limits.md`](../../experiences/chart-limits.md).
