# STATUS — MBB PPT Generator

> **Next run starts here.** v0.7.0 shipped 2026-06-14. All three Epic 5 tasks are done and merged. Next milestone is Epic 6 — multi-surface support (GitHub CLI + ZoComputer). Read RESUME.md and CONTEXT.md before starting.

---

## Current state

- **Version:** `0.7.0`
- **Latest tag:** `v0.7.0` (to be pushed — see below)
- **Tests:** 48/48 passing
- **CI:** green on main (tests + leakage scan)
- **Working tree:** clean

## What shipped in v0.7.0 (2026-06-14)

| PR | Task | What landed |
|---|---|---|
| #15 | Task 21 | S2 storyboard gate (`gate_check_storyboard.py`). Blocks S3 until `read_aloud_test: true` in `outline.json`. SKILL.md updated. |
| #16 | Task 22 + fix #2 | Render gate `--auto-fix` mode: font-shrink on minor text overflows (≤50%), re-gates once, logs every fix. Fixed two swallowed exceptions in `review.py`. |
| #17 | Task 23 | `section_divider` redesigned: full-width accent bar + 72pt numeral + 32pt title + 14pt italic subtitle. No content area. `add_text()` gains `italic=` param. Schema + cheatsheet updated. Version bumped to 0.7.0 in all 4 locations. |

## Open issues after this run

- **Minors deferred (degunk backlog):** #7–#14 — carried forward, not filed as new issues.
- **Issue #2** closed (bundled into PR #16).

## What's next

**Epic 6 — Multi-surface support (GitHub CLI + ZoComputer).** See ROADMAP.md and CONTEXT.md.
