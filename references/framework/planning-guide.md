# Planning Guide

> **Loaded optionally at S3 (Content)** when the structure is non-obvious. If you can sequence the deck and pick layouts confidently from the engine API alone, you do not need this file. Reach for it when the brief is ambiguous, when the topic is unfamiliar, or when slide diversity is sliding into monotony.
>
> This is a planning toolkit, not a reference manual. Decision tools are in section 2 (storyboard test) and section 4 (layout selection by task). Section 3 has narrative templates you can clone.

---

## 1. Pre-flight — the storyboard

Before any slide is generated, produce a numbered list where **each line is one slide's action title stated as a conclusion.** Then read the list aloud.

> If the action titles in order do not function as a 90-second spoken briefing, the storyboard is not done.

This is the single most-skipped step and the single most common cause of decks that look polished but fail to persuade. The storyboard is the deck's spine. If the spine is weak, no amount of design polish recovers it.

### Storyboard test — three checks

1. **Stand-alone test.** Each title must be readable without seeing the slide. "Margin pressure is concentrated in two product lines" passes. "Margin analysis" fails.
2. **Continuity test.** Reading title N after title N-1 should feel like a sentence continuation, not a topic switch. If you find yourself saying "and now …" between every title, the order is wrong.
3. **Conclusion-led test.** Every title states a finding (verb-bearing clause), not a topic (noun phrase). If a title is a label, rewrite it.

### Storyboard format

```
1. (cover)
2. Three actions return revenue to double-digit growth                    [executive_summary]
3. Premium mix shift drives margin without adding cost-to-serve           [grouped_bar]
4. Two distributor channels remain underdeveloped relative to peers       [horizontal_bar]
5. Operating simplification can fund execution without harming service    [waterfall]
6. The three actions are complementary, not sequential                    [table_insight]
7. A phased rollout reduces execution risk and accelerates learning       [timeline]
8. (closing)
```

The right column is the layout you intend to use. It can change after the storyboard, but committing to a layout per slide forces you to think about *how* you will say each thing, not just *what*.

---

## 2. Narrative templates

Two templates cover most decks. Clone the closer one and adjust.

### Standard deck — 10–12 slides (60–90 minute audience)

```
1.  Cover                                                        [cover]
2.  Table of contents                                            [toc]
3.  Executive summary — the recommendation, lead with answer     [executive_summary]   ★
4.  Why this conclusion is correct (governing argument 1)        [table_insight]       ★
5.  Why this conclusion is correct (governing argument 2)        [grouped_bar | big_number]
6.  Why this conclusion is correct (governing argument 3)        [side_by_side | metric_cards]
7.  Evidence / case study                                        [case_study | data_table]
8.  Risk and trade-offs                                          [matrix_2x2 | pros_cons]
9.  Implementation path                                          [timeline | process_chevron]
10. Synthesis — restate the recommendation in light of evidence  [key_takeaway | executive_summary]
11. (optional) Roadmap or next-step decisions                    [action_items]
12. Closing                                                      [closing]
```

★ = high-impact opening layouts. Slides 3–5 set the deck's tone; lean into `executive_summary` / `table_insight` / `big_number` / `key_takeaway` here, not bullet text.

### Short deck — 6–8 slides (15–30 minute audience)

```
1. Cover                                                         [cover]
2. Executive summary — the recommendation                        [executive_summary]   ★
3. Argument 1 with supporting data                               [table_insight | grouped_bar]
4. Argument 2 with supporting data                               [side_by_side | big_number]
5. Evidence / one strong case                                    [case_study]
6. Synthesis and recommendation                                  [key_takeaway]
7. Next steps                                                    [action_items]
8. Closing                                                       [closing]
```

When the audience is senior and time is short, **drop the TOC.** A senior audience does not need a contents page; they need the answer faster.

### Decision-meeting deck — 4–6 slides

```
1. Cover                                                         [cover]
2. The decision being asked + recommendation                     [executive_summary | big_number]
3. Three reasons the recommendation holds                        [table_insight | four_column]
4. The single biggest risk, addressed                            [matrix_2x2 | side_by_side]
5. Decision request and timeline                                 [action_items]
6. Closing                                                       [closing]
```

