# RESUME — pick-up doc for the next session

> **Purpose.** Give a fresh Claude session everything it needs to continue work on this skill without re-reading the entire history. Read this file first; everything else (`STATE.md`, `BACKLOG.md`, the post-mortem) is supporting detail.
>
> **Last updated.** 2026-05-09 by albertojb (with Claude Sonnet 4.5+).
>
> **Project root.** `/home/ajb/Projects/MBB-PPT-2/`
> **Public repo.** https://github.com/albertojb/mbb-ppt-generator
> **Latest tag.** `v0.5.4` on commit `b6d4870`. All v0.5.x milestones (0.5.0 → 0.5.4) shipped and pushed. Tests at 37/37 passing. CI green on `main`.
>
> **➡️ Next phase:** see [`HANDOFF.md`](./HANDOFF.md) — new layouts, layout-usage variability/consistency, and a speed/token/contradiction audit. That brief supersedes the v0.6.0 plan below as the immediate priority.

## v0.5.x summary (closed)

| Tag | Theme | What shipped |
|---|---|---|
| `v0.5.0` | Bug fixes + global gates | Bug A/B/C closed (value_chain / numbered_list_panel oval gates, harvey_ball_table widths). Two new global S3 checks: `executive_summary` capped at 15% of content slides, visual-density floor scales as `max(2, N // 4)`. |
| `v0.5.1` | Single source of truth | New `references/api-schemas.yaml` covers all 67 layouts. New `references/scripts/generate_cheatsheet.py` emits the cheatsheet. New `references/known-pitfalls.md`. Schema-driven structural validation in `gate_check_content.py`. Old `layout-matrix.yaml` deleted. |
| `v0.5.2` | Engine fixes | `cover()` redesigned (navy left-block + 36pt right pane, fits ~50 chars). `cover_centered()` preserves the legacy 44pt centered layout. Chart-subtitle duplication dropped from `grouped_bar` and `stacked_bar`. |
| `v0.5.3` | New layouts (1/2) | `ask`, `numbered_tiles`, `concept_three`, `journey_map`. |
| `v0.5.4` | New layouts (2/2) | `pyramid_staircase`, `cycle_4stage`, `index_callout`, `extension_rows`. All eight post-mortem § 4 layouts now in the engine. |

---

## 1. The two things the user cares about, in plain language

1. **Install must be brain-dead simple, no 30–40 minute spirals, no terminal demanded.** Solved as of the post-tag commits — keep the GUI `.skill` drop-in path and the STOP directive in `CLAUDE.md`. Do not regress to "Claude in Cowork runs install.py" — the Cowork sandbox blocks file writes outside session dirs and that path causes the 30–40 min token-burn loop.
2. **Layout variety. The deck output cannot look monotonous.** This is now the dominant priority. A real McKinsey deck team (post-mortem at `/home/ajb/claude-cowork-linux/mbb-ppt-skill-postmortem.md`) ran a 30-slide commercial-renewal deck through the skill and their custom python-pptx script. v1 used `executive_summary` 9 times in 30 slides; their v2 used 17 distinct layouts. Closing that gap is the v0.5 mission.

---

## 2. Where the install story currently stands (DO NOT REGRESS)

