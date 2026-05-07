# MBB PPT Generator

> Executive-grade PowerPoint generation with consulting-style discipline. Self-contained skill for AI agents (Claude Code, WorkBuddy, ClawHub) that follows the five-stage workflow: brief → outline → content → render+QA → deliver. Two machine-readable gates make pass/fail a program decision, not a model decision.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

## What this is

A skill spec plus a bundled Python engine plus a harness of gates and references, designed so an AI agent can produce a board-quality deck without you babysitting the layout. The workflow is grounded in:

- **Barbara Minto's Pyramid Principle** — answer-first, MECE-grouped, conclusion-led headlines
- **Harness engineering** — context loaded by stage, gates that emit JSON, anti-patterns documented at the top of the spec
- **Production hardening** — 18 guard rails, 6-segment cap on donut charts, 5-step cap on process chevrons, 120-character cap on action titles, file-integrity cleanup at save time

## Credits

This skill is a derivative work of [`Mck-ppt-design-skill`](https://github.com/likaku/Mck-ppt-design-skill) by [Kaku Li / likaku](https://github.com/likaku), Apache 2.0. The engine package (`mck_ppt/`), the QA module, the BLOCK_ARC chart implementations, and the file-integrity logic are Kaku Li's work and are bundled here under the original copyright. The five-stage workflow and self-refinement protocol are also adapted from Kaku Li's separate [`harness-skill-upgrader`](https://github.com/likaku/harness-skill-upgrader) skill.

See [`NOTICE`](NOTICE) for the full attribution chain and a list of modifications introduced by this fork.

## Install

This skill ships as a single self-contained folder. No external skill installation required.

```bash
# Clone or download the repo
git clone https://github.com/<your-org>/mbb-ppt-generator ~/.workbuddy/skills/mbb-ppt-generator

# Install runtime dependencies (small surface)
pip install python-pptx lxml pyyaml
```

Optional dependencies (only needed if you enable specific features):

```bash
# Local image processing (cover_image with rembg cutout)
pip install pillow numpy rembg

# Cloud cover-image generation (Tencent Hunyuan — OFF by default)
pip install tencentcloud-sdk-python
```

## Quick start

```python
import sys, os
sys.path.insert(0, os.path.expanduser('~/.workbuddy/skills/mbb-ppt-generator'))
from mck_ppt import MckEngine as ExecEngine
from mck_ppt.constants import NAVY, ACCENT_BLUE
from pptx.util import Inches

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
├── LICENSE                          # Apache 2.0
├── NOTICE                           # attribution chain
├── MBB_PPT_QA_CHECKLIST.md          # visual QA checklist (after the gates pass)
│
├── mck_ppt/                         # bundled engine (Kaku Li's, Apache 2.0)
│   ├── __init__.py
│   ├── constants.py                 # design system + guard-rail constants
│   ├── core.py                      # low-level drawing primitives
│   ├── engine.py                    # ~67 high-level layout methods
│   ├── qa.py                        # automated visual QA (used by render gate)
│   ├── deck_builder.py              # storyline-driven orchestration
│   ├── review.py                    # slide review + auto-fix pipeline
│   ├── cover_image.py               # optional cloud cover image (off by default)
│   └── storylines/                  # canned storyline templates
│
├── references/
│   ├── INDEX.md                     # knowledge router (stage → load map)
│   ├── layout-matrix.yaml           # capacity matrix (single source of truth)
│   ├── color-palette.md             # quick reference
│   ├── layout-catalog.md            # 72-layout index (legacy browse view)
│   ├── team/                        # most-stable layer (rarely changes)
│   ├── framework/                   # framework layer — to be filled out
│   ├── layouts/                     # per-layout reference — to be filled out
│   └── scripts/
│       ├── gate_check_content.py    # S3 content gate (English)
│       └── gate_check_render.py     # S4 render gate (English, w/ engine_bug whitelist)
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

## Status

- ✅ Engine bundled and self-contained — no external skill installation needed.
- ✅ DM Sans heading typography wired through.
- ✅ Both gate scripts in English with self-locating `mck_ppt` import.
- ✅ Experience corpus (overflow, layout-pitfalls, chart-limits) seeded.
- 🚧 `references/framework/` and `references/layouts/` reference files in progress — the routing table in SKILL.md will start fulfilling its promise as those files land.
- 🚧 Public release on GitHub + skill marketplaces — pending.

## License

Apache License 2.0. See [`LICENSE`](LICENSE). Original engine code copyright Kaku Li 2024-2026; adapter modifications copyright albertojb 2026. Both copyright lines are preserved in source headers.
