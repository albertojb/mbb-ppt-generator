# GOAL — MBB PPT Generator

NORTH STAR: Given a brief, the skill decides which structure and layouts to use — so the operator never has to — and machine-readable gates enforce that decision objectively.

---

## Goal

Make producing a consulting-quality `.pptx` deck so seamless, efficient, and low-babysitting that any Claude user — technical or not — can do it well, across Claude Cowork, GitHub CLI, and ZoComputer.

## Core decision the project drives

Given a brief, the skill decides which structure and layouts to use so the operator never has to. Machine-readable gates enforce that decision objectively. Every feature, gate, and layout added to this project should make that decision better or enforce it more reliably.

## Definition of done

The skill runs end-to-end, across all three supported surfaces (Cowork, GitHub CLI, ZoComputer), and produces a presentation-ready deck without operator intervention. Alberto is the judge.

Broad adoption is a secondary goal but not the finish line.

## Out of scope

- Other output formats (Google Slides, Keynote, PDF-only)
- Other AI providers
- Hosted web UI
- Multi-language support (English-only; CI-enforced)

## Fixed constraints

- **Apache 2.0 attribution chain** to Kaku Li / likaku must remain intact in all source files, NOTICE, LICENSE, and CHANGELOG. The CI brand-leakage scan enforces this.
- **English-only.** No CJK guidance, defaults, prompts, or comments.
- **Install story is locked.** GUI `.skill` drag-drop (primary) and terminal one-liner (secondary) are the only supported install paths. Do not regress either. Do not attempt install from within a Cowork session.
- **Module names are settled.** `mbb_ppt`, `MbbEngine`, `ExecEngine`. Do not rename.
