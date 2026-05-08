# MAINTAINERS — design rationale & harness pedagogy

> This file is for skill maintainers — people editing `SKILL.md`, `references/`, gate scripts, or the engine. Operators (people running the skill in Claude Cowork or Claude Code) do not need to read it. The runtime documentation is in `SKILL.md`.

## Why this skill is structured around mechanisms

Two ideas borrowed from Kaku Li's harness work apply to AI skills generally, not just to PPT.

### Iron law 1 — Output quality is multiplicative

```
AI output quality  =  AI capability  ×  context quality
```

It is multiplication, not addition. As context quality approaches zero, output quality approaches zero regardless of model capability. Most skill failures are not capability failures; they are context-quality failures. Context quality is the lever you control.

In practice this means: when you find a recurring failure mode, the right fix is almost never "be more careful in the prompt." The right fix is to put the necessary context in the right file at the right stage of the workflow, or to push the constraint into a gate script.

### Iron law 2 — Mechanism beats prompt

A prompt that asks the model to "be careful" is a soft constraint. A script that reads `gate_render.json` and refuses to advance unless `passed: true` is a hard constraint. **Prefer mechanism wherever you can encode the rule.**

The corollary: when a model says "task complete" and there is no gate file proving it, the task is *not* complete.

## How this manifests in the skill

| Soft (avoid) | Hard (prefer) |
|---|---|
| "Be careful with character budgets" in the prompt | `gate_check_content.py` reads `layout-matrix.yaml` and rejects content that exceeds them |
| "Page numbers go at the bottom right" | `PAGE_NUM_LEFT/TOP/WIDTH/HEIGHT` are constants the engine pins to |
| "Engine quirks are OK in some cases — use judgment" | `ENGINE_BUG_WHITELIST` enum in `gate_check_render.py`, with required textual evidence per entry |
| "Read all the references before generating" | `references/INDEX.md` routing table loads only the files for the current stage |
| "Run the gate after rendering" | `mbb-ppt render` runs both gates and exits non-zero on failure |

## Anti-patterns at the top of SKILL.md

`SKILL.md` § *Failure modes* deliberately puts three concrete anti-patterns ("Verbal gate-pass", "Mental S3 review", "engine_bug as escape hatch") at the top of the document, *before* HARD RULES. This is on purpose:

- A list of rules tells the model what to do.
- A list of failure modes tells the model where prior runs broke.
- The second is more durable, because it makes the rule's *purpose* visible.

When you find a new recurring failure mode, the question is: can it be encoded as a gate? If yes, write a gate. If no (because the rule needs human judgment), promote the failure mode into the SKILL.md anti-patterns section with a wrong/right pair.

## Maintenance notes

### Adding a new layout

Three files must be updated together:

1. `mbb_ppt/engine.py` — implementation.
2. `references/layout-matrix.yaml` — capacity row (`char_budget`, `tuple_arity`, `max_items`, etc.).
3. `references/api-cheatsheet.md` — one-liner row in the matching family table.
4. `references/layouts/<family>.md` — full layout reference (parameters, wireframe, example, pitfalls).

The S3 content gate consumes `layout-matrix.yaml` directly, so missing rows there silently disable validation for that layout.

### Adding a guard rail

1. Implement the check in `gate_check_render.py` (for visual rules) or `gate_check_content.py` (for content rules).
2. Add the rule to `references/framework/guard-rails.md` with rationale.
3. Update `SKILL.md` § *Production guard rails* with a one-line summary.
4. Add a smoke test in `tests/test_gates.py` that asserts the rule is enforced.

### Adding an `engine_bug` whitelist entry

1. Add the entry to `ENGINE_BUG_WHITELIST` in `gate_check_render.py`.
2. Include a textual evidence comment with the `engine.py` line reference and the design rationale.
3. The evidence comment is **mandatory**. A whitelist without evidence becomes folklore.

### Updating typography or color

`mbb_ppt/constants.py` is the single source of truth. After editing:

1. Update `SKILL.md` § *Design system* / *Colors* / *Typography* tables.
2. Update `references/team/brand-guide.md`.
3. Re-render `examples/minimal_example.py` and `examples/board_qbr_example.py` and verify.

### Self-Refinement persistence

`experiences/` is **append-only**. Never delete entries; mark superseded ones with `Superseded by NNN`. The pattern is:

```markdown
## Experience NNN: <short title>
**Date**: YYYY-MM-DD
**Problem**: <one-line description>
**Root Cause**: <why it happened>
**Fix**: <what was changed>
**Rule**: <how the gate could prevent this next time>
```

If the rule is mechanizable, file an issue or PR adding the check to `gate_check_content.py` or `gate_check_render.py`.

## Attribution invariants

These are non-negotiable and exist for legal/ethical reasons:

- Apache 2.0 file-header copyrights from Kaku Li are preserved in every Python source file in `mbb_ppt/`.
- `LICENSE` is verbatim Apache 2.0.
- `NOTICE` enumerates all upstream attribution and the modifications introduced by this fork.
- `README.md` and `SKILL.md` both credit Kaku Li / likaku for the upstream `Mck-ppt-design-skill` (URL preserved).
- The upstream URL `https://github.com/likaku/Mck-ppt-design-skill` appears in `pyproject.toml` (`Upstream`) and `NOTICE`.

If you are removing or changing any of the above, stop and read the Apache License 2.0 § 4.

## What this skill is *not*

It is not:

- A general-purpose `python-pptx` wrapper. The engine is opinionated about layout and rejects deviations the QA module cannot validate.
- A natural-language-to-deck pipeline that bypasses the workflow. The five-stage workflow is the contract — Fast Track only relaxes S2/S3 gates for ≤ 5-slide decks with no charts.
- A McKinsey skill. The naming convention "MBB-style" describes a category of executive consulting design and is not affiliated with or endorsed by any consulting firm.
- A presentation theme. Use it for content and structure; visual themes belong in `mbb_ppt/constants.py` and the per-layout reference files.

## Useful commands during maintenance

```bash
# Run the full test suite (15 tests)
pytest

# Run a render + gate end-to-end (CLI dogfooding)
mbb-ppt render examples/content.json --out /tmp/test.pptx

# Verify no McKinsey/Tencent/WorkBuddy leakage
grep -rli "mck\|mckinsey\|tencent\|workbuddy\|hunyuan\|clawhub" \
    --exclude-dir=_likaku_may3 --exclude-dir=_likaku_harness --exclude-dir=.git \
    --include="*.py" --include="*.md" --include="*.yaml" --include="*.toml" .

# Re-extract the API cheatsheet from engine docstrings (when adding/removing layouts)
python -c "..."  # see scripts/regen_cheatsheet.py if/when it's added
```
