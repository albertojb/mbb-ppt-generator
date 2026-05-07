# Experiences — Layout-Specific Pitfalls

> **Append-only.** Self-Refinement persistence layer. Read at the start of S3.
>
> Adapted from Likaku's `Mck-ppt-design-skill v2.3.3` `experiences/layout-pitfalls.md`. Apache 2.0.

---

## Experience 001 — `two_column_text` overuse

**Date**: 2026-05-02
**Problem**: Multiple `two_column_text` slides in the same deck looked visually monotonous; the deck "felt mechanical."
**Fix**: At most one `two_column_text` slide per deck. Replace others with `table_insight`, `side_by_side`, or `four_column`.
**Rule**: `gate_check_content.py` enforces `global_max_per_deck = 1`.

## Experience 002 — Cover subtitle position after multi-line title

**Date**: 2026-05-02
**Problem**: Multi-line cover titles were followed by subtitles in a fixed `y` position, causing visual overlap.
**Root Cause**: Older code hardcoded `subtitle_y = Inches(3.5)`.
**Fix**: Engine `v1.10.4+` computes `subtitle_y = title_y + title_h + Inches(0.3)` dynamically.
**Rule**: Use `eng.cover()` — never hand-write cover layout code.

## Experience 003 — Content starts at the wrong `y` after action title

**Date**: 2026-05-02
**Problem**: Code that placed first content element at `Inches(1.0)` collided with the action title separator at `Inches(1.05)`.
**Root Cause**: Inconsistent assumption about where the title bar ends.
**Fix**: Content starts at `CONTENT_TOP = Inches(1.3)` after `add_action_title()`.
**Rule**: Always import `CONTENT_TOP` from `mck_ppt.constants` rather than hand-coding the value.

## Experience 004 — Bottom bar cuts off last table row

**Date**: 2026-05-02
**Problem**: A bottom summary bar at fixed `y = Inches(6.2)` overlapped the last table row when row count grew.
**Root Cause**: Static positioning of the bottom bar regardless of dynamic content height.
**Fix**: `bar_y = max(last_row_bottom + Inches(0.2), Inches(6.1))`, clamped at `min(bar_y, Inches(6.4))`.
**Rule**: Render gate (Rule 1, 16) flags overlap and tight gaps.

## Experience 005 — Timeline last-label overflow is an engine bug

**Date**: 2026-05-03
**Problem**: `timeline` always reports `chart_legend_overflow` for the last milestone, even with a 2-character label like `'Q4'`.
**Root Cause**: Engine right-anchors the last label at a fixed offset; the QA check measures actual position, finds it past the right edge.
**Fix**: Added to `ENGINE_BUG_WHITELIST` in `gate_check_render.py` (limited to `timeline`). All other layouts triggering this category are real overflows and not exempt.
**Rule**: Whitelist exemption is in code, not in conversation. Verbal "ignore this error" is never acceptable.
