# STATUS — MBB PPT Generator

> **Next run starts here.** v0.8.1 shipped 2026-06-22. Epic 6 multi-agent deliverables done (AGENT.md + gate-storyboard CLI). Open Epic 6 items: GitHub Copilot end-to-end validation, ZoComputer surface documentation, SKILL.md MCP section. Read CONTEXT.md before starting.

---

## Current state

- **Version:** `0.8.1`
- **Latest tag:** `v0.8.1`
- **Tests:** 48/48 passing
- **CI:** green on main (tests + leakage scan)
- **Working tree:** clean

## What shipped in v0.8.1 (2026-06-22)

| Commit | What landed |
|---|---|
| feat | `AGENT.md` — generic agent instructions for any AI assistant without Claude-specific tooling. `gate-storyboard` CLI subcommand (pure-CLI path for all three gates). MCP `--setup` output is now agent-agnostic. |
| chore | Version bumped to 0.8.1 in all four locations. CHANGELOG updated. |

## What shipped in v0.8.0 (2026-06-22)

| Commit | What landed |
|---|---|
| ponytail cleanup | Dead `_LANG_REPLACEMENTS` / `_fix_language()` removed. `AutoFixPipeline.run()` default corrected to `max_rounds=1`. `DeckBuilder.build_from_module()` deleted (zero callers). |
| arch B: gates into package | New `mbb_ppt/gates.py` — importlib facade. `__main__.py` loses ~108 lines. |
| arch A: surface adapter | New `mbb_ppt/surfaces/mcp_server.py` — MCP JSON-RPC 2.0 stdio server, 4 tools. |

## Open items

- **Epic 6 remaining:** GitHub Copilot end-to-end validation (test `mcp_server.py` with a real MCP client), ZoComputer surface documentation, SKILL.md section for MCP setup.
- **Degunk backlog:** #7–#14 still deferred.

## What's next

**Complete Epic 6** — validate the MCP surface with a live MCP client, document ZoComputer integration, add MCP setup section to SKILL.md or README. See ROADMAP.md.
