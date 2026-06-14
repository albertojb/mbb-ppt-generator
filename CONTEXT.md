# CONTEXT — MBB PPT Generator

Things a future run needs that aren't in the code or git history.

---

## Architecture invariants (as of v0.7.0)

- **Single source of truth for layout API:** `references/api-schemas.yaml`. The cheatsheet is generated from it — never edit the cheatsheet by hand.
- **Gate contract:** every gate script returns `{"passed": bool, ...}` and exits non-zero when `passed` is false. This is machine-readable and must stay JSON-clean (no stray prints before the JSON blob).
- **Auto-fix contract:** `--auto-fix` on `gate_check_render.py` calls `AutoFixPipeline(max_rounds=1)`, re-gates once, and returns with an `auto_fix` metadata block. It does NOT touch `content.json` — fixes are in-pptx only (font-shrink). This was a deliberate decision; see DECISIONS.md.
- **`section_divider` new layout:** full-width forest-green accent bar + optional 72pt numeral + 32pt title + 14pt italic subtitle. No content area, no page number. The old `section_label` positional/keyword arg still works as an alias for `number`.
- **`add_text()` now has `italic=` kwarg.** Added in v0.7.0 to support subtitle in `section_divider`.

## What "install story untouchable" means

The install path (CLAUDE.md hard-STOP + `install.py` + GUI `.skill` drag-drop) is frozen. Any Epic 6 or 7 work on surface-specific adaptations must not change the install script, the CLAUDE.md hard-STOP text, or the plugin manifest structure. Surface-specific additions go in separate doc/adaptation layers on top.

## Test hygiene

- `tests/test_gates.py` owns all gate-script tests. 48 tests total as of v0.7.0.
- Storyboard gate tests and render-autofix tests are in separate `_run_*` helpers — keep them isolated.
- Never add layout tests to `test_gates.py` and vice versa.

## Deferred work (degunk backlog from v0.7.0 run)

Minor smells raised by code-degunker during v0.7.0 planning — not filed as issues, not blocking:

- #7–#14: minor code-style and over-defensive-check smells across `engine.py`, `core.py`, `review.py`. Not critical. Revisit during a cleanup sweep if a future run has slack capacity.

## Epic 6 entry points to investigate

When starting Epic 6 (multi-surface: GitHub CLI + ZoComputer):

- **GitHub CLI surface:** No GUI; must work entirely via terminal. Key question: does `python3` resolve correctly in a typical GitHub CLI environment? Gate scripts invoke `python3` — test whether a shebang or explicit `python3 path/to/gate.py` is more portable.
- **ZoComputer surface:** Unknown file-write scope. Determine whether ZoComputer agents can write to the project directory (for `experiences/` append and `content.json`). If not, document the workaround path.
- **Don't regress Cowork or terminal paths** — any surface-specific adaptation must be additive, not a fork.
