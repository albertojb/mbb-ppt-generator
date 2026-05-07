# Experiences — Text Overflow Patterns

> **Append-only.** Self-Refinement persistence layer. AI must read this file at the start of S3 (Content). When a pattern-level overflow is fixed during a run, append a new `Experience NNN` entry below.
>
> Adapted from Likaku's `Mck-ppt-design-skill v2.3.3` `experiences/overflow.md`. Apache 2.0.

---

## Experience 001 — Action Title Too Long

**Date**: 2026-05-02
**Problem**: Action titles longer than ~40 characters caused the 22pt title to wrap and overflow into the content area, colliding with the title separator line.
**Root Cause**: The title text frame is fixed-height at 0.9". Wrapped titles exceed that height.
**Fix**: Action title length cap. If a title exceeds the cap, split into a short main title plus a one-line subtitle.
**Rule**: `gate_check_content.py` enforces ≤ 120 chars (Rule 14) and ≥ 10 chars (must be a clause). For tighter visual safety, prefer ≤ 80 chars.

## Experience 002 — `four_column` description too long

**Date**: 2026-05-02
**Problem**: When any column's description exceeded ~120 characters at 14pt body, the bottom of the column overflowed the content area.
**Root Cause**: With four columns evenly distributed across the content width, each column is ~2.7" wide. 14pt body wraps to 4–5 lines at ~120 characters and runs out of vertical space.
**Fix**: Cap each column description at 120 characters. If the content exceeds that, split into bullets.
**Rule**: `gate_check_content.py` enforces `four_column.char_budget.desc = 120` from `layout-matrix.yaml`.

## Experience 003 — `process_chevron` with > 5 steps

**Date**: 2026-05-02
**Problem**: Six or more chevron steps caused arrow-spacing math to go negative, which generated invalid shape dimensions and a corrupted `.pptx`.
**Root Cause**: Rule 10 (horizontal overflow protection) protected the outer frame, but the connector-spacing formula was not synchronized.
**Fix**: Hard cap at 5 steps. If the user has more, split across multiple slides or merge steps.
**Rule**: `gate_check_content.py` enforces `process_chevron.max_steps = 5`. Engine v2.3+ also clamps internally as a safety net.

## Experience 004 — `process_chevron` step label cannot contain `\n`

**Date**: 2026-05-02
**Problem**: Step labels (the first element of each step tuple) containing `\n` caused the oval label shape to overflow vertically by ~21%.
**Root Cause**: The oval is fixed at 0.45" height; a multi-line label exceeds that.
**Fix**: Step labels must be single-line. Use e.g. `'1990-2010'` rather than `'Phase 1\n1990-2010'`.
**Rule**: `gate_check_content.py` enforces `'\n' not in step_label` for `process_chevron`.

## Experience 005 — `four_column` items must be 3-tuples

**Date**: 2026-05-02
**Problem**: Passing 2-tuples `(title, desc)` raised `ValueError: not enough values to unpack`.
**Root Cause**: The engine expects `(num, col_title, desc)` triples; `num` is rendered in the leading numbered circle.
**Fix**: Always pass 3-tuples. The first element is the visible identifier (e.g. `'1'`, `'A'`, `'RS1'`).
**Rule**: `gate_check_content.py` enforces tuple arity = 3 for `four_column`.

## Experience 006 — `timeline` last milestone label overflows right edge

**Date**: 2026-05-02
**Problem**: For a 5-milestone timeline, the last milestone's label rendered ~0.47" past the right boundary even when the label was short.
**Root Cause**: The timeline engine right-anchors the last label at a fixed offset regardless of label length. This is an engine bug.
**Fix**: Last milestone label ≤ 6 characters. The engine bug is acknowledged in `ENGINE_BUG_WHITELIST` (`chart_legend_overflow`, timeline only).
**Rule**: `gate_check_content.py` enforces `len(last_label) <= 6` for `timeline`.
