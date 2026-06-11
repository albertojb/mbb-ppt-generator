# Layouts — Special

> **Loaded on demand at S4 (Render).** Open this file when rendering `icon_grid`, `checklist`, `harvey_ball_table`, `meet_the_team`, `case_study`, or `metric_comparison`. These are layouts that don't fit the structure / data / chart / framework / comparison / process / image families.
>
> Capacity in [`../api-schemas.yaml`](../api-schemas.yaml).

---

## `icon_grid`

3-column (or `cols`-column) grid of icon-prefixed cards. Each card has a colored circle with the first letter of the title, a colored top accent strip, and a description. Use for capability grids, feature lists, or "five things to know" slides.

### Signature

```python
eng.icon_grid(title, items, cols=3, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `items` | list of **3-tuples** `(item_title, description, accent_color)` | yes | item_title ≤ 25, desc ≤ 50 | Up to 9 items in a 3×3 grid (default), or 8 in a 4×2 grid (`cols=4`). The icon "letter" is auto-derived from `item_title[0]`. |
| `cols` | int | no | — | Column count: 3 (default) or 4. With 4 cols, each card is narrower. |
| `source` | str | data → yes | — | — |

### Wireframe (3 cols × 2 rows)

```
┌──────────────────────────────────────────────────────────────┐
│ Six capabilities anchor the operating model                   │
│ ─────────────────────────────────────────────────             │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐                  │
│ │■━━━━━━━━━━━│ │■━━━━━━━━━━━│ │■━━━━━━━━━━━│                  │
│ │ ⓒ Clarity  │ │ ⓒ Cadence  │ │ ⓒ Capability│                  │
│ │ Roles and  │ │ Regular    │ │ Skills     │                  │
│ │ decision   │ │ review     │ │ match the  │                  │
│ │ rights ... │ │ meetings ..│ │ role ...   │                  │
│ └────────────┘ └────────────┘ └────────────┘                  │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐                  │
│ │■━━━━━━━━━━━│ │■━━━━━━━━━━━│ │■━━━━━━━━━━━│                  │
│ │ ⓒ Culture  │ │ ⓒ Coverage │ │ ⓒ Cycle    │                  │
│ │ Values     │ │ Geographic │ │ Quarterly  │                  │
│ │ reinforce  │ │ reach with │ │ cadence    │                  │
│ │ behavior...│ │ local ...  │ │ for ...    │                  │
│ └────────────┘ └────────────┘ └────────────┘                  │
│                                                               │
│ Source: operating-model framework                        7/N  │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
from mbb_ppt.constants import ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED, NAVY, MED_GRAY

eng.icon_grid(
    title='Six capabilities anchor the operating model',
    items=[
        ('Clarity',    'Roles and decision rights are explicit',    ACCENT_BLUE),
        ('Cadence',    'Regular review meetings with KPI focus',    ACCENT_GREEN),
        ('Capability', 'Skills match the role expectations',        ACCENT_ORANGE),
        ('Culture',    'Values reinforce desired behaviors',        ACCENT_RED),
        ('Coverage',   'Geographic reach with local presence',      NAVY),
        ('Cycle',      'Quarterly cadence for course-correction',   MED_GRAY),
    ],
    cols=3,
    source='Source: operating-model framework',
)
```

### Pitfalls

- **Item titles starting with the same letter.** The icon shows `title[0]` — six items starting with 'C' all show the same letter. Either pick titles with distinct first letters or accept the visual repetition (sometimes intentional for memorable mnemonics).
- **More than 9 items.** Doesn't fit cleanly. Cap at 9 (3×3) or 8 (4×2).
- **Description longer than 50 chars.** Wraps and crowds the small card. Keep terse.

---

## `checklist`

Status-table layout with rows representing tasks / items, a status-key column at the right, and alternating-color row backgrounds. Use for project trackers, audit checklists, readiness reviews.

### Signature

```python
eng.checklist(title, columns, col_widths, rows, status_map=None,
              source='', bottom_bar=None)
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `columns` | list[str] | yes | each ≤ 20 | Column header labels. The last column is the status indicator. |
| `col_widths` | list[Inches] | yes | — | One width per column. Last column is the status badge width — typically `Inches(1.4)`. |
| `rows` | list of variable-length tuples | yes | cell ≤ 30 | `(*data_vals, status_key)`. `data_vals` matches `len(columns) - 1`; `status_key` is one of the status_map keys. **Up to 7 rows.** |
| `status_map` | dict or `None` | no | — | Maps `status_key` → `(label, color, bg_color)`. **Default map (English):** `'active'`, `'risk'`, `'pending'`, `'done'`. |
| `source` | str | data → yes | — | — |
| `bottom_bar` | tuple or `None` | no | — | Optional gray summary bar. |

The default status map (used when you pass `status_map=None`):

