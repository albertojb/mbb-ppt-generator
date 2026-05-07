# MBB PPT Generator — Project State

> **Pause point: 2026-05-07 afternoon.** When albertojb says "resume the MBB PPT skill" (or anything similar), read this file first. Resume instructions are in § 6 below.

---

## 1. What this project is

Albertojb is building **MBB PPT Generator**, an Apache 2.0-licensed adaptation of [Kaku Li / likaku's `Mck-ppt-design-skill`](https://github.com/likaku/Mck-ppt-design-skill). The fork is fully credited (Apache 2.0 chain preserved) and modernized:

- English-only (CJK guidance and rendered defaults removed).
- Modern neutral sans-serif heading font: DM Sans → Inter → Calibri fallback (replacing Georgia).
- Engine documented as **ExecEngine** (the underlying module `mck_ppt` and class `MckEngine` stay, treated as implementation detail).
- Five-stage workflow (S1 brief → S2 outline → S3 content → S4 render+QA → S5 deliver).
- Two machine-readable gates: S3 content gate and S4 render gate. `passed` is a Python boolean derived from program logic — never a verbal claim.
- Self-Refinement loop with append-only `experiences/` directory.
- **Self-contained** — albertojb's team installs only this folder; no dependency on Likaku's separate skill installation.
- **Goal:** publish on GitHub and skill marketplaces.

---

## 2. Current status — what's done

The skill is in a **publishable 0.1.0 state.** Render gate passes end-to-end. Every file the routing table requires (vs. recommends optionally) exists.

| Area | Status | Notes |
|---|---|---|
| Engine bundled | ✅ | `mck_ppt/` is a copy of upstream with copyright preserved. `constants.py` swapped to DM Sans, Rule 11–18 constants added. |
| Engine CJK sweep | ✅ | 27 inline edits replacing user-visible CJK defaults with English. Smoke-tested via render gate. |
| `SKILL.md` | ✅ | Renamed from MBB_PPT_SKILL_v2.md. Top-of-file Likaku attribution. Anti-patterns, HARD RULES, two iron laws, 5-stage workflow, Self-Refinement protocol, layout capacity table, retired-layout list. |
| `MBB_PPT_QA_CHECKLIST.md` | ✅ | § 0 gate-script gate at top; visual checklist secondary. |
| `LICENSE` (Apache 2.0) | ✅ | Copied verbatim from Likaku. |
| `NOTICE` | ✅ | Full attribution chain with enumerated modifications. |
| `README.md` | ✅ | Public-facing, GitHub-ready. |
| `CHANGELOG.md` | ✅ | Initial 0.1.0 release notes documenting fork divergence. |
| `.gitignore` | ✅ | Excludes `_likaku_*/`, `*.zip`, project artifacts, gate output JSON. |
| `references/INDEX.md` | ✅ | Knowledge router (stage → load map). |
| `references/layout-matrix.yaml` | ✅ | Capacity matrix with char_budget and tuple_arity per layout. |
| `references/team/brand-guide.md` | ✅ | English, DM Sans, ~85 lines. Loaded at S1. |
| `references/team/presentation-convention.md` | ✅ | English, content boundary, ~95 lines. Loaded at S4. |
| `references/framework/engine-api.md` | ✅ | Quick reference for 67 ExecEngine methods, ~213 lines. Loaded at S2. |
| `references/framework/guard-rails.md` | ✅ | Rules 1–18 with code examples and enforcement column, ~283 lines. Loaded at S3. |
| `references/framework/planning-guide.md` | ✅ | Storyboarding, narrative templates, layout-by-task selection, ~250 lines. Loaded optionally at S3. |
| `references/scripts/gate_check_content.py` | ✅ | S3 content gate, English. |
| `references/scripts/gate_check_render.py` | ✅ | S4 render gate. Self-locating (no hardcoded `~/.workbuddy` path). `ENGINE_BUG_WHITELIST` enum. |
| `experiences/overflow.md` | ✅ | 6 entries. |
| `experiences/layout-pitfalls.md` | ✅ | 5 entries. |
| `experiences/chart-limits.md` | ✅ | 3 entries. |
| `examples/minimal_example.py` | ✅ | End-to-end S3 gate → render → S4 gate demo on a 6-slide deck. Verified `passed: true`. |
| `references/layouts/structure.md` | ✅ | First Part C file. Covers `cover`, `toc`, `section_divider`, `closing`, `appendix_title` with signatures, wireframes, examples, pitfalls. ~340 lines. |
| `references/layouts/data-stats.md` | ✅ | Second Part C file. Covers `big_number`, `two_stat`, `three_stat`, `data_table`, `metric_cards`, `table_insight` (the editorial workhorse). Each layout has full signature, parameter table, wireframe, example, pitfalls. ~430 lines. |
| `references/layouts/narrative.md` | ✅ | Third Part C file. Covers `executive_summary`, `key_takeaway`, `four_column`, `two_column_text`, `quote`, `numbered_list_panel`. Notes hardcoded 'Synergy analysis' header in `key_takeaway` as a known UX issue. ~520 lines. |
| `references/layouts/charts-circular.md` | ✅ | Fourth Part C file. Covers `donut` (active) plus retirement notes for `pie` and `gauge`. Includes BLOCK_ARC mechanism explanation: angle convention, inner_ratio table. ~250 lines. |
| `references/layouts/charts-bar-line.md` | ✅ | Fifth Part C file. Covers `grouped_bar`, `stacked_bar`, `horizontal_bar`, `line_chart`. Highlights the line_chart caller-normalization gotcha (values must be 0.0–1.0 fractions of chart height). ~340 lines. |
| `references/layouts/charts-advanced.md` | ✅ | Sixth Part C file. Covers `waterfall`, `pareto`, `stacked_area`, `bubble`, `kpi_tracker`, `multi_bar_panel`. Includes 2 inline engine fixes: hardcoded `¥` currency in `stacked_area` y-axis labels and totals replaced with `$` (still hardcoded — proper fix is a `currency_symbol` parameter, on backlog). ~430 lines. |
| `references/layouts/frameworks.md` | ✅ | Seventh Part C file. Covers `matrix_2x2`, `swot`, `temple`, `pyramid`, `stakeholder_map`, `risk_matrix`. Notes the historical `label_cn`/`label_en` parameter naming in `stakeholder_map` (vestigial bilingual design). ~440 lines. |
| `references/layouts/comparison.md` | ✅ | Eighth Part C file. Covers `side_by_side`, `before_after` (rich+simple forms), `pros_cons`, `rag_status` (variable-length tuples), `scorecard` (auto-color thresholds). ~430 lines. |
| `references/layouts/timeline.md` | ✅ | Ninth Part C file. Covers all 7 process/timeline layouts: `timeline`, `vertical_steps`, `process_chevron`, `value_chain`, `decision_tree`, `agenda` (variable-arity items), `action_items`. Calls out the timeline last-label engine bug and the process_chevron `\n` constraint. ~530 lines. |
| `references/layouts/images.md` | ✅ | Tenth Part C file. Covers all 8 image layouts: `content_right_image`, `three_images`, `image_four_points`, `full_width_image`, `case_study_image`, `quote_bg_image`, `goals_illustration`, `two_col_image_grid`. Notes the placeholder workflow (operators replace gray boxes with real images post-generation). ~340 lines. |
| `references/layouts/special.md` | ✅ | Eleventh Part C file. Covers `icon_grid`, `checklist` (variable-arity rows + status_map), `harvey_ball_table` (0–4 score matrix), `meet_the_team`, `case_study` (S/A/R), `metric_comparison` (auto-color +/- deltas). ~430 lines. |
| `references/layouts/dashboards.md` | ✅ | Twelfth and final Part C file. Covers `dashboard_kpi_chart` (KPIs + chart + summary) and `dashboard_table_chart` (table + chart + factoids). Includes a "when to use vs. break apart" guidance section. ~250 lines. |

### What's pending

| Item | Priority | Estimated effort | Notes |
|---|---|---|---|
| ~~`examples/` directory~~ | ✅ done | — | `examples/minimal_example.py` runs S3 gate → render → S4 gate end-to-end on a 6-slide demo. `passed: true` verified. |
| ~~`references/layouts/*.md`~~ | ✅ COMPLETE | 12 of 12 files done | All Part C complete. ~4,200 lines of per-layout reference covering all 67 active engine methods plus retired layouts. |
| **CJK comments in `engine.py`** | Low | 5 min | Lines 68-70, 862, 864, 2994-2995. Comments and docstring examples only. Zero runtime impact. |
| **CJK in `mck_ppt/storylines/ai_enterprise.py`** | Low | Decide first | Whole file is a Chinese storyline template, opt-in only (not auto-loaded). Decide whether to translate, replace, or leave as a Likaku-original opt-in extra. |
| **CJK in `mck_ppt/cover_image.py`** | Low | Decide first | Tencent prompt strings, opt-in only. Same decision as above. |
| **GitHub setup** | When ready | 30 min | `git init`, push to remote, set up release tag for 0.1.0, push 0.1.0 release notes. |
| **Skill marketplace metadata** | When ready | TBD | Specs vary by marketplace; need to know which targets first. |

---

## 3. Repository inventory

```
mbb-ppt-generator/
├── SKILL.md                              # entry point
├── README.md                             # public-facing
├── LICENSE                               # Apache 2.0
├── NOTICE                                # attribution chain
├── CHANGELOG.md                          # 0.1.0 release notes
├── MBB_PPT_QA_CHECKLIST.md               # visual QA checklist
├── STATE.md                              # this file
├── .gitignore
│
├── mck_ppt/                              # bundled engine (Likaku's, Apache 2.0)
│   ├── __init__.py
│   ├── constants.py                      # DM Sans + v2.0 boundary/guard-rail constants
│   ├── core.py
│   ├── engine.py                         # 67 layout methods; CJK defaults replaced
│   ├── qa.py                             # PptQA — used by render gate
│   ├── deck_builder.py
│   ├── review.py
│   ├── cover_image.py                    # opt-in, Tencent SDK
│   └── storylines/
│       ├── __init__.py
│       └── ai_enterprise.py              # Chinese storyline, opt-in
│
├── references/
│   ├── INDEX.md                          # knowledge router
│   ├── layout-matrix.yaml                # capacity matrix
│   ├── team/
│   │   ├── brand-guide.md                # English, DM Sans
│   │   └── presentation-convention.md    # English, content boundary
│   ├── framework/
│   │   ├── engine-api.md                 # 67-method quick reference
│   │   ├── guard-rails.md                # Rules 1–18
│   │   └── planning-guide.md             # storyboarding + layout selection
│   ├── layouts/                          # ⏳ pending — Part C
│   └── scripts/
│       ├── gate_check_content.py         # S3 gate
│       └── gate_check_render.py          # S4 gate, self-locating
│
└── experiences/
    ├── overflow.md
    ├── layout-pitfalls.md
    └── chart-limits.md

# Local-only (excluded from GitHub via .gitignore):
├── _likaku_may3/                         # upstream extract — reference only
├── _likaku_harness/                      # upstream meta-skill — reference only
├── *.zip                                 # source archives
├── mbb-ppt-skill-review-prompt.md        # original task brief
└── constants_update.py                   # superseded by mck_ppt/constants.py
```

---

## 4. Verified working

- `from mck_ppt import MckEngine` resolves from project root with `sys.path.insert(0, '.')`.
- `HEADING_FONT == "DM Sans"`; all v2.0 constants accessible from `mck_ppt.constants`.
- Smoke decks render to `.pptx` (~30 KB for 3-slide deck).
- `gate_check_render.py` finds the bundled engine via `_resolve_skill_root()` walker — no `~/.workbuddy` dependency.
- Render gate JSON output: `passed: true`, score 93/100 on simple decks, 72/100 on `kpi_tracker`-heavy decks (latter has 3 whitelisted `engine_bug_errors`, expected).
- Routing table files all resolve: S1 reads `team/brand-guide.md`, S2 reads `framework/engine-api.md` + `layout-matrix.yaml`, S3 reads `framework/guard-rails.md` + `experiences/`, S4 optionally reads `team/presentation-convention.md`.

---

## 5. Decisions already made (do not relitigate)

- Skill name: **MBB PPT Generator**.
- Engine documented as **ExecEngine** (alias). Underlying module stays `mck_ppt`, class stays `MckEngine`.
- Heading font: **DM Sans** preferred, Inter equivalent, Calibri fallback. Body: Arial.
- English-only — no CJK guidance.
- Tencent cloud cover image: opt-in only, off by default.
- Apache 2.0 attribution to Likaku is **kept everywhere it appears** (file headers, NOTICE, README, CHANGELOG, SKILL.md). Albertojb is added as adapter, not as replacing author.
- Gate scripts use English error messages.
- `experiences/` is **append-only** — never delete entries; mark superseded ones with `Superseded by NNN`.
- Five retired layouts (Venn, Cycle, Funnel, Pie, Gauge) stay retired — methods exist for back-compat but are not promoted.
- `mck_ppt/cover_image.py` and `mck_ppt/storylines/` are kept in the bundle — both are lazy-imported, so no install-time penalty for the dependencies they would require.
- `_likaku_*/` extracts and `*.zip` archives stay in the local working directory but are excluded from the public repo via `.gitignore`.

---

## 6. How to resume

When albertojb says "resume the PPT work", "continue MBB-PPT", or anything along those lines:

1. **Read this `STATE.md` first.** Confirm the snapshot above still matches reality with `ls /home/ajb/Projects/MBB-PPT-2/`.
2. **Quote the priority order back to albertojb:** (a) `examples/` directory for marketplace readiness, then (b) Part C `references/layouts/*.md` files, then (c) any decisions on CJK opt-in files / GitHub push.
3. **Ask for time-box.** Most natural prompts: "what can you do in N minutes?" or "let's do (a)" or "do (a) and start (b)".
4. **Suggested first move for Part C continuation:** `layouts/data-stats.md` — covers `big_number`, `two_stat`, `three_stat`, `data_table`, `metric_cards`, `table_insight`. The most-used layout family by far (especially `table_insight`, the editorial workhorse). ~30–45 min for a quality file. After that, `narrative.md` (executive_summary, key_takeaway — highest-impact for slide 2–5 quality), then the chart trio (`charts-circular.md`, `charts-bar-line.md`, `charts-advanced.md`), then frameworks/comparison/process/images/special/dashboards.
5. **Do NOT regenerate or re-edit completed files** unless albertojb explicitly asks. Files in § 2 marked ✅ are stable.
6. **If asked about publishing:** the skill is publishable today. The remaining Part C files improve model quality but are not blockers for a 0.1.0 release. Tag `0.1.0` whenever albertojb is ready.

### Source materials (local reference, excluded from public repo)

- `_likaku_may3/Mck-ppt-design-skill-main/` — Likaku's `v2.3.3-harness-v2` release. Use for: extracting docstring text for layouts/, comparing against original behavior, sanity-checking attribution.
- `_likaku_harness/mck-harness-skill-upgrader-main/` — Likaku's separate harness meta-skill. Use for: principles reference only, do not copy.
- `*.zip` archives — backup of the above.
