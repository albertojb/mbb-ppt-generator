# Layouts — Data & Statistics

> **Loaded on demand at S4 (Render).** Open this file when rendering `big_number`, `two_stat`, `three_stat`, `data_table`, `metric_cards`, or `table_insight`. These are the heaviest-used data layouts — `table_insight` in particular is the editorial workhorse for opening slides.
>
> Capacity numbers are authoritative in [`../layout-matrix.yaml`](../layout-matrix.yaml). This file's matrix references are summaries.

---

## `big_number`

A single dominant statistic with context. Use when one figure carries the whole slide's argument.

### Signature

```python
eng.big_number(title, number, unit='', description='',
               detail_items=None, source='', bottom_bar=None)
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 (Rule 14); aim for ≤ 80 | Conclusion-led action title. |
| `number` | str/int | yes | ≤ 10 chars | Rendered at 44pt navy bold in `HEADING_FONT`. Examples: `'+12%'`, `'$3.4B'`, `'70'`. |
| `unit` | str | no | short, e.g. `'%'`, `'million'` | Rendered small under the number. If omitted, the detail-area label becomes `'Solution'`; if present, it becomes `'Detail'`. |
| `description` | str or list[str] | no | ≤ 60 chars per line | Right-side context paragraph or bullet list. |
| `detail_items` | list[str] | no | — | Optional gray panel below with bullet-list detail. |
| `source` | str | data → yes | — | Required if the number comes from external data. |
| `bottom_bar` | tuple `(label, text)` | no | — | Optional gray bar at slide bottom. |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Margin pressure is concentrated in two product lines  ← title│
│ ─────────────────────────────────────────────────            │
│ ┌──────────┐                                                 │
│ │          │   Premium and standard SKUs together account    │
│ │   +12%   │   for 87% of the margin gap. Re-pricing the     │
│ │          │   premium tier alone closes ~7pp.               │
│ │  margin  │                                                 │
│ └──────────┘                                                 │
│                                                              │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Solution                                                 │ │
│ │   • Reprice premium SKUs Q2                              │ │
│ │   • Bundle standard SKUs into 3-tier offer Q3            │ │
│ │   • Track margin recovery via weekly cohort dashboard    │ │
│ └──────────────────────────────────────────────────────────┘ │
│ Source: finance team, Q1 close                          5/N  │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.big_number(
    title='Margin pressure is concentrated in two product lines',
    number='+12%',
    unit='margin',
    description='Premium and standard SKUs together account for 87% of '
                'the margin gap. Re-pricing the premium tier alone closes ~7pp.',
    detail_items=[
        '• Reprice premium SKUs Q2',
        '• Bundle standard SKUs into 3-tier offer Q3',
        '• Track margin recovery via weekly cohort dashboard',
    ],
    source='Source: finance team, Q1 close',
)
```

### Pitfalls

- **The number is too long.** Anything over ~10 chars wraps inside the navy box; the box is fixed at 3.5". Reformat: `'1,234,567'` → `'1.2M'`.
- **No description.** A `big_number` with just a title and a number reads as a slogan, not analysis. Always pair the number with at least one sentence of context, even if `description` is short.
- **Decoration-as-content.** Resist using `big_number` when the number is not actually the argument. If three numbers matter, use `three_stat`. If the argument is qualitative, use `key_takeaway`.

---

## `two_stat`

Two statistics presented side-by-side with optional detail body below. Use for comparisons (before/after, A/B, this-period/last-period) where two figures are the headline.

### Signature

```python
eng.two_stat(title, stats, detail_items=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | Conclusion-led. |
| `stats` | list of **3-tuples** `(number, label, is_navy:bool)` | yes | number ≤ 10, label ≤ 20 | Exactly 2. The third element controls the box fill: `True` = navy filled with white text, `False` = gray fill with navy number. |
| `detail_items` | list[str] | no | — | Optional bullet list in the lower 3.5" of the slide. |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Channel performance widened in Q1                     ← title│
│ ─────────────────────────────────────────────────            │
│ ┌────────────────────────┐  ┌────────────────────────┐       │
│ │                        │  │                        │       │
│ │        +18%            │  │        -7%             │       │
│ │     Partner channel    │  │      Direct channel    │       │
│ │                        │  │                        │       │
│ └────────────────────────┘  └────────────────────────┘       │
│         (navy filled)            (gray filled)               │
│                                                              │
│ • Partner growth driven by two new distributors in EMEA      │
│ • Direct decline concentrated in tier-3 enterprise accounts  │
│                                                              │
│ Source: finance team                                     5/N │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.two_stat(
    title='Channel performance widened in Q1',
    stats=[
        ('+18%', 'Partner channel', True),
        ('-7%',  'Direct channel', False),
    ],
    detail_items=[
        '• Partner growth driven by two new distributors in EMEA',
        '• Direct decline concentrated in tier-3 enterprise accounts',
    ],
    source='Source: finance team',
)
```

