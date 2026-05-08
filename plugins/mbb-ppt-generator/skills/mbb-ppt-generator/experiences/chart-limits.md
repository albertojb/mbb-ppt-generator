# Experiences — Chart Capacity Limits

> **Append-only.** Self-Refinement persistence layer. Read at the start of S3.
>
> Adapted from Likaku's `Mck-ppt-design-skill v2.3.3` `experiences/chart-limits.md`. Apache 2.0.

---

## Experience 001 — `donut` max 6 segments

**Date**: 2026-05-02
**Problem**: A 7-segment donut produced legend labels that overflowed the right side and overlapped each other vertically.
**Root Cause**: Each segment maps to one legend row; the legend column has a fixed total height that fits at most 6 rows at the configured 14pt label size.
**Fix**: Donut limited to 6 segments. When the input has more, merge to top-5 + an `'Other'` aggregate.

```python
# Top-5 + Other reduction
if len(segments) > 6:
    top5 = sorted(segments, key=lambda x: x[0], reverse=True)[:5]
    rest_pct = 1.0 - sum(s[0] for s in top5)
    segments = top5 + [(rest_pct, MED_GRAY, 'Other')]
```

**Rule**: `gate_check_content.py` enforces `donut.max_segments = 6`.

## Experience 002 — `grouped_bar` max 6 categories × 3 series

**Date**: 2026-05-02
**Problem**: 7 categories × 3 series produced bars narrow enough that x-axis labels overlapped.
**Root Cause**: Dynamic-width math reduces font size only to a floor; below that floor labels collide.
**Fix**: Cap at 6 categories × 3 series. If the user has more data, split into multiple slides (e.g. by region) or pivot to `horizontal_bar`.
**Rule**: `gate_check_content.py` enforces `grouped_bar.max_categories = 6` and `max_series = 3`.

## Experience 003 — `pie` is retired; use `donut`

**Date**: 2026-05-06
**Problem**: `pie` and `donut` had the same rendering path but `donut` reads cleaner because the center label can hold the total or a callout. Maintaining both was redundant.
**Fix**: `pie` is retired in `layout-matrix.yaml` with `replacement: donut`. The engine method still exists for backward compatibility but should not be used in new decks.
**Rule**: `gate_check_content.py` does not block `pie` (legacy decks still parse), but the planning guide directs all new decks to `donut`.
