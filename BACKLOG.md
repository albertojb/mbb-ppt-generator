# MBB PPT Generator — Backlog & Roadmap

> **For a fresh chat session.** This file is self-contained: read it once and you can pick up where the prior chat left off without reading any conversation history. It captures gaps, recommended sequencing, open strategic questions, and the exact "first 5 minutes" to verify you're starting from the right place.
>
> Lives at: https://github.com/albertojb/mbb-ppt-generator (also locally at `/home/ajb/Projects/MBB-PPT-2/`)

---

## 1. Where the project is right now (0.1.0 published)

- **Repo**: [albertojb/mbb-ppt-generator](https://github.com/albertojb/mbb-ppt-generator), public, Apache 2.0
- **Tag**: `v0.1.0` on commit `98ccffb` (initial commit)
- **HEAD**: `bec3e3f` (post-tag packaging + tests + second example)
- **51 files tracked**, ~4,200 lines of layout reference + ~200 KB engine source + 15 passing tests
- **Self-contained**: bundles Likaku's `mck_ppt/` engine (Apache 2.0); no external skill installation needed
- **English-only** (CJK swept from engine, defaults, prompts, comments)
- **Heading typography**: DM Sans → Inter → Calibri fallback
- **5-stage workflow**: brief → outline → content → render+QA → deliver, with two machine-readable gates whose `passed` is a Python boolean derived from program logic, never a verbal claim
- **Tests**: 15 passing — package import, render integrity, layout families, both gates' pass/fail logic
- **Examples**: 3 runnable demos (minimal_example.py, board_qbr_example.py, the bundled storyline) — all render with `passed: true`
- **Documentation**: SKILL.md + README.md + 12 per-layout reference files + 3 framework files + 2 team files + INDEX.md + 3 experiences files + STATE.md + this file

### What's NOT done (the reason this file exists)

Six tiers of gaps were identified in the prior chat. Tier 1 (engine correctness) has real defects that should be fixed before public marketplace submission. Tiers 2–6 are progressive polish.

---

## 2. First 5 minutes for a fresh chat

Before doing any work, run these to verify your starting state matches:

```bash
cd /home/ajb/Projects/MBB-PPT-2

# 1. State check
git log --oneline --decorate | head -5
# Expected: bec3e3f → dc9312d → f57e091 → 98ccffb (tag: v0.1.0)
git status   # should be clean

# 2. Tests pass
python3 -c "
import sys, tempfile
from pathlib import Path
sys.path.insert(0, '.')
def _t(): d=Path(tempfile.mkdtemp(prefix='mbb_')); p=d/'p'; p.mkdir(); return p
PR=Path('.').resolve()
from tests import test_smoke, test_layouts, test_gates
n=p=0
for mod in [test_smoke, test_layouts, test_gates]:
    for name in dir(mod):
        if not name.startswith('test_'): continue
        n+=1
        try:
            import inspect
            args=[(_t() if x=='tmp_project_dir' else PR) for x in inspect.signature(getattr(mod,name)).parameters]
            getattr(mod,name)(*args); p+=1
        except Exception as e: print(f'FAIL {name}: {e}')
print(f'{p}/{n} tests passed')
"
# Expected: 15/15 tests passed

# 3. Examples render
python3 examples/minimal_example.py 2>&1 | tail -3
python3 examples/board_qbr_example.py 2>&1 | tail -3
# Expected: both DELIVERED with passed: true

# 4. Read the lightweight pointer
cat STATE.md   # current pause point + recent commits
```

If any of these fail, **stop and diagnose before proceeding.** Don't do new work on a broken baseline.

### Where to look for context

| File | Purpose |
|---|---|
| `SKILL.md` | The skill specification — what the skill does, how it works, all 18 guard rails |
| `README.md` | Public-facing entry point with quickstart |
| `CHANGELOG.md` | 0.1.0 release notes documenting fork divergence |
| `STATE.md` | Lightweight pause-point pointer (changes per session) |
| `BACKLOG.md` | **This file** — the rich roadmap (stable across sessions) |
| `NOTICE` | Apache 2.0 attribution chain (Kaku Li → albertojb) |
| `references/INDEX.md` | Routing table — what to load at each stage |
| `references/layouts/*.md` | 12 per-layout reference files (4,200 lines covering 67 active layouts) |
| `mck_ppt/engine.py` | The 67-method layout library (~3,200 lines) |

---

## 3. Open strategic questions (need albertojb input before deciding)

These are not "do work" tasks — they're decisions that shape later work. Surface these to albertojb in the new chat before committing to a plan.

| Question | Why it matters |
|---|---|
| **Who is the primary user?** AI agents writing decks autonomously, humans who want a Python library, or consultants who want a sample-deck library? | Each implies different documentation, different examples, different marketplaces. |
| **What's the differentiator vs. raw `python-pptx`?** | python-pptx alone could do everything. The value-add is the design system + harness + gates. README touches this but doesn't articulate it concisely. |
| **What's the differentiator vs. AI tools that generate slides directly** (Gamma, Beautiful.ai, Pitch)? | Those are end-to-end consumer tools. This skill is for someone who wants programmatic control + version control + diff-able decks. Narrow but real audience. |
| **Which marketplaces are the targets?** Claude Code skill marketplace, ClawHub, WorkBuddy, PyPI, all of them? | Each has different submission formats, manifests, metadata requirements. Tier 5 below is gated on this. |
| **Long-term scope: chart library? Presentation framework? AI deck-design DSL?** | Decisions about scope inform what makes 0.2.0 vs. 1.0.0 vs. "out of scope, decline the feature request." |

---

## 4. The backlog (six tiers)

Estimated total ~12 hours of focused work to go from "tagged 0.1.0" to "I'd be proud to point anyone at this." Recommendation: do tiers in order, but tiers 2–4 can run partially in parallel.

### Tier 1 — Engine correctness gaps (REAL defects; fix before public marketplace)

| # | Gap | File | Effort | Recommendation |
|---|---|---|---|---|
| 1.1 | `key_takeaway` hardcoded `'Synergy analysis'` left header | `mck_ppt/engine.py` line ~1134 | 15 min — add `left_title` parameter with sensible default | **Fix.** Visible defect on a high-impact layout. |
| 1.2 | `scorecard` hardcoded `['Domain', 'Score', 'Maturity']` headers | `mck_ppt/engine.py` line ~476 | 10 min — add `headers` parameter | **Fix.** Trivial. |
| 1.3 | `stacked_area` hardcoded `$` currency in y-axis labels and totals | `mck_ppt/engine.py` lines ~2506, 2522 | 10 min — add `currency_symbol='$'` parameter | **Fix.** |
| 1.4 | `review.py` redundancy/compression regex are no-ops for English | `mck_ppt/review.py` lines 318–337 | 60–90 min — write English equivalents (hedging removal, compression patterns, jargon replacements) | **Fix or document as "experimental, Chinese-only".** Currently misleading: `AutoFixPipeline` is exposed, advertised in docstrings, does nothing useful for English decks. |
| 1.5 | 5 whitelisted `engine_bug_errors` per render | `references/scripts/gate_check_render.py` ENGINE_BUG_WHITELIST + `mck_ppt/engine.py` (the layouts that trigger them) | 30–45 min investigation | **Investigate.** Confirm `peer_font_inconsistency` is truly intentional design; if so, document each instance with an inline comment in `engine.py` linking to the rationale. The current whitelist comment is generic. |
| 1.6 | `set_ea_font` writes `'Arial'` to East Asian font slot on every text run | `mck_ppt/core.py` lines 61–68 | 20–30 min — make `set_ea_font` a true no-op when `typeface == BODY_FONT`, OR remove the function entirely (engine code that calls it would also need adjustment) | **Fix.** Generates pointless XML noise. |
| 1.7 | `_LANG_REPLACEMENTS = {}` dead variable | `mck_ppt/review.py` line 315 | 2 min — remove | Easy cleanup. |
| 1.8 | `mck_ppt/storylines/__init__.py` is empty | `mck_ppt/storylines/__init__.py` | 5 min — add proper exports / docstring | Idiomatic cleanup. |

**Total Tier 1: ~3 hours.**

After Tier 1, bump version to 0.1.1 (or move v0.1.0 tag forward if not yet pushed — but it IS now pushed, so use 0.1.1).

### Tier 2 — Test coverage depth

15 tests is a starting point. Coverage is shallow — most layout tests just assert "renders without error".

| # | Gap | Effort |
|---|---|---|
| 2.1 | Unit tests for `PptQA` itself (currently only tested through render gate) | 60 min |
| 2.2 | Tests for guard rails 11, 13, 14, 15, 16, 17, 18 specifically (currently documented but not asserted) | 45 min |
| 2.3 | Tests for `DeckBuilder` error paths (invalid `type`, missing `data` key) | 20 min |
| 2.4 | Test that asserts `eng.save()` strips theme shadows / 3D effects (currently only p:style strip is asserted) | 15 min |
| 2.5 | Smoke tests for `multi_bar_panel`, `bubble`, `decision_tree`, `agenda` (documented but never test-rendered) | 30 min |
| 2.6 | Tests for the `experiences/` self-refinement loop (verify append + parse) | 30 min |
| 2.7 | Coverage measurement via `pytest --cov` — set a target (e.g., 70%) | 10 min |

**Total Tier 2: ~3.5 hours.**

### Tier 3 — Documentation gaps

Marketplace polish.

| # | Gap | Effort |
|---|---|---|
| 3.1 | **Screenshot or visual** of generated output in README — single biggest first-impression lever | 20 min — generate a deck, screenshot 3 slides, add to README |
| 3.2 | "Why this skill?" comparison vs. alternatives (raw python-pptx, Gamma, Beautiful.ai, Pitch, Marp, Slidev) | 30 min |
| 3.3 | AI agent integration guide (concrete examples for Claude Code, WorkBuddy, ClawHub) | 45 min |
| 3.4 | Troubleshooting / FAQ section | 30 min |
| 3.5 | Architecture diagram (Mermaid or ASCII) showing the 5-stage workflow + 14 files involved | 30 min |
| 3.6 | `CONTRIBUTING.md` — how to file issues, run tests, propose features | 20 min |
| 3.7 | `CODE_OF_CONDUCT.md` — adopt Contributor Covenant | 5 min |
| 3.8 | `SECURITY.md` — vulnerability disclosure policy | 10 min |
| 3.9 | `.github/ISSUE_TEMPLATE/` and `PULL_REQUEST_TEMPLATE.md` | 15 min |
| 3.10 | MkDocs / Sphinx setup for browsable HTML docs (deploy to GitHub Pages) | 60–90 min |
| 3.11 | Per-layout rendered-screenshot previews (60 layouts × small thumbnail) — **diminishing returns; consider skipping** | 90 min |

**Total Tier 3 (skipping 3.11): ~5 hours.**

### Tier 4 — Process / tooling

| # | Gap | Effort |
|---|---|---|
| 4.1 | GitHub Actions CI — run `pytest` on push and PR | 20 min — `.github/workflows/test.yml` |
| 4.2 | Linting setup — `ruff` config + `pre-commit` hook | 15 min |
| 4.3 | Build artifact verification — `python -m build` produces a clean wheel | 30 min |
| 4.4 | Version bump automation — `bump-my-version` or `setuptools_scm` | 30 min |
| 4.5 | Dependency vulnerability scanning — Dependabot config | 10 min |
| 4.6 | Type hints across 67 engine methods (NOT recommended — separate project; ~10–20 hours) | — |

**Total Tier 4 (skipping 4.6): ~2 hours.**

### Tier 5 — Marketplace publishing

Depends entirely on which marketplaces are targeted. **Confirm targets in §3 before doing this work.**

| Marketplace | What's needed | Effort |
|---|---|---|
| GitHub | ✅ Already done. | — |
| PyPI | Name reservation check, `python -m build`, `twine upload`. Metadata already correct. | 30 min |
| Claude Code skill marketplace | Probably needs a `.claude-skill.yaml` manifest. **Research current spec first.** | Unknown |
| WorkBuddy | Unknown format. **Research first.** | Unknown |
| ClawHub | Unknown format. **Research first.** | Unknown |
| Hugging Face Spaces (optional) | Could host a deck-generation demo Space. | 60 min |
| AI agent install instructions | Parallel install paths in README for Claude Code, etc. | 30 min |

**Total Tier 5: 1–4 hours depending on targets.**

### Tier 6 — Strategic positioning

The biggest non-obvious gap. Without these, the technical work might be wasted on the wrong audience.

| # | Item | Effort |
|---|---|---|
| 6.1 | Write a one-page "what is this skill, who is it for, what makes it different" doc — possibly `MANIFESTO.md` or expand README's intro | 60 min |
| 6.2 | Decide and document the long-term roadmap — what's in scope, what's not, what's 0.2.0 vs. 1.0.0 | 30 min — discuss with albertojb first |
| 6.3 | Decide and document the contribution policy (do you accept feature requests? bug reports? PRs?) | 15 min |

**Total Tier 6: ~2 hours, but blocked on §3 strategic input.**

---

## 5. Recommended sequencing

Highest-leverage 4–5 hour push to publishable-with-confidence:

```
Tier 1 (3 hrs)     →  Engine fixes (1.1, 1.2, 1.3, 1.6) + investigate 1.5
                       → bump version to 0.1.1, push
Tier 3 partial    →  Screenshots + architecture diagram + CONTRIBUTING/SECURITY
(1.5 hrs)              → push
Tier 4 partial    →  GitHub Actions CI + ruff config
(45 min)               → push
```

Anything beyond that is iterative: pick the next-most-painful gap, fix it, push, repeat.

### What to skip outright

- Per-layout rendered-screenshot previews (tier 3.11) — diminishing returns
- Type hints across 67 methods (tier 4.6) — separate project
- MkDocs (tier 3.10) — GitHub renders markdown well enough; defer until docs grow

---

## 6. Versioning notes

Current state: `v0.1.0` tag pushed to GitHub at commit `98ccffb` (initial commit). The packaging commit `dc9312d` is post-tag — already pushed but not labeled.

**Next version bump should be 0.1.1**, not 0.1.0 movement (since 0.1.0 is already public). Apply the tag after Tier 1 fixes:

```bash
git tag -a v0.1.1 -m "Engine correctness fixes (1.1–1.8 from BACKLOG.md)"
git push origin v0.1.1
```

Major-version semantics for this project (proposed; confirm with albertojb):
- `0.x.y` — pre-release, breaking changes allowed without notice
- `1.0.0` — first stable release; engine API frozen, gate behavior frozen
- Patch (`0.1.x`): bug fixes, documentation, internal changes
- Minor (`0.x.0`): new layouts, new gate checks, new examples
- Major (`x.0.0`): breaking changes to engine signatures, gate JSON schema, or routing structure

---

## 7. Things to NEVER undo

If a fresh chat is tempted to "improve" any of these, push back — they were deliberate:

- **Apache 2.0 attribution to Kaku Li in every `mck_ppt/*.py` file header.** Required by the license and ethically right. Don't strip it.
- **The `mck_ppt/` module name** (vs. renaming to `mbb_ppt`). Keeping the original name preserves Apache 2.0 lineage and is documented as an "implementation detail" in SKILL.md.
- **`MckEngine` class name.** Same reason. Documented under the `ExecEngine` alias.
- **`experiences/` is append-only.** Mark superseded entries with `Superseded by NNN`; never delete.
- **Five retired layouts** (Venn, Cycle, Funnel, Pie, Gauge). Methods still exist for backward compat; not promoted in new decks. Do not delete the methods.
- **Both gate scripts use English error messages.** Don't accept "minor" Chinese reintroductions.
- **The English-only positioning.** If a future contributor wants Chinese support, that's a fork or a separate `mbb-ppt-generator-zh` project, not a re-introduction here.
- **`gate_render.json` `passed` is a Python boolean derived from `len(user_code_errors) == 0`.** Never let it become an AI verbal claim or a fuzzy threshold.
- **`ENGINE_BUG_WHITELIST` is a hardcoded enum in code.** Verbal exemptions are forbidden by design. New whitelist entries require a PR with textual evidence in the comment.

---

## 8. Useful commands cheat-sheet

```bash
# Run all tests (once pytest installed)
pytest

# Or manually without pytest:
python3 -c "
import sys, tempfile, inspect
from pathlib import Path
sys.path.insert(0, '.')
def _t(): d=Path(tempfile.mkdtemp(prefix='mbb_')); p=d/'p'; p.mkdir(); return p
PR=Path('.').resolve()
from tests import test_smoke, test_layouts, test_gates
n=p=0
for mod in [test_smoke, test_layouts, test_gates]:
    for name in dir(mod):
        if not name.startswith('test_'): continue
        n+=1
        try:
            args=[(_t() if x=='tmp_project_dir' else PR) for x in inspect.signature(getattr(mod,name)).parameters]
            getattr(mod,name)(*args); p+=1
        except Exception as e: print(f'FAIL {name}: {e}')
print(f'{p}/{n} tests passed')
"

# Run examples
python3 examples/minimal_example.py
python3 examples/board_qbr_example.py

# Build the storyline
python3 -c "
from mck_ppt.deck_builder import DeckBuilder
from mck_ppt.storylines import ai_enterprise
DeckBuilder.build(ai_enterprise.STORYLINE, 'storyline.pptx')
"

# Run gates manually
python3 references/scripts/gate_check_content.py <content.json> <project_dir>
python3 references/scripts/gate_check_render.py <pptx> <project_dir>

# Audit residual CJK in tracked files
git ls-files '*.py' '*.md' '*.yaml' | xargs grep -lP '[\x{4E00}-\x{9FFF}]' 2>/dev/null

# Verify CJK hasn't crept back into the engine
grep -cP '[\x{4E00}-\x{9FFF}]' mck_ppt/*.py mck_ppt/storylines/*.py
# Expected: review.py: 14 (intentional regex no-ops); everything else: 0

# Engine smoke test from clean slate
python3 -c "
import sys; sys.path.insert(0,'.')
from mck_ppt import MckEngine
eng = MckEngine(total_slides=2)
eng.cover(title='Smoke test')
eng.closing(title='Done')
eng.save('/tmp/smoke.pptx')
print('OK')
"
```

---

## 9. How to start a fresh chat productively

When opening a new chat, give it:

```
We're continuing work on MBB PPT Generator at /home/ajb/Projects/MBB-PPT-2/
(also on GitHub at https://github.com/albertojb/mbb-ppt-generator).

Read BACKLOG.md first, then run the "first 5 minutes" verification.

Today I have NN minutes. Let's do [pick from § 4 tiers].
```

That gives the new chat enough context to produce useful work in the first turn without re-deriving everything.

---

*BACKLOG.md last updated 2026-05-07 immediately after pushing v0.1.0 to GitHub.*