| Key | Label | Color | Background |
|---|---|---|---|
| `'active'` | `'→ Active'` | `ACCENT_GREEN` | `LIGHT_GREEN` |
| `'risk'` | `'△ At risk'` | `ACCENT_ORANGE` | `LIGHT_ORANGE` |
| `'pending'` | `'○ Pending'` | `MED_GRAY` | `BG_GRAY` |
| `'done'` | `'✓ Done'` | `ACCENT_BLUE` | `LIGHT_BLUE` |

### Example

```python
from pptx.util import Inches

eng.checklist(
    title='FY26 launch readiness — 4 of 7 tracks active',
    columns=['Workstream', 'Owner', 'ETA', 'Notes', 'Status'],
    col_widths=[Inches(3.0), Inches(2.0), Inches(1.5), Inches(3.7), Inches(1.4)],
    rows=[
        ('Pricing test',          'Sales VP',   'Q2-mid',  'Cohort selected',     'active'),
        ('EMEA distributor sign', 'Reg. dir',   'Q2-end',  '2 of 3 closed',       'active'),
        ('Service hiring',        'Service dir','Q3-mid',  'Pipeline in 4 cities','active'),
        ('Cost simplification',   'Ops VP',     'Q4',      'Plan in draft',       'pending'),
        ('Brand refresh',         'CMO',        'Q3',      'Agency RFP open',     'risk'),
        ('Talent bench plan',     'CHRO',       'Done',    'Approved Q4',         'done'),
        ('API ecosystem',         'CTO',        'FY27',    'Concept stage',       'pending'),
    ],
    bottom_bar=('Risk',
                'Brand refresh slip would push positioning launch to Q4.'),
    source='Source: PMO weekly review',
)
```

### Pitfalls

- **Row arity mismatch.** Each row must have `len(columns) - 1` data values plus the trailing `status_key`. Validate.
- **Custom `status_map` missing keys.** If you override `status_map` and a row references a key not in the map, it falls back to `('?', MED_GRAY, BG_GRAY)`. Validate that every row's key exists in your map.
- **More than 7 rows.** Engine adapts row height down but the status column compresses. Cap at 7.

---

## `harvey_ball_table`

Multi-criteria evaluation matrix using Harvey Ball indicators (empty / quarter / half / three-quarter / full circles). Use for option scoring across multiple dimensions where qualitative differences matter more than precise numbers.

### Signature