### Pitfalls

- **Wrong tuple arity.** Engine expects 3-tuples `(number, label, is_navy)`. Passing 2-tuples raises `ValueError`.
- **Both stats navy or both gray.** Defeats the visual differentiation. The convention is: navy for the focal / positive stat, gray for the comparison / context stat. Use one of each.
- **Stats that aren't comparable.** `('+18%', 'Partner growth')` and `('$1.2M', 'Q1 revenue')` are different units and confuse the audience. Both stats should answer the same question with the same unit.

---

## `three_stat`

Three statistics in a row. Use for KPI snapshots (e.g. revenue / margin / NPS) when all three figures matter equally.

### Signature

```python
eng.three_stat(title, stats, detail_items=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `stats` | list of **3 × 3-tuples** `(number, label, is_navy:bool)` | yes | number ≤ 10, label ≤ 20 | Exactly 3 stats. Same `is_navy` semantics as `two_stat`. |
| `detail_items` | list[str] | no | — | Optional bullet list below the stat row. |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Q1 dashboard: growth recovered, margin held, NPS rose ← title│
│ ─────────────────────────────────────────────────            │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐                     │
│ │  +12%    │  │  31%     │  │   +8     │                     │
│ │ Revenue  │  │  Margin  │  │   NPS    │                     │
│ │  growth  │  │   QoQ    │  │   pts    │                     │
│ └──────────┘  └──────────┘  └──────────┘                     │
│   navy           gray           navy                         │
│                                                              │
│ All three KPIs improved in Q1; margin held above plan       │
│ despite higher input costs.                                  │
│                                                              │
│ Source: company financials                              5/N  │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.three_stat(
    title='Q1 dashboard: growth recovered, margin held, NPS rose',
    stats=[
        ('+12%', 'Revenue growth', True),
        ('31%',  'Margin QoQ',     False),
        ('+8',   'NPS pts',        True),
    ],
    detail_items=[
        'All three KPIs improved in Q1; margin held above plan despite higher input costs.',
    ],
    source='Source: company financials',
)
```

### Pitfalls

- **Cherry-picked KPIs.** Three is small enough that the audience expects them to be the *most important* three. If you skip a metric that matters, the audience notices and asks. Pick the three the audience would pick.
- **Mixed alternation.** `(navy, gray, navy)` highlights the first and third; `(gray, navy, gray)` highlights the middle. Pick the pattern intentionally — it directs attention.
- **No detail_items.** Without context, three_stat reads like a placeholder dashboard. Add at least one synthesis sentence in `detail_items`.

---

## `data_table`

Header row + data rows with thin separators. Use when the analytical structure is genuinely tabular (many rows × few columns) and there is no insight panel needed.

### Signature

```python
eng.data_table(title, headers, rows, col_widths=None,
               source='', bottom_bar=None)
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `headers` | list[str] | yes | ≤ 15 chars per header | Rendered 14pt `MED_GRAY` bold. |
| `rows` | list[list[str]] | yes | ≤ 40 chars per cell | Each row's length must match `len(headers)`. Max **8 rows** ([`layout-matrix`](../layout-matrix.yaml)). |
| `col_widths` | list[Inches] or `None` | no | — | If `None`, columns split evenly. Pass explicit widths when one column is much wider (e.g. a description column). |
| `source` | str | data → yes | — | — |
| `bottom_bar` | tuple | no | — | Optional gray summary bar. |

The engine adapts row height: if the rows would overflow the content area, height shrinks and font auto-drops to 10pt. This is dynamic-sizing per Rule 8.

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Three actions improve growth while protecting margin  ← title│
│ ─────────────────────────────────────────────────            │
│  ACTION              MECHANISM                  IMPACT       │
│ ─────────────────────────────────────────────────────────    │
│  Premium bundles    Raise mix in high-value     Revenue +12% │
│ ─────────────────────────────────────────────────────────    │
│  Channel expansion  Add distributor reach       Revenue +8%  │
│ ─────────────────────────────────────────────────────────    │
│  Cost simplification Reduce duplication         Margin +3pp  │
│ ─────────────────────────────────────────────────────────    │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Implication   Three actions are complementary, not       │ │
│ │               sequential.                                │ │
│ └──────────────────────────────────────────────────────────┘ │
│ Source: strategy team                                    6/N │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.data_table(
    title='Three actions improve growth while protecting margin',
    headers=['Action', 'Mechanism', 'Impact'],
    rows=[
        ['Premium bundles',     'Raise mix in high-value segments', 'Revenue +12%'],
        ['Channel expansion',   'Add distributor reach',            'Revenue +8%'],
        ['Cost simplification', 'Reduce duplication',               'Margin +3pp'],
    ],
    bottom_bar=('Implication', 'Three actions are complementary, not sequential.'),
    source='Source: strategy team',
)
```

