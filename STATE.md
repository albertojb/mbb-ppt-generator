# MBB PPT Generator — Project State

> **Pause point: 2026-05-07 (v0.2.0 rebrand).** When albertojb says "resume the MBB PPT skill" (or anything similar), read this file first. Resume instructions are in § 6 below.

---

## 1. What this project is

Albertojb is building **MBB PPT Generator**, an Apache 2.0-licensed adaptation of [Kaku Li / likaku's `Mck-ppt-design-skill`](https://github.com/likaku/Mck-ppt-design-skill). The fork is fully credited (Apache 2.0 chain preserved) and modernized:

- English-only (CJK guidance, defaults, prompts all removed).
- DM Sans heading font (Inter substitute, Calibri fallback) replacing Georgia. Body Arial. Both sans-serif.
- **Primary color forest green `#1B4332`** (McKinsey-style navy retired). Sober muted accents (slate, olive, rust, burgundy). White page background.
- Engine module **`mbb_ppt`**, class **`MbbEngine`**, public alias **`ExecEngine`** (rename from upstream `mck_ppt` / `MckEngine` in v0.2.0).
- Five-stage workflow (S1 brief → S2 outline → S3 content → S4 render+QA → S5 deliver).
- **`mbb-ppt` CLI** (`render` / `gate-content` / `gate-render` / `version`) so non-technical operators can invoke the skill via Cowork: "use the MBB skill on this file" → no Python or sed required.
- Two machine-readable gates: S3 content gate, S4 render gate. `passed` is a Python boolean derived from program logic — never a verbal claim.
- Self-Refinement loop with append-only `experiences/` directory.
- **Self-contained** — pip-installed (`pip install -e ~/.claude/skills/mbb-ppt-generator`); no dependency on Likaku's separate skill installation.
- **Status:** **0.2.0 in progress (rebrand + Cowork UX).** Published at https://github.com/albertojb/mbb-ppt-generator (public, Apache 2.0, topics + description set).

---

## 2. Current status — what's done

### v0.2.0 — rebrand + Cowork-first UX (this round)

| Change | Status |
|---|---|
| Module rename `mck_ppt` → `mbb_ppt` (preserving Apache 2.0 file-header copyrights) | ✅ |
| Class rename `MckEngine` → `MbbEngine`; `ExecEngine` exported as alias | ✅ |
| Self-resolving install path (no `~/.workbuddy/...` hardcoded; pip-installable; SKILL.md documents `~/.claude/skills/mbb-ppt-generator/`) | ✅ |
| Tencent Hunyuan cover-image (`cover_image.py`) and `[cloud]` pip extra deleted | ✅ |
| Primary color `NAVY` value swapped from `#051C2C` to `#1B4332` (forest green); accent palette retuned (slate/olive/rust/burgundy) | ✅ |
| `references/api-cheatsheet.md` — single-file method index loaded at S2 | ✅ |
| `mbb_ppt/__main__.py` CLI (`mbb-ppt render/gate-content/gate-render/version`) with `[project.scripts]` entry point | ✅ |
| HARD RULE 0 added to SKILL.md — operator-friendly invocation; forbid grepping engine source | ✅ |
| Harness pedagogy ("Iron law 1/2") moved from SKILL.md to MAINTAINERS.md | ✅ |
| All `mck`/`mckinsey`/`tencent`/`workbuddy`/`hunyuan`/`clawhub` non-attribution references scrubbed | ✅ |
| README + CHANGELOG + NOTICE + STATE updated | ✅ |
| All 15 tests pass with new module name + version | ✅ |
| `examples/minimal_example.py` and `examples/board_qbr_example.py` render cleanly with both gates passing | ✅ |
| `mbb-ppt render` CLI smoke-tested with `ppt-project-demo/content.json` — both gates pass | ✅ |

### v0.1.0 — initial fork (still in place)

All v0.1.0 deliverables remain:

- 51 files tracked; 15 passing tests; 3 working examples; ~4,200 lines of layout reference; 12 per-layout files; 12-slide storyline; both gate scripts.
- Apache 2.0 attribution preserved everywhere it appeared.

---

## 3. Verified working (post-v0.2.0)

- `from mbb_ppt import MbbEngine, ExecEngine` resolves; `__version__ == '0.2.0'`.
- `NAVY == PRIMARY == #1B4332` (forest green).
- `pytest` → 15/15 passing.
- `python examples/minimal_example.py` → score 78/100, passed: true.
- `python examples/board_qbr_example.py` → score 98/100, passed: true.
- `python -m mbb_ppt render <content.json>` → both gates pass.
- `python -m mbb_ppt gate-content <content.json>` → exit 0, prints PASS.
- `python -m mbb_ppt gate-render <deck.pptx>` → exit 0, prints PASS.

---

## 4. What's left

**See [`BACKLOG.md`](BACKLOG.md) for the comprehensive roadmap.** Highest-priority items:

- **Round 3 (deferred from v0.2.0 session)** — visual variety + layout-selection guidance + visual-density gate. The user's #1 complaint after the AcademyOS run was "underwhelming, just a bunch of text in columns". Add: content-pattern → layout-family table to S2; visual-density gate requiring ≥ 2 chart/diagram/image layouts in 6+ slide decks.
- **Tier 1 — Engine correctness (~2 hrs)**: hardcoded `'Synergy analysis'` header in `key_takeaway`, hardcoded `scorecard`/`stacked_area` defaults, no-op auto-fix in `review.py` for English text, `set_ea_font` XML noise.
- **Tier 3 — Docs polish**: screenshots, architecture diagram, AI-agent integration walkthrough, CONTRIBUTING/CODE_OF_CONDUCT.
- **Tier 4 — CI**: GitHub Actions running pytest + leakage grep on every push.
- **Tier 5 — Marketplace publishing**: Claude Code skill marketplace, PyPI.

---

## 5. Decisions already made (do not relitigate)

- Skill name: **MBB PPT Generator**.
- Engine module: **`mbb_ppt`**. Class: **`MbbEngine`**. Public alias: **`ExecEngine`**. (v0.2.0 rebrand.)
- Heading font: **DM Sans** preferred, Inter equivalent, Calibri fallback. Body: Arial. Both sans-serif.
- Primary color: **forest green `#1B4332`** (`NAVY` and `PRIMARY` both point at this). Sober muted accents.
- English-only — no CJK guidance.
- **Tencent / Hunyuan cover-image integration is deleted** (not "opt-in" — fully removed in v0.2.0).
- **No `~/.workbuddy/` references anywhere** — install path is `~/.claude/skills/mbb-ppt-generator/`.
- Apache 2.0 attribution to Kaku Li / likaku is **kept everywhere it appears** (file headers, NOTICE, README, CHANGELOG, SKILL.md). The upstream URL `https://github.com/likaku/Mck-ppt-design-skill` is preserved verbatim.
- Gate scripts use English error messages.
- `experiences/` is **append-only** — never delete entries; mark superseded ones with `Superseded by NNN`.
- Five retired layouts (Venn, Cycle, Funnel, Pie, Gauge) stay retired — methods exist for back-compat but are not promoted.
- 12-slide `ai_enterprise.py` storyline is a **template**, not a finished deck.
- Cowork-first invocation: HARD RULE 0 forbids grepping engine source or writing inline Python for gates. Use `mbb-ppt` CLI + `references/api-cheatsheet.md`.

---

## 6. How to resume

When albertojb says "resume the PPT work", "continue MBB-PPT", or anything along those lines:

1. **Read this `STATE.md` first.** Confirm with `ls /home/ajb/Projects/MBB-PPT-2/` and `cd /home/ajb/Projects/MBB-PPT-2 && git log --oneline | head`.
2. **Quote the priority queue back:**
   - (a) Round 3 (visual variety + layout-selection guidance + visual-density gate) — the user's main concern after the v0.2.0 rebrand. Pending.
   - (b) Tier 1 engine correctness fixes (~2 hrs).
   - (c) GitHub Actions CI (~30 min).
3. **Ask for time-box.**
4. **Do NOT regenerate or re-edit completed files** unless albertojb explicitly asks. Files in § 2 marked ✅ are stable and committed.

### Source materials (local, excluded from public repo via .gitignore)

- `_likaku_may3/Mck-ppt-design-skill-main/` — Likaku's `v2.3.3-harness-v2` release.
- `_likaku_harness/mck-harness-skill-upgrader-main/` — Likaku's harness meta-skill.
- `*.zip` — backup archives.
- `mbb-ppt-skill-review-prompt.md` — original task brief from albertojb's first session.
- `mbb skill vs mck skill` — albertojb's session log comparing v0.1.0 output to upstream.
- `constants_update.py` — superseded by `mbb_ppt/constants.py`.
