# MBB PPT Generator — Agent Instructions

> **For Claude Cowork and Claude Code users:** read `SKILL.md` instead — it has Claude-specific tooling, richer references, and layout guidance. This file is for agents running in other environments (any AI assistant, CLI tool, browser-based agent, etc.).

---

## What this skill does

Generates executive-grade PowerPoint decks (`.pptx`) using a five-stage workflow with two machine-readable quality gates. The output follows the McKinsey/Bain/BCG communication style: pyramid structure, conclusion-led headlines, visual variety, sober forest-green design.

## Install (one-time, requires Python 3.10+)

**Terminal (Mac / Linux):**
```bash
python3 -c "import urllib.request,subprocess,sys,tempfile,os; d=tempfile.mkdtemp(); p=os.path.join(d,'install.py'); urllib.request.urlretrieve('https://raw.githubusercontent.com/albertojb/mbb-ppt-generator/main/install.py', p); sys.exit(subprocess.call([sys.executable, p]))"
```

**Windows PowerShell:**
```powershell
python -c "import urllib.request,subprocess,sys,tempfile,os; d=tempfile.mkdtemp(); p=os.path.join(d,'install.py'); urllib.request.urlretrieve('https://raw.githubusercontent.com/albertojb/mbb-ppt-generator/main/install.py', p); sys.exit(subprocess.call([sys.executable, p]))"
```

After install, confirm it works: `python3 -m mbb_ppt version`

---

## Five-stage workflow

Every deck lives under a working directory `ppt-project-{slug}/`. Each stage produces one artifact. **Do not skip stages or advance past a failed gate.**

```
S1 Brief → S2 Outline [gate] → S3 Content [gate] → S4 Render [gate] → S5 Deliver
```

---

### S1 — Brief

Collect from the user (or infer from context):

| Field | What it means |
|---|---|
| `audience` | Who is in the room. Role and decision authority. |
| `goal` | Decide / persuade / inform. One sentence. |
| `duration_minutes` | Roughly 1 slide per minute. |
| `key_messages` | Up to 5 core points the audience must leave with. |

**Produce:** `ppt-project-{slug}/brief.md`

---

### S2 — Outline

Choose a layout for each slide. Match the layout to what the data looks like:

| Content shape | Layouts to consider |
|---|---|
| Trend / time series | `grouped_bar`, `line_chart`, `stacked_area` |
| Composition / share | `donut`, `stacked_bar`, `mekko`, `horizontal_bar` |
| Ranking / outliers | `horizontal_bar`, `pareto`, `ranked_table` |
| 2×2 framework | `matrix_2x2`, `swot`, `risk_matrix` |
| Process / phased plan | `process_chevron`, `timeline`, `value_chain`, `project_gantt` |
| Exhibit + so-what | `insight_rail` |
| Case proof | `case_study`, `case_study_image` |
| Text argument | `executive_summary`, `numbered_list_panel`, `four_column` |
| Big stat | `big_number`, `kpi_tracker` |

**Rules:**
- Lead with an `executive_summary` carrying the recommendation (not a cover slide).
- Do not add a cover or closing slide unless the user explicitly asks.
- For decks with ≥ 6 content slides, include at least 2 chart/diagram/image layouts — the gate enforces this.
- No single layout should exceed ~25% of content slides. `executive_summary` is capped at 15%.
- Action titles must be conclusion-led clauses (> 10 chars, contains a verb, ≤ 120 chars).

**Produce:** `ppt-project-{slug}/outline.json`

```json
{
  "brief": {"audience": "Board", "goal": "Strategy review", "duration_minutes": 15},
  "read_aloud_test": false,
  "slides": [
    {"idx": 1, "layout": "executive_summary",
     "title": "Three actions return revenue to growth",
     "key_point": "Premium mix, channel expansion, and cost simplification compose the recommendation."},
    {"idx": 2, "layout": "grouped_bar",
     "title": "Premium mix drives 60% of the margin recovery",
     "key_point": "Channel B shows the steepest improvement curve."}
  ]
}
```

