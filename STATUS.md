# STATUS — MBB PPT Generator

> **Next run starts here.** v0.8.0 shipped 2026-06-22. Epic 6 architecture foundation is done (gates module + surface adapter + MCP server). Open Epic 6 items: GitHub Copilot end-to-end validation, ZoComputer surface documentation, SKILL.md MCP section. Read RESUME.md and CONTEXT.md before starting.

---

## Current state

- **Version:** `0.8.0`
- **Latest tag:** `v0.8.0`
- **Tests:** 48/48 passing
- **CI:** green on main (tests + leakage scan)
- **Working tree:** clean

## What shipped in v0.8.0 (2026-06-22)

| Commit | What landed |
|---|---|
| ponytail cleanup | Dead `_LANG_REPLACEMENTS` / `_fix_language()` removed from `review.py`. `AutoFixPipeline.run()` default corrected to `max_rounds=1`. `DeckBuilder.build_from_module()` deleted (zero callers). Stale docs archived to gitignored `archive/`. |
| arch B: gates into package | New `mbb_ppt/gates.py` — importlib facade exposing `run_storyboard_gate`, `run_content_gate`, `run_render_gate`, `run_render_gate_autofix`. `__main__.py` loses ~108 lines of path-hacking. |
| arch A: surface adapter | New `mbb_ppt/surfaces/` package. `mcp_server.py` is a ~200-line MCP JSON-RPC 2.0 stdio server exposing all four gates + render as MCP tools. Run `--setup` to get config snippets for Claude Code and VS Code/Copilot. |

## Open items after this run

- **Epic 6 remaining:** GitHub Copilot end-to-end validation (test `mcp_server.py` with a real Copilot session), ZoComputer surface documentation, SKILL.md section for MCP setup.
- **Degunk backlog:** #7–#14 still deferred.

## What's next

**Complete Epic 6** — validate the MCP surface with GitHub Copilot, document ZoComputer integration approach, add MCP setup section to SKILL.md or README. See ROADMAP.md.