### Pitfalls

- **More than 8 rows.** Rows shrink to illegibility. If you have 9+ rows, split into two slides or use `data_table` only for the top-N.
- **Cell text > 40 chars.** Will wrap and crowd. Reformat as bullets in a single cell or restructure as `table_insight` with the long text in the right panel.
- **Too many columns.** 3–4 columns is comfortable; 5–6 forces narrow widths that wrap mid-word. Cap at 4 unless you've passed explicit `col_widths` that account for short cells.
- **Choosing `data_table` when you have an insight to add.** Use `table_insight` instead — same table on the left, plus a dedicated insight panel on the right. Strictly better for analysis slides.

---

## `metric_cards`

Three or four accent-colored metric cards in a row. Use for parallel KPIs / capabilities / pillars where each item has a number or short value plus a description.

### Signature

```python
eng.metric_cards(title, cards, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `cards` | list of 3-tuples or 5-tuples | yes | card_title ≤ 20, desc ≤ 80 | 3-tuple: `(letter, card_title, desc)` — auto-colors NAVY/BG_GRAY. 5-tuple: `(letter, card_title, desc, accent_color, light_bg)` for explicit colors. Max **4 cards**. |
| `source` | str | data → yes | — | — |

The first element (`letter`) is rendered in a numbered/lettered circle at the top of each card.

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Four pillars of the FY26 operating plan               ← title│
│ ─────────────────────────────────────────────────            │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│ │   1      │ │   2      │ │   3      │ │   4      │          │
│ │          │ │          │ │          │ │          │          │
│ │ Premium  │ │ Channel  │ │ Cost     │ │ Talent   │          │
│ │   mix    │ │ growth   │ │ disc.    │ │  bench   │          │
│ │ ───────  │ │ ───────  │ │ ───────  │ │ ───────  │          │
│ │ Reprice  │ │ Add 2    │ │ Reduce   │ │ Hire 12  │          │
│ │ premium  │ │ distrib. │ │ overlap  │ │ senior   │          │
│ │ Q2-Q3    │ │ EMEA Q2  │ │ in svc.  │ │ engineers│          │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
│  navy strip  navy strip   navy strip   navy strip            │
│                                                              │
│ Source: FY26 plan                                       4/N  │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.metric_cards(
    title='Four pillars of the FY26 operating plan',
    cards=[
        ('1', 'Premium mix',   'Reprice premium bundles in Q2–Q3'),
        ('2', 'Channel growth','Add two distributors in EMEA Q2'),
        ('3', 'Cost discipline','Reduce overlap in shared services'),
        ('4', 'Talent bench',  'Hire 12 senior engineers by Q4'),
    ],
    source='Source: FY26 plan',
)
```

### Pitfalls

- **More than 4 cards.** Card width drops below 2.7", text crowds. Hard cap at 4. If you have 5+ items, split slides or move to `four_column` (which has a different visual register) or `icon_grid`.
- **Different-length descriptions across cards.** Cards are visually parallel, so descriptions of dramatically different length read as imbalanced. Aim for descriptions within ±20% of each other in length.
- **Using ACCENT_PAIRS for the wrong number.** The auto-color path uses the deck's default (NAVY/BG_GRAY). Pass the 5-tuple form when you genuinely want each card a different accent — but only for ≥ 3 cards (Rule: accents only when ≥ 3 parallel items need differentiation).

---

## `table_insight` ★