---

## 3. Layout selection by task

When the storyboard has the message but the layout is unclear, pick from this matrix. The right column shows what NOT to use even though it might seem to fit.

| Communication task | Preferred layouts | Avoid |
|---|---|---|
| **State the recommendation** | `executive_summary`, `key_takeaway`, `big_number` | bullets, plain text |
| **One critical statistic** | `big_number`, `metric_cards` (one card) | paragraph |
| **Two options to compare** | `side_by_side`, `before_after`, `metric_comparison` | generic two-column text |
| **Three or four parallel ideas** | `table_insight`, `four_column`, `metric_cards`, `icon_grid` | bullet list |
| **Causal chain or process** | `process_chevron` (≤ 5 steps), `vertical_steps`, `value_chain`, `timeline` | numbered text |
| **Time-series trend** | `grouped_bar`, `line_chart`, `stacked_area`, `multi_bar_panel` | table only |
| **Composition / share of total** | `donut`, `stacked_bar`, `horizontal_bar` | bullet list |
| **Ranking / outlier** | `horizontal_bar`, `pareto`, `bubble` | unordered table |
| **Risk or prioritization** | `matrix_2x2`, `risk_matrix`, `swot`, `harvey_ball_table` | plain text |
| **Quote or framing claim** | `quote`, `quote_bg_image` | textbox in a slide title |
| **Case study** | `case_study`, `case_study_image`, `content_right_image` | dense paragraph |
| **Roadmap / phased plan** | `timeline`, `process_chevron`, `vertical_steps` | bulleted "next steps" |
| **Synthesis at end of section** | `key_takeaway`, `table_insight`, `executive_summary` | topic-only title + bullets |
| **Action / next steps** | `action_items`, `vertical_steps` | "discussion items" placeholder |
| **Team / people** | `meet_the_team` | photo grid without context |
| **Dashboard view** | `dashboard_kpi_chart`, `dashboard_table_chart` | three separate KPI slides |

### When two layouts both fit

Pick the **denser** one if you have the data to fill it. `table_insight` always beats `four_column` if you have rows of structured comparison data. `executive_summary` always beats `key_takeaway` for openers because it carries a numbered argument structure.

Pick the **simpler** one if you do not have the data. A bad `dashboard_kpi_chart` (sparse, fake numbers) is worse than a strong `big_number`.

---

## 4. Opening slides — slides 2-5

Slides 2–5 establish the deck's intellectual register. If the audience has decided by slide 5 that the deck is bullet-heavy and topic-led, no amount of effort on slides 6–12 recovers their attention.

**Strongly preferred for slides 3–5:**

- `executive_summary` (numbered governing thought + supports)
- `table_insight` (data + insight panel — the single highest-impact editorial layout in the engine)
- `big_number` (when one statistic dominates the argument)
- `key_takeaway` (left analysis + right gray panel)

**Acceptable but not exciting:** `metric_cards`, `four_column`, `side_by_side`.

**Avoid in slides 2–5:** `two_column_text`, `data_table` (without an insight panel), generic bullet layouts. These signal "the model gave up." Use them only when justified by the analysis structure, not by laziness.

---

## 5. Layout diversity

### Hard floor — visual density

The S3 content gate enforces this: **decks with ≥ 6 content slides (excluding cover/TOC/section_divider/closing) must include ≥ 2 chart, diagram, image, or process-flow layouts.** A deck of seven `executive_summary` / `four_column` / `side_by_side` slides will fail the gate, regardless of how well-written the text is.

This is the most common output failure of consulting-style skills: well-written text columns with no visual variety. The gate exists because the failure mode is predictable.

When the gate fires, the fix is in section 3 *Layout selection by task* — pick the layouts that match your data shape. If your deck is genuinely text-heavy (e.g. a legal brief in slide form), state that as a constraint in the brief and use the Fast Track exemption documented in `SKILL.md` § 5.

### Soft rule — adjacency

Two adjacent content slides should not use the same layout method **unless** the analytical structure genuinely demands repetition (e.g. three sequential `case_study` slides for three case studies in a portfolio).

**Diversity is not novelty for its own sake.** A 10-slide deck that uses 10 different layouts to show the same kind of content reads as showy and chaotic. The right rhythm is something like:

