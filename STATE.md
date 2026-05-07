# MBB PPT Generator — Project State

> **Pause point: 2026-05-07.** When albertojb says "resume the MBB PPT skill" (or anything similar), read this file first. Resume instructions are in § 6 below.

---

## 1. What this project is

Albertojb is building **MBB PPT Generator**, an Apache 2.0-licensed adaptation of [Kaku Li / likaku's `Mck-ppt-design-skill`](https://github.com/likaku/Mck-ppt-design-skill). The fork is fully credited (Apache 2.0 chain preserved) and modernized:

- English-only (CJK guidance, defaults, prompts all removed).
- DM Sans heading font (Inter substitute, Calibri fallback) replacing Georgia.
- Engine documented as **ExecEngine** (the underlying module `mck_ppt` and class `MckEngine` stay, treated as implementation detail).
- Five-stage workflow (S1 brief → S2 outline → S3 content → S4 render+QA → S5 deliver).
- Two machine-readable gates: S3 content gate, S4 render gate. `passed` is a Python boolean derived from program logic — never a verbal claim.
- Self-Refinement loop with append-only `experiences/` directory.
- **Self-contained** — albertojb's team installs only this folder; no dependency on Likaku's separate skill installation.
- **Goal:** publish on GitHub and skill marketplaces. **0.1.0 is tagged and ready to push.**

---

## 2. Current status — what's done

The skill is at **0.1.0, fully feature-complete and committed to git.**

### Top-level files
| File | Status |
|---|---|
| `SKILL.md` | ✅ |
| `README.md` | ✅ GitHub-ready |
| `LICENSE` | ✅ Apache 2.0 (verbatim from upstream) |
| `NOTICE` | ✅ Full attribution chain with enumerated modifications |
| `CHANGELOG.md` | ✅ 0.1.0 release notes |
| `MBB_PPT_QA_CHECKLIST.md` | ✅ § 0 gate-script gate at top |
| `STATE.md` | ✅ this file |
| `.gitignore` | ✅ excludes `_likaku_*/`, `*.zip`, project artifacts |

### Engine (`mck_ppt/`)
| File | Status | Notes |
|---|---|---|
| `__init__.py` | ✅ | Exposes `MckEngine`, constants, `SlideReviewer`, `AutoFixPipeline`, lazy `generate_cover_image`. |
| `constants.py` | ✅ | DM Sans typography, content boundary (Rule 15), page-num lock (Rule 18), guard-rail constants, new colors. |
| `core.py` | ✅ | Drawing primitives. CJK-free. |
| `engine.py` | ✅ | All 67 layout methods. CJK-free (30+ inline edits). $ prefix in `stacked_area` (was ¥). |
| `qa.py` | ✅ | `PptQA` class — used by render gate. CJK-free. |
| `deck_builder.py` | ✅ | Storyline-driven orchestration. |
| `review.py` | ✅ | User-facing strings translated; redundancy/compression regex patterns retained as documented no-ops for English text. |
| `cover_image.py` | ✅ | Opt-in cloud feature. Fully translated to English (metaphor map keyed on English business themes; English prompts to Hunyuan API). |
| `storylines/ai_enterprise.py` | ✅ | **Replaced** Likaku's 33-slide Chinese storyline with a 12-slide English MBB-style strategy review template demonstrating layout variety. Builds clean, both gates pass. |

### References (`references/`)
| Section | Status | Notes |
|---|---|---|
| `INDEX.md` | ✅ | Knowledge router. |
| `layout-matrix.yaml` | ✅ | Capacity matrix. |
| `team/` | ✅ | `brand-guide.md`, `presentation-convention.md`. |
| `framework/` | ✅ | `engine-api.md`, `guard-rails.md`, `planning-guide.md`. |
| `layouts/` | ✅ | **All 12 files done.** Total ~4,268 lines covering every layout. |
| `scripts/` | ✅ | `gate_check_content.py`, `gate_check_render.py`. Render gate self-locates the bundled engine. |

### Experiences (`experiences/`)
| File | Status |
|---|---|
| `overflow.md` | ✅ 6 entries |
| `layout-pitfalls.md` | ✅ 5 entries |
| `chart-limits.md` | ✅ 3 entries |

### Examples
| File | Status |
|---|---|
| `examples/minimal_example.py` | ✅ Runs end-to-end S3 → render → S4 with `passed: true`. |

### Git status
- Repo initialized on `main` branch.
- One commit: `98ccffb` — "Initial commit — MBB PPT Generator 0.1.0".
- Tag: `v0.1.0` annotated.
- 43 files tracked, ~4,200+ lines of layout reference + ~200KB engine source.
- Pre-publish: needs a remote (`git remote add origin ...`) and `git push -u origin main --tags`.

---

## 3. Verified working

- `from mck_ppt import MckEngine` resolves from project root.
- `HEADING_FONT == "DM Sans"`; all v2.0 constants accessible.
- 6-slide minimal_example.py renders → `gate_render.json` with `passed: true`, score 78/100.
- 12-slide storyline (`ai_enterprise.STORYLINE`) builds via `DeckBuilder.build()` with `passed: true`.
- Render gate self-locates the bundled engine via `_resolve_skill_root()` walker.
- All routing-table files exist; no missing-file warnings at any stage.
- CJK character count in critical engine paths: **0** (engine.py, core.py, constants.py, qa.py, deck_builder.py, cover_image.py, storylines/ai_enterprise.py). Only `review.py` retains 14 CJK lines, all of which are documented no-op regex patterns for Chinese text simplification (would never fire on an English deck).

---

## 4. What's left (all low priority — non-blocking for publish)

| Item | Priority | Notes |
|---|---|---|
| `git remote add origin` + `git push -u origin main --tags` | Medium | Needs albertojb's GitHub repo URL. Cannot do without credentials. |
| Skill marketplace submission | Medium | Specs vary by marketplace — depends which ones albertojb targets. |
| Replace residual `review.py` regex with English-aware equivalents | Low | Currently no-op for English text. Functional gap is small. |
| Add `pyproject.toml` for `pip install -e .` style installation | Low | Useful if albertojb wants to package as a pip-installable library. |
| Build a 2nd richer example (e.g. board-deck variant of the storyline) | Low | One example covers the basics; a second adds variety. |

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
- `mck_ppt/cover_image.py` and `mck_ppt/storylines/` are kept in the bundle — both are lazy-imported, no install-time penalty.
- `_likaku_*/` extracts and `*.zip` archives stay in the local working directory but are excluded from the public repo via `.gitignore`.
- `review.py` Chinese-targeting regex patterns are kept verbatim from upstream and documented as no-ops for English text. They preserve Likaku's original work in case a future bilingual fork wants them; they cause no harm to English users.
- Currency prefix in `stacked_area` y-axis labels: hardcoded `$`. A `currency_symbol` parameter is on the long-term backlog but not blocking 0.1.0.
- 12-slide `ai_enterprise.py` storyline is a **template**, not a finished deck — operators clone and edit before delivering.

---

## 6. How to resume

When albertojb says "resume the PPT work", "continue MBB-PPT", or anything along those lines:

1. **Read this `STATE.md` first.** Confirm with `ls /home/ajb/Projects/MBB-PPT-2/` and `cd /home/ajb/Projects/MBB-PPT-2 && git log --oneline`.
2. **Quote the priority queue back:**
   - (a) Push to GitHub once albertojb provides the remote URL.
   - (b) Skill marketplace submission once albertojb picks a target.
   - (c) Optional: pyproject.toml, second example, review.py English-aware patterns.
3. **Ask for time-box.** Most natural prompt forms: "what can you do in N minutes?", "let's push to GitHub", "build a board-deck example".
4. **Suggested first move if albertojb asks "what's next":** push to GitHub. The codebase is 0.1.0-tagged and ready; only the remote URL is missing. ~5 min once URL is provided.
5. **Do NOT regenerate or re-edit completed files** unless albertojb explicitly asks. Files in § 2 marked ✅ are stable and committed.
6. **If asked about publishing:** the skill is publishable today. Tag `v0.1.0` is already created. The first push will create the GitHub repo from this clean state.

### Source materials (local, excluded from public repo via .gitignore)

- `_likaku_may3/Mck-ppt-design-skill-main/` — Likaku's `v2.3.3-harness-v2` release.
- `_likaku_harness/mck-harness-skill-upgrader-main/` — Likaku's harness meta-skill.
- `*.zip` — backup archives.
- `mbb-ppt-skill-review-prompt.md` — original task brief from albertojb's first session.
- `constants_update.py` — superseded by `mck_ppt/constants.py`.
