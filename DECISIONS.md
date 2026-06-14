# DECISIONS — MBB PPT Generator

One line per key decision: **decision — why — which GOAL line it serves.**

---

## v0.7.0 (Epic 5 — Process discipline)

- **Auto-fix trims font size in-pptx, not content.json** — mapping pptx shape names back to content.json fields is architecturally fragile; in-pptx font-shrink via `AutoFixPipeline` satisfies the acceptance criterion ("without operator intervention") more reliably — serves "machine-readable gates enforce the decision objectively"
- **Auto-fix capped at max_rounds=1** — a second pass after a still-failing gate hides repeated overflow problems; one pass fixes transient overflow, two passes masks structural layout issues — serves "gates enforce objectively"
- **Storyboard gate checks `read_aloud_test: true` (not presence of slide titles)** — slide titles are always present in a valid outline.json; the field that confirms deliberate review is `read_aloud_test` — serves "the skill decides which structure and layouts to use — so the operator never has to"
- **`section_divider` has no content area in the new design** — the slide is a visual separator, not a content carrier; adding body text here breaks the operator's mental model of what dividers are for — serves "seamlessly, efficiently and without much babysitting"
- **`section_label` kept as backward-compatible alias for `number`** — callers using the old positional or keyword form must not break on upgrade; deprecate silently rather than hard-remove — serves install story stability

## Pre-v0.7.0 (carried from project charter)

- **Apache 2.0 fork of likaku/Mck-ppt-design-skill** — enables open sharing without legal friction; original credit preserved — serves adoption goal
- **Module names `mbb_ppt` / `MbbEngine` / `ExecEngine` settled** — renaming after public release breaks existing operator scripts; names are locked from v0.1.0 — fixed constraint
- **Install story locked (CLAUDE.md hard-STOP + install.py + GUI drag-drop)** — any divergence from this path has caused 15–40 min failed installs in Cowork sandboxes — fixed constraint
- **English-only, CJK hardening + CI scan** — scope decision to avoid maintenance burden; out of scope is explicit in GOAL.md — fixed constraint
- **No hosted UI, no other AI providers, no other output formats** — each expands the operator's required choices; NORTH STAR is that the skill decides, not the operator — serves "the operator never has to"