**Gate S2 — storyboard (mandatory):**

Read all slide titles aloud in order. If the sequence does not work as a 90-second spoken briefing, revise before continuing. Then set `"read_aloud_test": true` in `outline.json` and run:

```bash
python3 -m mbb_ppt gate-storyboard ppt-project-{slug}/outline.json
```

Do not proceed to S3 until this exits 0.

---

### S3 — Content

Fill in every slide with concrete copy, numbers, and chart data. Add a `source` field to every non-structural slide.

**Content.json format** — each slide has `idx`, `layout`, `title`, `source`, and layout-specific fields. The full layout API is in `references/api-cheatsheet.md`. Example:

```json
{
  "slides": [
    {
      "idx": 1, "layout": "executive_summary",
      "title": "Three actions return revenue to growth",
      "items": [
        ["01", "Premium mix", "Shift 15pp of volume to high-margin SKUs by Q3."],
        ["02", "Channel expansion", "Open 3 tier-2 city distributor agreements by Q4."],
        ["03", "Cost simplification", "Remove 2 underperforming SKUs and consolidate packaging."]
      ],
      "source": "Internal P&L, 2026 Q1"
    },
    {
      "idx": 2, "layout": "grouped_bar",
      "title": "Premium mix drives 60% of the margin recovery",
      "series": [["Premium", 12, 18, 27], ["Standard", 40, 38, 35], ["Value", 48, 44, 38]],
      "categories": ["2024", "2025", "2026F"],
      "source": "Finance model v3, Jun 2026"
    }
  ]
}
```

**Gate S3 — content (mandatory):**

```bash
python3 -m mbb_ppt gate-content ppt-project-{slug}/content.json
```

This writes `ppt-project-{slug}/gate_content.json`. Advance only when `"passed": true`. If false, fix every item in `fail_items` and re-run.

---

### S4 — Render + QA

```bash
python3 -m mbb_ppt render ppt-project-{slug}/content.json \
    --out ppt-project-{slug}/deck.pptx
```

This runs the S3 gate, renders the deck, and runs the S4 QA gate in sequence. It exits non-zero if any gate fails.

**If the render gate fails:** fix the `user_code_errors` listed in `ppt-project-{slug}/gate_render.json` and re-run.

**Auto-fix for minor text overflow:**
```bash
python3 references/scripts/gate_check_render.py \
    ppt-project-{slug}/deck.pptx ppt-project-{slug}/ --auto-fix
```

---

### S5 — Deliver

The deck is at `ppt-project-{slug}/deck.pptx`. Confirm `gate_render.json` shows `"passed": true` before delivering.

---

## Core principles

**Answer first.** Lead with the recommendation. Background only when the audience cannot interpret it without context.

**One idea per slide.** Each slide has one governing thought in the title. Everything else supports it.

**Conclusion-led titles.** Titles are complete clauses with a verb and a conclusion — not labels.

| Weak | Strong |
|---|---|
| Margin analysis | Margin pressure is concentrated in two product lines |
| Expansion options | Spain is the best near-term expansion market |

**Visual variety.** A deck that is all text columns fails the S3 gate. Use charts, diagrams, and process flows to show, not just tell.

---

## Layout reference

Full API for every layout is in `references/api-cheatsheet.md`. Per-layout detail is in `references/layouts/`. The canonical schema (tuple arity, field names, character budgets) is in `references/api-schemas.yaml`.

---

## MCP integration (for MCP-capable agents)

If your agent supports MCP, the skill can be registered as a local MCP server — this lets your agent call the gates and renderer as functions rather than shell commands.

```bash
python3 -m mbb_ppt.surfaces.mcp_server --setup
```

This prints a config snippet you add to your agent's MCP settings. The server exposes four tools: `gate_storyboard`, `gate_content`, `gate_render`, `render`.
