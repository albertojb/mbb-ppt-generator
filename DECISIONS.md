# DECISIONS — MBB PPT Generator

One line per key decision: **decision — why — which GOAL line it serves.**

---

## v0.8.1 (Epic 6 — Multi-agent reach)

- **`AGENT.md` as a separate file rather than modifying `SKILL.md`** — ~70% of SKILL.md is reusable workflow logic; ~30% is Claude-specific (TodoWrite, Read/Write tools, path bootstrap); splitting keeps the Claude Cowork/Code path untouched and avoids confusing non-Claude agents with tool references they can't call — serves "works for any agent without breaking Cowork"
- **`gate-storyboard` added as CLI subcommand rather than docs-only instruction** — AGENT.md's five-stage workflow needed a pure-CLI path for all three gates; S3 and S4 had subcommands, S2 did not; consistency closes the gap — serves "pure-CLI workflow for non-Claude agents"
- **MCP `--setup` output is agent-agnostic (removed VS Code/Copilot framing)** — the server is a generic MCP stdio server; naming a specific client in the setup output is misleading — serves "any MCP-compatible client"

## v0.8.0 (Epic 6 — Multi-surface / architecture)

- **`mbb_ppt/gates.py` as importlib facade over gate scripts** — gate scripts stay standalone CLI tools (tests and docs reference them by path); `gates.py` is the clean package-level seam for any surface adapter; `__main__.py` loses 108 lines of path-hacking in exchange — serves multiplatform goal
- **MCP protocol implemented directly (~200 lines), not via `mcp` SDK** — avoids a new runtime dep on a still-maturing SDK; JSON-RPC 2.0 over stdio is stable and well-specified; add the SDK if the protocol surface grows materially — serves "no unrequested dependencies"
- **Surface adapter creates only the MCP server; Cowork and CLI surfaces left as existing code paths** — CONTEXT.md install-story constraint forbids touching `install.py`; Cowork and CLI already work; ZoComputer requires API/prompt injection rather than a Python module — any ZoComputer adapter belongs in documentation, not a Python class — serves "additive, not a fork"
- **Dead `_LANG_REPLACEMENTS` / `_fix_language()` removed from `review.py`** — iterated over an empty dict; removed at source rather than leaving inert code — serves codebase health
- **`AutoFixPipeline.run()` default corrected to `max_rounds=1`** — was accidentally set to 3 from initial implementation; DECISIONS.md already said cap at 1 round — aligns code with existing decision
- **`DeckBuilder.build_from_module()` deleted** — zero callers anywhere in the codebase; deletion test passed — serves "fewest lines possible"

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
