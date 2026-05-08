# MBB PPT Generator

> Executive-grade PowerPoint generation with consulting-style discipline. Self-contained Claude skill (Claude Code, Claude Cowork) that follows a five-stage workflow — brief → outline → content → render+QA → deliver — and uses two machine-readable gates so pass/fail is a program decision, not a model decision.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](pyproject.toml)
[![Tests: 15 passing](https://img.shields.io/badge/Tests-15%20passing-brightgreen)](tests/)
[![Status: 0.2.0](https://img.shields.io/badge/Status-0.2.0-blue)](CHANGELOG.md)

## What this is

A skill spec plus a bundled Python engine plus a harness of gates and references, designed so an AI agent can produce a board-quality deck without you babysitting the layout. The workflow is grounded in:

- **Barbara Minto's Pyramid Principle** — answer-first, MECE-grouped, conclusion-led headlines
- **Harness engineering** — context loaded by stage, gates that emit JSON, anti-patterns documented at the top of the spec
- **Production hardening** — 18 guard rails, 6-segment cap on donut charts, 5-step cap on process chevrons, 120-character cap on action titles, file-integrity cleanup at save time

## Credits

This skill is a derivative work of [`Mck-ppt-design-skill`](https://github.com/likaku/Mck-ppt-design-skill) by [Kaku Li / likaku](https://github.com/likaku), Apache 2.0. The Python engine package, the QA module, the BLOCK_ARC chart implementations, and the file-integrity logic are Kaku Li's work and are bundled here under the original copyright (the module was renamed from `mck_ppt` to `mbb_ppt` in this fork; class renamed `MckEngine` → `MbbEngine`). The five-stage workflow and self-refinement protocol are also adapted from Kaku Li's separate [`harness-skill-upgrader`](https://github.com/likaku/harness-skill-upgrader) skill.

See [`NOTICE`](NOTICE) for the full attribution chain and a list of modifications introduced by this fork.

## Install

### As a Claude skill (recommended for Claude Cowork / Claude Code users)

```bash
git clone https://github.com/albertojb/mbb-ppt-generator.git ~/.claude/skills/mbb-ppt-generator
cd ~/.claude/skills/mbb-ppt-generator
pip install -e .
```

After install, the skill is available in Claude Cowork and Claude Code under the name **MBB PPT Generator**. Non-technical users invoke it by saying:

> *"Use the MBB PPT skill on this brief."*  
> *"Make me a board deck from `meeting_notes.md` using the MBB skill."*

The skill takes care of the brief → outline → content → render → QA workflow internally; you do not need to run any Python yourself.

### As a Python package (for direct programmatic use)

```bash
git clone https://github.com/albertojb/mbb-ppt-generator.git
cd mbb-ppt-generator
pip install -e .

# Optional extras
pip install -e ".[dev]"        # core + pytest
pip install -e ".[image]"      # core + rembg/Pillow/numpy for image processing
pip install -e ".[all]"        # everything
```

After install, run the test suite to confirm setup:

```bash
pytest                # 15 tests, ~5 seconds
```

## 60-second quickstart

```bash
python examples/minimal_example.py
# → ppt-project-demo/deck.pptx, gate_render.json (passed: true)
```

Open `ppt-project-demo/deck.pptx` in PowerPoint or Keynote.

## CLI

After install, a `mbb-ppt` command is on your PATH (or run as `python -m mbb_ppt`):

```bash
mbb-ppt render content.json --out deck.pptx     # render content.json to .pptx + run both gates
mbb-ppt gate-content content.json               # S3 content gate only
mbb-ppt gate-render deck.pptx                   # S4 render gate only
```

The CLI exits non-zero if any gate fails, so it composes cleanly with shell scripts and CI.

## Programmatic use

```python
from mbb_ppt import MbbEngine as ExecEngine

eng = ExecEngine(total_slides=4)
eng.cover(title='Q1 2026 strategy review', subtitle='Board update',
          author='Strategy team', date='March 2026')
eng.executive_summary(
    title='Three actions return revenue to double-digit growth',
    headline='Growth is concentrated in two channels and one product tier',
    items=[('1', 'Shift mix toward premium', 'Higher margin, limited cost-to-serve impact'),
           ('2', 'Expand in underpenetrated channels', 'Two distributor channels remain underdeveloped'),
           ('3', 'Fund through operating simplification', 'Back-office complexity can shrink without harming service')],
    source='Source: internal analysis, Q1 2026',
)
eng.closing(title='Thank you', message='Discussion and decision points')
eng.save('output/q1_strategy_review.pptx')
```

## Repository layout

```
mbb-ppt-generator/
├── SKILL.md                         # main skill spec (entry point for AI)
├── README.md                        # this file
├── MAINTAINERS.md                   # harness pedagogy + design rationale
├── LICENSE                          # Apache 2.0
├── NOTICE                           # attribution chain
├── MBB_PPT_QA_CHECKLIST.md          # visual QA checklist (after the gates pass)
│
├── mbb_ppt/                         # bundled engine (Apache 2.0)
│   ├── __init__.py
│   ├── __main__.py                  # CLI entry (python -m mbb_ppt)
│   ├── constants.py                 # design system + guard-rail constants
│   ├── core.py                      # low-level drawing primitives
│   ├── engine.py                    # ~67 high-level layout methods
│   ├── qa.py                        # automated visual QA (used by render gate)
│   ├── deck_builder.py              # storyline-driven orchestration
│   ├── review.py                    # slide review + auto-fix pipeline
│   └── storylines/                  # canned storyline templates
│
├── references/
│   ├── INDEX.md                     # knowledge router (stage → load map)
│   ├── api-cheatsheet.md            # one-page method signatures
│   ├── layout-matrix.yaml           # capacity matrix (single source of truth)
│   ├── team/                        # brand + presentation conventions
│   ├── framework/                   # engine-api, guard-rails, planning-guide
│   ├── layouts/                     # per-layout reference (12 files)
│   └── scripts/
│       ├── gate_check_content.py    # S3 content gate
│       └── gate_check_render.py     # S4 render gate
│
└── experiences/                     # self-refinement persistence (append-only)
    ├── overflow.md
    ├── layout-pitfalls.md
    └── chart-limits.md
```

## How the gates work

The skill enforces two machine-readable gates instead of trusting verbal pass-claims from the model.

### S3 content gate

Run after the model produces `content.json` (the per-slide content spec) and before render:

```bash
python references/scripts/gate_check_content.py \
    ppt-project-foo/content.json  ppt-project-foo/
```

Writes `ppt-project-foo/gate_content.json`. Advance only when `"passed": true`.

### S4 render gate

Run after the `.pptx` is saved:

```bash
python references/scripts/gate_check_render.py \
    ppt-project-foo/deck.pptx  ppt-project-foo/
```

Writes `ppt-project-foo/gate_render.json`. The `passed` field is a Python boolean derived from `len(user_code_errors) == 0`. Engine-design quirks are exempted only via the hardcoded `ENGINE_BUG_WHITELIST` enum at the top of the script — verbal exemptions are not accepted.

## Self-Refinement

When a pattern-level fix is applied during a run, append a numbered `Experience NNN` entry to the matching file under `experiences/`. Format:

```markdown
## Experience NNN: <short title>
**Date**: YYYY-MM-DD
**Problem**: <one-line description>
**Root Cause**: <why it happened>
**Fix**: <what was changed>
**Rule**: <how the gate could prevent this next time>
```

If the rule is mechanizable, also propose a check to add to one of the gate scripts. The skill gets stronger over time — a missed defect today should be a blocked defect tomorrow.

## Examples

Three runnable examples ship with the skill, all passing both gates end-to-end:

| Example | What it shows | Run |
|---|---|---|
| `examples/minimal_example.py` | Full S1→S5 workflow on a 6-slide strategy review. Writes `content.json`, runs both gates as subprocesses, renders the deck, prints the verdict. **Best for**: learning the harness workflow. | `python examples/minimal_example.py` |
| `examples/board_qbr_example.py` | 10-slide quarterly business review. Imperative engine calls (no JSON round-trip). Demonstrates dashboard, RAG status, Pareto, Harvey Ball evaluation, and case study layouts. **Best for**: operating-cadence decks. | `python examples/board_qbr_example.py` |
| `mbb_ppt/storylines/ai_enterprise.py` | 12-slide strategy-review storyline using `DeckBuilder.build()`. Covers cover, TOC, executive_summary, big_number, grouped_bar, table_insight, side_by_side, donut, timeline, key_takeaway, action_items, closing. **Best for**: starting from a complete template. | `python -c "from mbb_ppt.deck_builder import DeckBuilder; from mbb_ppt.storylines import ai_enterprise; DeckBuilder.build(ai_enterprise.STORYLINE, 'output.pptx')"` |

## Tests

```bash
pytest                              # all 15 tests
pytest tests/test_smoke.py          # just the import + render smoke checks
pytest tests/test_gates.py          # gate-script behavior
pytest tests/test_layouts.py        # layout family coverage
pytest -k storyline                 # only the 12-slide storyline build
```

Coverage spans engine import, .pptx zip integrity, the `full_cleanup()` XML sanitizer, all five layout families (structure, data, narrative, charts, frameworks), the bundled storyline, and both gate scripts (with assertions that the gates correctly catch short titles, missing sources, and donut over-counts).

## Status

- **0.2.0** — module rebranded `mck_ppt` → `mbb_ppt`; primary color forest-green; CLI added; cloud cover-image integration removed.
- **0.1.0** — feature-complete and tagged. Engine bundled and self-contained; no external skill installation needed.

## License

Apache License 2.0. See [`LICENSE`](LICENSE). Original engine code copyright Kaku Li 2024-2026; adapter modifications copyright albertojb 2026. Both copyright lines are preserved in source headers.