```
exec_summary  →  grouped_bar  →  table_insight  →  big_number  →
case_study    →  matrix_2x2   →  timeline       →  action_items
```

Mix of editorial layouts (`exec_summary`, `key_takeaway`, `table_insight`), data layouts (`grouped_bar`, `big_number`), framework layouts (`matrix_2x2`), and process layouts (`timeline`, `action_items`).

If you find yourself reaching for `bulletted_text` twice in three slides, that is a sign the storyboard has not yet committed to a real argument structure. Go back to step 1.

---

## 6. Content density rules

Every content slide must include:

- **A conclusion-led action title** (verb-bearing clause, ≤ 120 chars — Rule 14).
- **At least three meaningful zones** — typically the title bar, a body area, and an insight or summary bar. If the slide has only a title and a single bullet list, it is too sparse.
- **≥ 50 % of the practical content area filled.** Visible whitespace below the body suggests the slide is half-finished. Render gate flags > 55 % empty.
- **A source line** when external data appears. Format: `Source: <origin>, <date>`. Required by S3 gate.
- **A clear implication** — the reader should know, after reading the slide, what they are being asked to think or do.

Common density failures and fixes:

| Failure | Fix |
|---|---|
| Slide is 70 % whitespace below content | Add an insight bar (`bottom_bar=('Implication', '...')`) or split into two slides |
| Title is "Market trends" | Rewrite as a conclusion: "Market trends favor low-cost entrants over premium" |
| Three bullets, no data | Replace with `metric_cards` or `table_insight` if you have any numbers to attach |
| Action title is a question | Restate as the answer to the question; questions go in section dividers, not action titles |
| All bullets, no chart, on a data-rich topic | Convert to `grouped_bar` / `donut` / `pareto` whichever fits the data shape |

---

## 7. Common structural anti-patterns

These show up repeatedly. Avoid by name.

- **The information dump.** A slide that shows everything you found on a topic, hoping the audience will pick what matters. Remove the things that do not support the slide's action title.
- **The bottom-bar afterthought.** Adding `bottom_bar=('Takeaway', '…')` to recover a slide whose body says nothing. The bottom bar restates the title; if the body does not earn it, the bottom bar will not save it.
- **The "exec summary" with no answer.** A slide titled "Executive summary" whose four items are themselves topics ("Market dynamics", "Competition", "Strategy", "Next steps"). Each item must be a finding, not a section name.
- **The placeholder TOC.** A TOC with descriptions like "Overview of the project" and "Background information." Descriptions must preview the conclusion of each section.
- **The chart with no message.** A bar chart whose action title is "Revenue by quarter." The action title must state what the chart proves: "Revenue growth accelerated in Q3 driven by partner channel."
- **The risk slide without a response.** `risk_matrix` or `pros_cons` that lists risks but does not pair each with a mitigation. Use the `notes=` parameter or follow with an `action_items` slide.
- **The roadmap with five sequential `process_chevron` slides.** One `timeline` collapses this into a single slide that the audience can absorb.

---

## 8. When to break the rules

This guide is opinionated. Defy it when:

- The audience has explicitly asked for a different format (e.g. legal needs a long-form brief, not a deck).
- The brief is a one-question decision and a 12-slide standard template is overkill — use the **decision-meeting deck** template instead.
- A specific layout maps so well to the analytical structure that diversity is artificial — three case studies legitimately deserve three `case_study` slides.

The principles that do **not** flex:

- Action titles state conclusions. (Always.)
- Pyramid-Principle answer-first ordering. (Always.)
- Source attribution on data slides. (Always.)
- Storyboard before slides. (Always.)
- Gates pass before delivery. (Always.)

Everything else is a strong default with documented exceptions.

---

## Cross-references

- **Method catalog and signatures:** [`engine-api.md`](engine-api.md).
- **Capacity limits per layout:** [`../layout-matrix.yaml`](../layout-matrix.yaml).
- **Production rules:** [`guard-rails.md`](guard-rails.md).
- **Past structural failures and fixes:** [`../../experiences/layout-pitfalls.md`](../../experiences/layout-pitfalls.md).