```python
eng.harvey_ball_table(title, criteria, options, scores,
                      legend_text=None, summary=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `criteria` | list[str] | yes | each ≤ 35 | Row labels — the dimensions being scored. Up to 6 criteria. |
| `options` | list[str] | yes | each ≤ 14 | Column headers — the options being scored. Up to 4 options. |
| `scores` | list[list[int]] | yes | 0–4 | `scores[criterion_idx][option_idx]`. Values: 0 (empty circle), 1 (quarter), 2 (half), 3 (three-quarter), 4 (full). |
| `legend_text` | list[str] or `None` | no | each ≤ 25 | Legend strings explaining the score levels (e.g. `['● Strong fit', '◑ Partial fit', '○ Weak fit']`). |
| `summary` | str | no | ≤ 80 | Bottom gray summary bar. |
| `source` | str | data → yes | — | — |

The first column header is fixed to `'Dimension'`.

### Example

```python
eng.harvey_ball_table(
    title='Three options scored across five strategic criteria',
    criteria=[
        'Revenue impact',
        'Margin expansion',
        'Capability fit',
        'Time to value',
        'Risk profile',
    ],
    options=['Premium push', 'Channel growth', 'Cost simp.'],
    scores=[
        [4, 3, 2],   # revenue impact
        [4, 2, 4],   # margin expansion
        [3, 4, 4],   # capability fit
        [2, 3, 4],   # time to value
        [2, 3, 4],   # risk profile (low risk = full ball)
    ],
    legend_text=['● Strong', '◑ Partial', '○ Weak'],
    summary='Cost simplification scores most consistently across criteria.',
    source='Source: option evaluation workshop',
)
```

### Pitfalls

- **Score out of range.** Values must be 0–4. The `draw_harvey_ball()` helper clamps with `max(0, min(4, round(score)))`, so 5+ becomes 4 and -1 becomes 0 — but use the proper range explicitly.
- **`scores` shape mismatch.** `len(scores)` must equal `len(criteria)`, and each inner list length must equal `len(options)`. Mismatched shape causes silent visual errors.
- **Too many criteria or options.** > 6 criteria → rows compress; > 4 options → columns narrow. Cap at the matrix limits.

---

## `meet_the_team`

Profile cards in a row, each with a circle badge (first letter of name), name, role, and bio bullets. Use sparingly — typically once per deck, near the start (introductions) or near the end (acknowledgments).

### Signature

```python
eng.meet_the_team(title, members, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | no for action title — but the title bar still renders | ≤ 120 | — |
| `members` | list of **3-tuples** `(name, role, bio)` | yes | name ≤ 20, role ≤ 25, bio ≤ 100 chars or list[str] | Up to **4 members**. `bio` accepts a single string (split on `\n`) or a list of strings. |
| `source` | str | data → yes | — | — |

### Example

```python
eng.meet_the_team(
    title='Meet the strategy team',
    members=[
        ('Alex Park', 'Strategy lead',
         ['10 years at top-tier firms', 'Led 3 prior reorgs', 'Wharton MBA']),
        ('Maya Chen', 'Operating partner',
         ['Former CFO at Acme', 'Operations background', 'Stanford GSB']),
        ('Sam Diaz',  'Senior associate',
         ['Top-tier strategy alum', 'Consumer goods focus', 'INSEAD']),
        ('Jin Park',  'Analyst',
         ['Former bulge-bracket banker', 'Modeling specialist', 'Wharton UG']),
    ],
    source='Source: organizational chart',
)
```

### Pitfalls

- **More than 4 members.** Card width compresses; bios become unreadable. Cap at 4. For larger teams, use multiple slides or summarize ("Plus 12 senior analysts and 8 partners").
- **Photos vs. letter circles.** The current engine renders a letter circle (first letter of name). Real photos are not embedded; if you want photos, replace the circles in PowerPoint after generation.
- **Imbalanced bio lengths.** A member with a 100-char bio next to one with a 30-char bio looks lopsided. Aim for parallel structure and length.

---

## `case_study`

Situation / Action / Result narrative — three (or N) horizontal sections with letter badges and a final navy-fill section signaling the result. The conventional pattern is `'S'` / `'A'` / `'R'` letters, but any sequence works.

### Signature

```python
eng.case_study(title, sections, result_box=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `sections` | list of **3-tuples** `(letter, section_title, description)` | yes | section_title ≤ 20, desc ≤ 120 | 3 sections is the canonical S/A/R pattern. Up to 4. **The last section gets navy fill** (signaling the result / outcome); earlier sections get gray. |
| `result_box` | tuple `(label, text)` or `None` | no | text ≤ 200 | Optional bottom gray panel summarizing the case-study finding. |
| `source` | str | data → yes | — | — |

### Example

```python
eng.case_study(
    title='Case study — Acme reduced churn 40% in 18 months',
    sections=[
        ('S', 'Situation', 'Churn at 24% annually; service NPS 6.2/10; competitors gaining'),
        ('A', 'Action',    'Service redesign + 30 senior hires + retention bonuses'),
        ('R', 'Result',    'Churn 14%; NPS 8.4/10; net retention 110%; share +3pp'),
    ],
    result_box=('Implication',
                'Service investment is reproducible across our portfolio; '
                'the playbook applies to BetaCo and Gamma in the next 12 months.'),
    source='Source: Acme case file, FY25',
)
```

### Pitfalls

- **More than 4 sections.** Section width compresses below readable; the navy "result" emphasis is diluted.
- **Result section that doesn't conclude.** The last section should state the outcome / finding, not continue the action narrative. If your "result" is a list of more actions, the case study isn't done yet — defer the slide.

---

## `metric_comparison`

Before / after / change — three columns showing paired metrics with a delta badge. The delta badge auto-colors green for `+` deltas and red for `-` deltas.

### Signature

```python
eng.metric_comparison(title, metrics, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `metrics` | list of **4-tuples** `(label, before_val, after_val, delta_str)` | yes | label ≤ 25, vals ≤ 8, delta ≤ 8 | 3–5 rows recommended. **`delta_str` must start with `+` or `-`** for the auto-color to work; positive deltas get `ACCENT_GREEN`, negative get `ACCENT_RED`. |
| `source` | str | data → yes | — | — |

The column headers are fixed: `'Before'`, `'After'`, `'Change'`.

### Example

```python
eng.metric_comparison(
    title='Three KPIs improved meaningfully after the operating-model rollout',
    metrics=[
        ('Revenue',          '$1.0B',  '$1.24B', '+24%'),
        ('Margin',           '24%',    '31%',    '+7pp'),
        ('NPS',              '6.2',    '8.4',    '+2.2'),
        ('Time to resolve',  '4.2 d',  '1.8 d',  '-57%'),
    ],
    source='Source: post-implementation review, FY25',
)
```

### Pitfalls

- **Delta string without `+`/`-` prefix.** A delta like `'24%'` (no sign) defaults to red because `startswith('+')` is false. Always include the sign explicitly.
- **Mixed units across rows.** All four columns are visually parallel; mixing absolute, percentage, and time units in the same column reads as inconsistent. Either standardize or label each row's units inside the value (`'4.2 d'`).
- **Confusing with `before_after`.** `metric_comparison` is purely numeric; `before_after` carries narrative bullets. If the comparison is about *what changed* (state shift), use `before_after`. If it's about *how much changed* (numeric delta), use `metric_comparison`.

---

## Cross-references

- **Method index:** [`../framework/engine-api.md`](../framework/engine-api.md).
- **Capacity matrix:** [`../api-schemas.yaml`](../api-schemas.yaml).
- **`draw_harvey_ball()` implementation:** `mbb_ppt/core.py`.
- **Past defects in these layouts:** [`../../experiences/`](../../experiences/).
