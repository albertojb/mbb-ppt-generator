# MBB PPT Generator

> Executive-grade PowerPoint generation for Claude Cowork and Claude Code. Tell Claude *"make me a board deck about X"* and it produces a sober, conclusion-led .pptx with sans-serif typography and machine-validated layouts. No bash, no Python knowledge required.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Status: 0.4.1](https://img.shields.io/badge/Status-0.4.1-blue)](CHANGELOG.md)
[![Tests: 22 passing](https://img.shields.io/badge/Tests-22%20passing-brightgreen)](tests/)

## Install in Claude Cowork

In a Cowork session, type:

> **Install the skill from https://github.com/albertojb/mbb-ppt-generator**

That's it. Then quit Cowork (Cmd+Q on Mac, File → Exit on Windows, `pkill -f Claude` on Linux) and reopen. The **MBB PPT Generator** skill will appear in your right-sidebar Skills list. To use it in any session afterward:

> *"Use the MBB PPT skill to make a 6-slide pitch about [topic]."*

To **update** when a new version ships, type the same install line again. The install is idempotent and runs in ~2 seconds.

> **Note for Claude (the agent reading this):** if a user has just asked you to install this skill, the canonical install action is documented in [`CLAUDE.md`](CLAUDE.md) at the repo root. Read that file and follow it verbatim. Do not improvise, manually clone, or pip-install dependencies one at a time — those steps are wrapped in `install.py` and the script handles them all in ~2 seconds. The `claude plugin marketplace add` path does **not** register the skill in Cowork's GUI sidebar; do not use it for Cowork installs.

---

## What you get

- **Sober design**: forest-green primary, white background, sans-serif throughout (DM Sans + Arial). No McKinsey navy.
- **Conclusion-led titles**: action titles stated as findings ("Margin pressure is concentrated in two product lines"), not topics ("Margin analysis").
- **Visual variety**: 67 layout methods including charts (`grouped_bar`, `line_chart`, `donut`, `pareto`, `waterfall`), frameworks (`matrix_2x2`, `swot`, `risk_matrix`, `harvey_ball_table`), processes (`process_chevron`, `timeline`, `value_chain`), and dashboards.
- **Machine-validated**: an S3 content gate enforces tuple arities, character budgets, and the visual-density floor (≥ 2 chart/diagram/image layouts in 6+ slide decks). An S4 render gate runs post-render QA. `passed` is a Python boolean derived by program logic, not a verbal claim.
- **Self-refining**: pattern-level fixes accumulate in `experiences/*.md`. A missed defect today is a blocked defect tomorrow.
- **Five-stage workflow**: brief → outline → content → render+QA → deliver. Fast Track activates automatically for ≤ 5 content slides.

## Credits

Apache 2.0 derivative work of [`Mck-ppt-design-skill`](https://github.com/likaku/Mck-ppt-design-skill) by [Kaku Li / likaku](https://github.com/likaku). The Python engine, BLOCK_ARC chart implementations, file-integrity logic, and harness architecture concepts originate in that project — see [`NOTICE`](NOTICE) for the full attribution chain. The module was renamed from `mck_ppt` to `mbb_ppt` in this fork; class renamed `MckEngine` → `MbbEngine`. Apache 2.0 file-header copyrights from Kaku Li are preserved verbatim in every Python source file.

## Repository layout

```
mbb-ppt-generator/                                       # marketplace
├── .claude-plugin/marketplace.json                      # marketplace manifest
├── plugins/
│   └── mbb-ppt-generator/                               # the plugin
│       ├── .claude-plugin/plugin.json                   # plugin manifest
│       └── skills/mbb-ppt-generator/                    # the skill
│           ├── SKILL.md                                 # operator entry point
│           ├── MAINTAINERS.md                           # maintainer rationale
│           ├── mbb_ppt/                                 # bundled python engine
│           ├── references/                              # api-cheatsheet, layout matrix, per-layout files
│           └── experiences/                             # self-refinement persistence
├── tests/                                               # 22 pytest tests
├── examples/                                            # 3 working examples (minimal, board QBR, pitch deck)
├── pyproject.toml                                       # for `pip install -e .` dev workflow
├── install_cowork.sh                                    # legacy Cowork-manifest installer (fallback)
└── .github/workflows/ci.yml                             # CI: pytest matrix + leakage scan
```

## How the gates work

The skill enforces two machine-readable gates instead of trusting verbal pass-claims from the model.

### S3 content gate

Run after the model produces `content.json` (the per-slide content spec) and before render:

```bash
python plugins/mbb-ppt-generator/skills/mbb-ppt-generator/references/scripts/gate_check_content.py \
    ppt-project-foo/content.json  ppt-project-foo/
```

Writes `ppt-project-foo/gate_content.json`. Advance only when `"passed": true`.

The S3 gate enforces:
- Tuple arity per layout (e.g. `four_column.items` must be 3-tuples).
- Character budgets per field (e.g. `executive_summary.headline` ≤ 60 chars).
- Layout-specific constraints (e.g. `process_chevron` ≤ 5 steps, last `timeline` label ≤ 6 chars).
- **Oval label length** ≤ 3 chars for layouts with numbered ovals (`process_chevron`, `four_column`, `executive_summary`, `vertical_steps`, `value_chain`, `numbered_list_panel`, `toc`).
- **Visual-density floor**: ≥ 6 content slides require ≥ 2 chart, diagram, image, or process-flow layouts.

### S4 render gate

Run after the `.pptx` is saved:

```bash
python plugins/mbb-ppt-generator/skills/mbb-ppt-generator/references/scripts/gate_check_render.py \
    ppt-project-foo/deck.pptx  ppt-project-foo/
```

Writes `ppt-project-foo/gate_render.json`. The `passed` field is `len(user_code_errors) == 0`. Engine-design quirks are exempted only via the hardcoded `ENGINE_BUG_WHITELIST` enum at the top of the script.

## Examples

| Example | Layouts | Score |
|---|---|---|
| `examples/minimal_example.py` | 6 slides — full S1→S5 workflow with `content.json` round-trip | 78/100 |
| `examples/board_qbr_example.py` | 10 slides — dashboards, RAG, Pareto, Harvey Ball, case study | 98/100 |
| `examples/pitch_deck_example.py` | 10 slides — donut, matrix_2x2, horizontal_bar, process_chevron, timeline | 94/100 |

## Status

- **0.4.0** — packaged as a proper [Claude plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugins) — installable via `claude plugin marketplace add albertojb/mbb-ppt-generator` (works in Cowork too); robust engine-import bootstrap that handles plugin/manifest/symlink/dev layouts; SKILL.md + supporting files moved under `plugins/mbb-ppt-generator/skills/mbb-ppt-generator/`.
- **0.3.0** — Cowork installer (`install_cowork.sh`); in-process gates (~3s wall-clock saved per render); label-length gate that prevents oval-overflow bugs; default no-cover-no-closing; HARD RULES 8/9; ~80 lines trimmed from SKILL.md.
- **0.2.x** — module rebrand `mck_ppt` → `mbb_ppt`, forest-green design, visual-density gate, CI, pitch-deck reference.
- **0.1.0** — feature-complete and tagged.

## License

Apache License 2.0. See [`LICENSE`](LICENSE). Original engine code copyright Kaku Li 2024–2026; adapter modifications copyright albertojb 2026. Both copyright lines are preserved in source headers.