| Path | Audience | Status |
|---|---|---|
| **GUI drag-drop of `mbb-ppt-generator.skill`** from GitHub Releases (`/releases/latest/download/mbb-ppt-generator.skill`) | non-technical Cowork users (Mac/Windows/Linux) | **Primary path.** Built by user in commits `c83a338` → `f00778a` → `df0c726` → `85da8e5`. SKILL.md is at the zip root (Cowork's upload validator requires this). Single drop-in. |
| **One-line terminal install** (`python -c "import urllib...install.py"`) | terminal users | **Secondary path.** Same `install.py` we shipped in v0.4.2, now positioned as Option 2 in `CLAUDE.md`, not Option 1. |
| **`claude plugin marketplace add`** | Claude Code CLI only | **Avoid for Cowork.** Writes to `~/.claude/plugins/cache/` which is invisible to Cowork's GUI Skills sidebar. Documented in `CLAUDE.md` as "do NOT use for Cowork installs". |
| **Claude in Cowork runs install.py** itself | nobody | **DEAD END.** Cowork sandboxes block writes outside session dirs; agent burns 30–40 min and fails. `CLAUDE.md` opens with a hard `STOP — DO NOT attempt to install this from within a Cowork session.` directive. **Keep that directive.** |

What the user types in Cowork now (or tells Claude in any chat):

> *"Install the skill from https://github.com/albertojb/mbb-ppt-generator"*

Claude in Cowork reads `CLAUDE.md`, hits the STOP directive, delivers the user-facing message verbatim (GUI option + terminal option), then stops. User chooses one.

**If you're working on install in the next session: don't.** It's done. Touch only if a user reports a regression in the GUI drop-in or the terminal one-liner.

---

## 3. The post-mortem in 12 bullets

Full doc: `/home/ajb/claude-cowork-linux/mbb-ppt-skill-postmortem.md` (480 lines, very specific). The condensed version:

- **Layout monotony.** `executive_summary` is the most permissive layout, so the model funnels everything into it. v1 used it 9× in 30 slides. There's no penalty signal. **Highest-impact fix.**
- **Bug A — `value_chain`** gate falsely fails valid input. The engine renders `str(i+1)` in the oval but `gate_check_content.py` validates `stages[i][0]` (user's stage_title) against `MAX_OVAL_LABEL_CHARS=3`. Drop the `_check_oval_label` call. (~5-line fix.)
- **Bug B — `numbered_list_panel`** same pattern. Drop the `_check_oval_label` call. (~5-line fix.)
- **Bug C — `harvey_ball_table`** hardcodes `c1w + 4×colw = 12.8"` which overflows the 12.33" content width on every render. Parameterize widths.
- **Char-budgets vs render-geometry mismatches.** Matrix says 80 chars for `executive_summary.desc`; box only fits ~55. `cover.title` matrix says 40; box at 44pt fits ~25–30. Audit needed.
- **API parameter formats are opaque.** Cheatsheet shows method names + one-liner; not tuple arity, dict-key sets, color conventions, the 0–4 Harvey ball mapping. Operators read `engine.py` to write valid `content.json`. Single biggest productivity drag.
- **Cover layout is broken.** 11" wide × 44pt only fits ~30 effective chars; longer titles wrap and overflow by 100%+. v2 uses navy left-block + 7.8" wide × 36pt right pane (fits ~50 chars).
- **Workflow friction.** Many gate round-trips for issues that could auto-fix (text overflow ≤ 50%, body overflow ≤ 0.3").
- **No "ask" / decision-points layout.** Every renewal deck closes with one; operators fake it with `executive_summary`.
- **Storyboarding not enforced.** SKILL.md says skipping it is the #1 cause of bad decks. There's no S2 gate.
- **Section dividers visually quiet.** Three identical-looking dividers slide past unnoticed in a 30-slide deck.
- **Doc gaps.** The 3-char oval rule is in `gate_check_content.py` only — not in `api-cheatsheet.md` or the matrix. The "two_column_text max 1 per deck" rule similarly hidden.

---

## 4. Next milestone: v0.6.0 — process discipline (~1 week)

All of v0.5.x shipped. Next work is v0.6.0 (process discipline). Three tasks from the original plan:

| # | Task | Acceptance |
|---|---|---|
| 21 | **S2 storyboarding gate.** Print all slide titles in order; require operator to set `read_aloud_test: true` in `outline.json` after reading them aloud. | New `gate_check_storyboard.py`; S2 fails when the field is false or missing. |
| 22 | **Auto-fix mode on render gate.** For known patterns (text overflow ≤ 50%, body overflow ≤ 0.3"), shrink font 1pt or trim 5 chars and re-render once. Cap at 1 retry. | `gate_check_render.py --auto-fix` succeeds on a deck with one minor overflow without operator intervention. |
| 23 | **Stronger section_divider.** Top accent bar + 72pt numeral + 32pt title + 14pt italic subtitle. No content area, no source line. | A 30-slide deck with 3 section dividers reads visibly different from surrounding content. |

Tag as `v0.6.0`. Read post-mortem § 6 for design rationale before starting.

### Bonus follow-ups (deferred, low priority)

- Per-layout reference docs under `references/layouts/*.md` for the eight new v0.5.3/v0.5.4 layouts (one paragraph each).
- Deeper char-budget audit beyond the three known mismatches resolved in v0.5.1/v0.5.2.
- Tighter generator output: sort layouts by integer pattern (current sort is string-based to handle `'1b'`/`'23b'`/etc., which gives a stable but not numeric order).

---

## 5. Old v0.5 plan (kept for reference; all shipped)

Adapted from § 3 of the post-mortem. **All of v0.5 is layout-quality work.** Install is parked.

### v0.5.0 — kill the obvious bugs (1–2 days)

| # | Task | File | Effort | Acceptance |
|---|---|---|---|---|
| 1 | **Bug A — value_chain oval gate** | `plugins/mbb-ppt-generator/skills/mbb-ppt-generator/references/scripts/gate_check_content.py` line ~118 (`check_value_chain`) | 5 lines | Render a `value_chain` slide with `stages = [("Diagnose", "...", NAVY), ...]` (8-char title) — passes both gates. |
| 2 | **Bug B — numbered_list_panel oval gate** | same file, `check_numbered_list_panel` (line ~125) | 5 lines | `numbered_list_panel` with `items = [("Operating model", "..."), ...]` passes. |
| 3 | **Bug C — harvey_ball_table widths** | `plugins/mbb-ppt-generator/skills/mbb-ppt-generator/mbb_ppt/engine.py` line ~2404 | 20 min — add `first_col_w`, `opt_col_w` params with dynamic defaults | 4-option Harvey ball table renders without `body_overflow` errors. |
| 4 | **Cap `executive_summary` use** at ≤ 15% of content slides via S3 gate | `gate_check_content.py` (new global check) | 30 lines | Deck with 30 content slides and 5 `executive_summary` fails the gate; deck with 4 passes. Error message lists alternatives by content shape. |
| 5 | **Scale visual-density floor** linearly: `max(2, N // 4)` for N content slides | `gate_check_content.py` `check_visual_density_global` | 5-line edit | 30-slide deck requires 7+ visual layouts. |

Tag as v0.5.0.

### v0.5.1 — API schema as single source of truth (3–4 days)

| # | Task | File | Acceptance |
|---|---|---|---|
| 6 | **`references/api-schemas.yaml`** — every active layout's full param schema (tuple arity, dict keys, type hints, optional/required, color conventions, the 0–4 Harvey ball mapping) | NEW | 67 active layouts covered. Schema validated by a small smoke test. |
| 7 | **Generation script** that emits `references/api-cheatsheet.md` from the schema with a "Shape" column | NEW `references/scripts/generate_cheatsheet.py` | Run before each release; never hand-edit the cheatsheet again. |
| 8 | **`gate_check_content.py` reads the same schema** so a single edit updates both validation and docs | edit | Today's `LAYOUT_CHECKERS` dispatch is replaced by schema-driven validation for the structural checks (count, tuple arity, char budget). Custom checks (oval-label rules, the visual-density global) stay as code. |
| 9 | **`references/known-pitfalls.md`** — the 3-char oval rule, chart-subtitle re-render, cover wrap behavior, two_column_text global cap | NEW | One page, scan-readable, every implicit constraint documented in user-visible terms. |

Tag as v0.5.1.

### v0.5.2 — char-budget audit + cover redesign (2 days)

| # | Task | File | Acceptance |
|---|---|---|---|
| 10 | **Audit char-budgets** in `references/layout-matrix.yaml` against actual render geometry. Specific known mismatches: `executive_summary.desc` (80→55), `cover.title` (40→28), `process_chevron.step_label` (10→3 to match gate). | edit | Each entry has a comment linking to the engine line that imposes the geometry. |
| 11 | **Drop chart-subtitle duplication** in `grouped_bar` and `stacked_bar` — the 13pt sub-title rendered in a 5"×0.3" box overflows for any title >38 chars. The action title at the top is enough. | `engine.py` ~lines 1709 (grouped_bar) and ~1832 (stacked_bar) | Render both with a 110-char title; passes render gate. |
| 12 | **Cover redesign.** Navy left-block (4.5"×full) + right pane (7.8"×1" at 36pt). Optional: keep current cover as `cover_centered`. | `engine.py` cover() | "Commercial renewal: proposed offer for [client]" (45 chars) renders on one line, no overflow. |

Tag as v0.5.2.

### v0.5.3 — new layouts (3–4 days, one per push)

From post-mortem § 4. Each follows the existing engine pattern. Each ships with a schema entry, a one-paragraph addition to the relevant `references/layouts/<family>.md` file, and a 3-slide regression test deck.

| # | Layout | Use case | Reference |
|---|---|---|---|
| 13 | `numbered_tiles` (escalating fill) | Tiered offers, phased rollouts, escalating commitment. Three tiles side by side, gray → light blue → navy. | post-mortem § 4.1 |
| 14 | `concept_three` | 3-dimensional concepts (intent / cadence / value), 3-stage flows. Three large circles + arrows + descriptions. | § 4.3 |
| 15 | `pyramid_staircase` | Maturity progression. Five ascending steps, each wider than the last. (Engine has `pyramid` already; if it doesn't render as ascending steps, replace.) | § 4.4 |
| 16 | `cycle` (4-stage loop) | Continuous improvement, problem-management cycles. 2×2 grid with clockwise arrows. | § 4.5 |
| 17 | `index_callout` | "5 optional items, here's the one we're emphasizing." Numbered list left + detail panel right. | § 4.6 |
| 18 | `extension_rows` | Modular catalogs, scope extensions. Horizontal rows with vertical accent bar. | § 4.7 |
| 19 | `journey_map` | Customer journey, persona × metric. Chevron header + stakeholder/metric cards per stage. | § 4.8 |
| 20 | `ask` / `decision_points` | Closing slide. 3–5 numbered decisions: decision / owner / deadline / status. | § 4.10 |

Tag as v0.5.3.

### v0.6.0 — process discipline (1 week)

| # | Task | Acceptance |
|---|---|---|
| 21 | **S2 storyboarding gate.** Print all slide titles in order; require operator to set `read_aloud_test: true` in `outline.json` after reading them aloud. | `gate_check_storyboard.py` exists; S2 fails when the field is false or missing. |
| 22 | **Auto-fix mode on render gate.** For known patterns (text overflow ≤ 50%, body overflow ≤ 0.3"), shrink font 1pt or trim 5 chars and re-render once. Cap at 1 retry. | Render gate run with `--auto-fix` succeeds on a deck with 1 minor overflow without operator intervention. |
| 23 | **Stronger section_divider.** Top accent bar + 72pt numeral + 32pt title + 14pt italic subtitle. No content area, no source line. | A 30-slide deck with 3 section dividers reads visibly different from the surrounding content. |

Tag as v0.6.0.

---

## 5. Concrete first 5 minutes for the next session

Run these in order to confirm starting state:

```bash
cd /home/ajb/Projects/MBB-PPT-2

# 1. Confirm where we are
git log --oneline -8                         # should show v0.5.4 commit b6d4870 at HEAD
git status                                   # should be clean

# 2. Read this doc + the post-mortem (don't bulk-load other refs yet)
cat RESUME.md
cat /home/ajb/claude-cowork-linux/mbb-ppt-skill-postmortem.md

# 3. Tests pass on baseline
python3 -m pytest tests/                     # expect 37/37 passing

# 4. Pick ONE task from § 4 above. v0.6.0 #21 (S2 storyboarding gate) is the
#    smallest blast radius — start there.
```

For the next session's opening prompt to a fresh Claude:

> *"Resume MBB PPT work. Read /home/ajb/Projects/MBB-PPT-2/RESUME.md first; that's a single self-contained handoff doc. v0.5.x is fully shipped (37/37 tests; latest tag v0.5.4). Start with v0.6.0 task #21 — the S2 storyboarding gate. Quote the v0.6.0 task list back before writing any code so I can confirm the order."*

---

## 6. Things to NOT change (preserved-by-design)

- **Five-stage workflow** (S1 brief → S2 outline → S3 content → S4 render → S5 deliver). Validated by the post-mortem — it's the right discipline.
- **Machine-readable gates** with `passed: bool` derived in code. Don't soften this.
- **`full_cleanup()` on save.** Removes theme references that cause "File needs repair" prompts. Real value.
- **Append-only `experiences/*.md`.** Pattern for accumulating institutional knowledge across runs.
- **Apache 2.0 attribution chain to Kaku Li.** NOTICE / LICENSE / file-header copyrights stay verbatim. Upstream URL `https://github.com/likaku/Mck-ppt-design-skill` preserved.
- **Forest green primary, sans-serif typography, white background.** Sober palette. No reverting to McKinsey navy.
- **Cowork install story** (this section). The user has settled on GUI `.skill` drop-in + terminal one-liner; do not regress.
- **Module names.** `mbb_ppt`, `MbbEngine`, `ExecEngine` alias.

---

## 7. Open questions to ask the user before doing v0.5.x work

Surface these in the new chat so the priorities aren't relitigated:

1. **Sequence:** is the post-mortem priority order (P0 first, then P1, then new layouts) the right one, or is there a customer-driven slide that needs a specific layout sooner? (E.g. if the next deck the user is delivering is a maturity-assessment, prioritize `pyramid_staircase`.)
2. **Audience for v0.5:** ex-consultants (the original target) — anything new since the post-mortem we should know about (specific firms, deck types, languages other than English)?
3. **Schema file format:** YAML (`api-schemas.yaml`) vs. JSON Schema vs. Python dataclasses with type hints. YAML is what the post-mortem suggests; happy to confirm before writing.
4. **Auto-fix risk tolerance:** auto-fix on the render gate trims user content. OK if the gate output flags every auto-fix loudly?
5. **Section divider redesign:** 72pt numeral is bold. OK to go that big, or stay ≤ 48pt?

---

## 8. Pointers — where the actual code lives (post-tag layout)

```
/home/ajb/Projects/MBB-PPT-2/
├── CLAUDE.md                                                              ← agent install playbook (KEEP)
├── README.md                                                              ← user-facing
├── RESUME.md                                                              ← THIS FILE
├── STATE.md                                                               ← legacy state pointer (still valid)
├── BACKLOG.md                                                             ← legacy roadmap (superseded by § 4 here for v0.5)
├── CHANGELOG.md                                                           ← per-release notes
├── install.py                                                             ← cross-platform installer (SECONDARY path; keep)
├── install_cowork.sh                                                      ← legacy bash installer (kept as fallback)
├── mbb-ppt-generator.skill                                                ← GUI drop-in zip (PRIMARY path; rebuild on each release)
├── pyproject.toml                                                         ← package config
├── tests/                                                                 ← 22 pytest tests
├── examples/                                                              ← minimal/board_qbr/pitch_deck
└── plugins/mbb-ppt-generator/
    ├── .claude-plugin/plugin.json                                         ← plugin manifest
    └── skills/mbb-ppt-generator/                                          ← THE SKILL ITSELF
        ├── SKILL.md                                                       ← operator entry point
        ├── MAINTAINERS.md
        ├── mbb_ppt/                                                       ← engine (Python)
        │   ├── engine.py                                                  ← 67 layout methods
        │   ├── core.py                                                    ← drawing primitives (add_oval lives here)
        │   ├── constants.py                                               ← colors, fonts, page geometry
        │   ├── qa.py                                                      ← post-render QA
        │   └── ...
        ├── references/
        │   ├── api-cheatsheet.md                                          ← REGENERATE in v0.5.1
        │   ├── layout-matrix.yaml                                         ← AUDIT in v0.5.2
        │   ├── api-schemas.yaml                                           ← NEW in v0.5.1
        │   ├── known-pitfalls.md                                          ← NEW in v0.5.1
        │   ├── framework/                                                 ← engine-api, guard-rails, planning-guide
        │   ├── layouts/                                                   ← 12 per-family reference files
        │   └── scripts/
        │       ├── gate_check_content.py                                  ← Bug A & B fixes here
        │       ├── gate_check_render.py
        │       └── generate_cheatsheet.py                                 ← NEW in v0.5.1
        └── experiences/                                                   ← append-only learning corpus
```

---

## 9. Files referenced by the post-mortem (for line-number lookups)

The post-mortem cites these specific lines. Verify they're still accurate when picking up tasks:

- `mbb_ppt/engine.py:1653` — `value_chain` definition (Bug A)
- `mbb_ppt/engine.py:2923` — `numbered_list_panel` definition (Bug B)
- `mbb_ppt/engine.py:2404` — `harvey_ball_table` definition (Bug C)
- `mbb_ppt/engine.py:1235` — `three_stat` (third tuple slot is `is_navy:bool`, undocumented)
- `gate_check_content.py:check_value_chain` — has the bad `_check_oval_label` call
- `gate_check_content.py:check_numbered_list_panel` — same
- `gate_check_content.py:check_visual_density_global` — for the linear scaling fix

(The path prefix is now `plugins/mbb-ppt-generator/skills/mbb-ppt-generator/` for engine.py and `plugins/mbb-ppt-generator/skills/mbb-ppt-generator/references/scripts/` for the gate scripts. Post-mortem uses the pre-restructure paths.)

---

*End of resume doc.*