**The editorial workhorse.** Left ~60% data table; middle double-chevron arrow; right ~32% gray insight panel with bulleted insights. The single highest-impact layout in the engine for opening / argument slides. Strongly preferred for slides 2–5 of any substantive deck.

### Signature

```python
eng.table_insight(title, headers, rows, insights,
                  col_widths=None, insight_title='Insight:',
                  source='', bottom_bar=None)
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `headers` | list[str] | yes | ≤ 15 chars each | Bold 14pt. |
| `rows` | list[list[str]] | yes | ≤ 40 chars per cell | Each row's length must equal `len(headers)`. Max **6 rows**. Cell text supports `**bold**` markup inline. |
| `insights` | list[str] | yes | ≤ 60 chars each | 2–4 bullet insights shown in the right panel. |
| `col_widths` | list[Inches] or `None` | no | — | Optional explicit column widths for the table. |
| `insight_title` | str | no | short, e.g. `'Insight:'`, `'Why:'`, `'So what:'` | Default `'Insight:'`. |
| `source` | str | data → yes | — | — |
| `bottom_bar` | tuple | no | — | Optional gray summary bar. |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Three actions improve growth while protecting margin  ← title│
│ ─────────────────────────────────────────────────            │
│ ┌────────────────────────────────────┐  ┌──────────────────┐ │
│ │ ACTION       MECHANISM     IMPACT  │  │ Insight:         │ │
│ │ ──────────────────────────────────  │ ▶│ ───────          │ │
│ │ Premium      Raise mix in   +12%   │  │                  │ │
│ │ bundles      premium                │  │ • Actions are    │ │
│ │ ──────────────────────────────────  │  │   complementary, │ │
│ │ Channel      Add EMEA       +8%    │  │   not sequential │ │
│ │ expansion    distributors           │  │                  │ │
│ │ ──────────────────────────────────  │  │ • First two      │ │
│ │ Cost simp.   Reduce         +3pp   │  │   accelerate     │ │
│ │              service overlap        │  │   growth         │ │
│ └────────────────────────────────────┘  │                  │ │
│                                         │ • The third      │ │
│                                         │   funds          │ │
│                                         │   execution      │ │
│                                         └──────────────────┘ │
│ Source: strategy team                                    3/N │
└──────────────────────────────────────────────────────────────┘
```

The double-chevron arrow ▶ in the middle visually bridges table → insight; the engine draws it natively.

### Example

```python
eng.table_insight(
    title='Three actions improve growth while protecting margin',
    headers=['Action', 'Mechanism', 'Impact'],
    rows=[
        ['Premium bundles',     'Raise mix in premium',           '+12%'],
        ['Channel expansion',   'Add EMEA distributors',          '+8%'],
        ['Cost simplification', 'Reduce service overlap',         '+3pp'],
    ],
    insights=[
        'Actions are complementary, not sequential.',
        'First two accelerate growth; the third funds execution.',
        'Each is feasible within one planning cycle.',
    ],
    source='Source: strategy team',
)
```

### Pitfalls

- **Too many rows.** 6 is the cap. Beyond that, the table compresses and the insight panel narrows. Split into multiple slides if the analysis is genuinely 7+ rows.
- **Insights as topic labels.** Insights must be findings, not topics. Bad: `'Implementation'`. Good: `'Each action is feasible within one planning cycle.'`.
- **Insight count outside 2–4.** One insight makes the panel feel padded with whitespace; 5+ insights crowd. The visual rhythm assumes 2–4.
- **Treating it as a placeholder.** `table_insight` is the layout to use for substantive analysis, not a fallback when you cannot decide. Use it because the *data + insight* split fits the argument, not because nothing else does.

### Cross-references

- **Why this layout matters in slides 2–5:** [`../framework/planning-guide.md`](../framework/planning-guide.md) § 4 (Opening slides).
- Capacity: `table_insight` row in [`../layout-matrix.yaml`](../layout-matrix.yaml).

---

## Cross-references

- **Method index:** [`../framework/engine-api.md`](../framework/engine-api.md).
- **Capacity matrix:** [`../layout-matrix.yaml`](../layout-matrix.yaml).
- **Production rules:** [`../framework/guard-rails.md`](../framework/guard-rails.md).
- **Past defects in these layouts:** [`../../experiences/overflow.md`](../../experiences/overflow.md), [`../../experiences/layout-pitfalls.md`](../../experiences/layout-pitfalls.md).
