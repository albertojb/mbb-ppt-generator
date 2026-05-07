# Layouts — Comparison and Evaluation

> **Loaded on demand at S4 (Render).** Open this file when rendering `side_by_side`, `before_after`, `pros_cons`, `rag_status`, or `scorecard`. These layouts each pair items for evaluation; pick by what kind of pairing your argument needs.
>
> Capacity in [`../layout-matrix.yaml`](../layout-matrix.yaml).

---

## `side_by_side`

Two columns with navy headers, gray bodies, bullet content. Use for option comparisons (Option A vs. Option B), market comparisons (segment X vs. segment Y), or any case where two distinct entities are weighed against each other.

### Signature

```python
eng.side_by_side(title, options, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | Conclusion-led — the title should usually preview the recommendation, not just name the comparison. |
| `options` | list of **2 × 2-tuples** `(option_title, points)` | yes | option_title ≤ 20, point ≤ 50 | Exactly 2 options. `points` is `list[str]` of bullets, ≤ 6 each. |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Option B (premium expansion) wins on margin and risk balance │
│ ─────────────────────────────────────────────────             │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━┓ ┏━━━━━━━━━━━━━━━━━━━━━━━━┓         │
│ ┃ Option A — Volume push  ┃ ┃ Option B — Premium      ┃         │
│ ┗━━━━━━━━━━━━━━━━━━━━━━━━┛ ┗━━━━━━━━━━━━━━━━━━━━━━━━┛         │
│ ┌─────────────────────────┐ ┌─────────────────────────┐       │
│ │                         │ │                         │       │
│ │ • +18% revenue growth   │ │ • +12% revenue growth   │       │
│ │ • -2pp margin pressure  │ │ • +3pp margin expansion │       │
│ │ • $25M capex            │ │ • $12M capex            │       │
│ │ • 9-month payback       │ │ • 14-month payback      │       │
│ │ • Service strain risk   │ │ • Brand uplift          │       │
│ │                         │ │ • Talent retention pos. │       │
│ └─────────────────────────┘ └─────────────────────────┘       │
│                                                               │
│ Source: option analysis                                  6/N  │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.side_by_side(
    title='Option B (premium expansion) wins on margin and risk balance',
    options=[
        ('Option A — Volume push', [
            '• +18% revenue growth',
            '• -2pp margin pressure',
            '• $25M capex',
            '• 9-month payback',
            '• Service strain risk',
        ]),
        ('Option B — Premium', [
            '• +12% revenue growth',
            '• +3pp margin expansion',
            '• $12M capex',
            '• 14-month payback',
            '• Brand uplift',
            '• Talent retention positive',
        ]),
    ],
    source='Source: option analysis',
)
```

### Pitfalls

- **Title that only names the comparison.** `'Option A vs. Option B'` is a weak title. The title must preview the answer: `'Option B wins on margin and risk balance.'`
- **Imbalanced bullet counts.** 2 bullets vs. 6 reads as imbalanced argument. Aim within ±1.
- **Bullet text > 50 chars.** Wraps tightly inside the column. Break long bullets into two short ones.
- **Different bullet structures across columns.** If left has metric-style bullets ("+18%, -2pp") and right has narrative bullets ("Strong growth, mild margin"), they're hard to compare. Use parallel structure.

---

## `before_after`

Vertical-divider editorial layout for transition / transformation narratives. The most flexible comparison layout in the engine — content can be simple bullets or richer dict structures with brand / value pairs and case studies.

### Signature

```python
eng.before_after(title, before_title, before_points,
                 after_title, after_points, source='',
                 corner_label='', bottom_bar=None,
                 left_summary='', right_summary='',
                 right_summary_color=None)
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `before_title` / `after_title` | str | yes | ≤ 30 each | Section subtitles for left and right halves. |
| `before_points` / `after_points` | list[dict] **or** list[str] | yes | — | If list[str]: simple bullets. If list[dict]: rich rows with `'label'`, `'brand1'`, `'val1'`, optional `'brand2'`, `'val2'`, `'extra'` for `before_points`; `'title'`, `'desc'`, optional `'cases'`: list of `(name, performance)` for `after_points`. See engine docstring for full schema. |
| `corner_label` | str | no | ≤ 25 | Optional dashed corner annotation (e.g. chapter callout). |
| `bottom_bar` | tuple `(label, text)` or `None` | no | — | Optional gray summary bar at slide bottom. |
| `left_summary` / `right_summary` | str | no | ≤ 80 | Optional one-line summary at the bottom of each half. |
| `right_summary_color` | RGBColor or `None` | no | — | Override summary color (default DARK_GRAY). Use a navy or accent color when the right summary is the punchline. |
| `source` | str | data → yes | — | — |

### Wireframe (simple bullet form)

```
┌──────────────────────────────────────────────────────────────┐
│ The category shifted from product-led to service-led         │
│ ─────────────────────────────────────────────────             │
│ Before                  ▎              After                  │
│ ─────────               ▎              ─────────              │
│                         ▎                                     │
│ • Hardware sales        ▎              • Subscription bundles │
│ • One-time license      ▎     ───▶     • Monthly service      │
│ • Channel partners      ▎              • Direct + partners    │
│ • SKU proliferation     ▎              • Outcome-based pricing│
│                         ▎                                     │
│                         ▎                                     │
│                                                               │
│ Source: industry analysis                                7/N  │
└───────────────────────────────────────────────────────────────┘
```

### Example (simple form)

```python
eng.before_after(
    title='The category shifted from product-led to service-led',
    before_title='Before',
    before_points=[
        '• Hardware sales',
        '• One-time license',
        '• Channel partners',
        '• SKU proliferation',
    ],
    after_title='After',
    after_points=[
        '• Subscription bundles',
        '• Monthly service',
        '• Direct + partners',
        '• Outcome-based pricing',
    ],
    bottom_bar=('Implication',
                'Strategy must shift from product roadmap to service portfolio.'),
    source='Source: industry analysis',
)
```

### Pitfalls

- **Mixing simple and rich forms across before / after.** If `before_points` is `list[str]` and `after_points` is `list[dict]`, the visual feels mismatched. Use the same form on both sides.
- **Forgetting the punchline.** `before_after` carries an implicit "and now what?" — the audience expects the slide to land somewhere. Pair with `bottom_bar` or `left_summary` / `right_summary` to make the implication explicit.
- **Confusing with `metric_comparison`.** `metric_comparison` is for paired numeric values (before $ / after $); `before_after` is for paired narratives. If the data is purely numeric per row, `metric_comparison` is cleaner.

---

## `pros_cons`

Two-column pros / cons layout with optional bottom conclusion. Pros header in navy, cons header in dark gray — visual signal alone tells the audience which side is which.

### Signature

```python
eng.pros_cons(title, pros_title, pros, cons_title, cons,
              conclusion=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `pros_title` | str | yes | ≤ 25 | Left header. Convention: `'Advantages'`, `'Pros'`, or a finding (`'Why this works'`). |
| `pros` | list[str] | yes | each ≤ 60 chars | 3–5 bullet items. Pre-formatted with `•` prefix recommended. |
| `cons_title` | str | yes | ≤ 25 | Right header. Convention: `'Risks'`, `'Cons'`, `'What could go wrong'`. |
| `cons` | list[str] | yes | each ≤ 60 chars | 3–5 bullet items. |
| `conclusion` | tuple `(label, text)` or `None` | no | text ≤ 120 | Optional gray bottom panel — the resolution of the pros / cons. |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Premium expansion — advantages outweigh risks if pricing  ← title
│ holds                                                         │
│ ─────────────────────────────────────────────────             │
│  Advantages                          Risks                    │
│  ──────────                          ─────                    │
│                                                               │
│  • +3pp margin                       • Dilution at low end    │
│  • Brand uplift                      • Service capacity needs │
│  • Higher LTV                        • 18-month payback       │
│  • Competitive moat                  • Channel pushback       │
│                                                               │
│ ┌──────────────────────────────────────────────────────────┐  │
│ │ Conclusion  Proceed if Q2 pricing test confirms +6%      │  │
│ │             premium-tier elasticity holds.               │  │
│ └──────────────────────────────────────────────────────────┘  │
│ Source: option analysis                                  7/N  │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.pros_cons(
    title='Premium expansion — advantages outweigh risks if pricing holds',
    pros_title='Advantages',
    pros=[
        '• +3pp margin',
        '• Brand uplift',
        '• Higher LTV',
        '• Competitive moat',
    ],
    cons_title='Risks',
    cons=[
        '• Dilution at low end',
        '• Service capacity needs',
        '• 18-month payback',
        '• Channel pushback',
    ],
    conclusion=('Conclusion',
                'Proceed if Q2 pricing test confirms +6% premium-tier elasticity holds.'),
    source='Source: option analysis',
)
```

### Pitfalls

- **No conclusion.** A pros / cons slide without a `conclusion` panel reads as indecisive. Always add the conclusion — even if it's "decision deferred pending X data."
- **Bullet count mismatch.** 5 pros and 2 cons signals advocacy, not analysis. Match counts (±1) unless the imbalance is the point.
- **Bullet text without `•` prefix.** Engine does not auto-prefix; pass the bullet character.
- **`pros_cons` when `before_after` would be clearer.** `pros_cons` is for evaluating one option's tradeoffs. If you're comparing two distinct things (option A vs. option B), use `side_by_side`.

---

## `rag_status`

Multi-project status table with red/amber/green status dots. Use for portfolio reviews where the audience needs to see which initiatives are healthy and which are not.

### Signature

```python
eng.rag_status(title, headers, rows, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `headers` | list[str] | yes | header ≤ 18 | Column headers. **First column is project name; second column is the RAG dot; remaining columns are values; last column is the note.** |
| `rows` | list of variable-length tuples `(name, status_color, *values, note)` | yes | name ≤ 24, value ≤ 18, note ≤ 50 | Each row's length depends on `len(headers)`: position 0 is name, position 1 is `status_color` (an `RGBColor` like `ACCENT_GREEN` / `ACCENT_ORANGE` / `ACCENT_RED`), the slice `[2:-1]` is values matching the middle headers, position -1 is the note text. Up to 8 rows. |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Portfolio status — 4 of 6 initiatives green                  │
│ ─────────────────────────────────────────────────             │
│  PROJECT          STATUS  OWNER     ETA       NOTE            │
│ ─────────────────────────────────────────────────             │
│  Premium relaunch   ●     Sales VP  Q2-end   On plan          │
│ ─────────────────────────────────────────────────             │
│  EMEA expansion     ●     Reg. dir  Q3-end   2 distrib closed │
│ ─────────────────────────────────────────────────             │
│  Cost simp.         ●     Ops VP    Q4-mid   Tracking +5%     │
│ ─────────────────────────────────────────────────             │
│  Service uplift     ●     Service   Q3-mid   Capacity gap     │
│ ─────────────────────────────────────────────────             │
│  New product launch ●     Eng VP    Slipped  Pushed to FY26   │
│ ─────────────────────────────────────────────────             │
│  API ecosystem      ●     CTO       FY26     Concept stage    │
│                                                               │
│ Source: PMO dashboard                                    8/N  │
└───────────────────────────────────────────────────────────────┘
```

(Dot colors: `ACCENT_GREEN` = on plan, `ACCENT_ORANGE` = at risk, `ACCENT_RED` = behind / slipped.)

### Example

```python
from mck_ppt.constants import ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED

eng.rag_status(
    title='Portfolio status — 4 of 6 initiatives green',
    headers=['Project', 'Status', 'Owner', 'ETA', 'Note'],
    rows=[
        ('Premium relaunch',  ACCENT_GREEN,  'Sales VP', 'Q2-end',  'On plan'),
        ('EMEA expansion',    ACCENT_GREEN,  'Reg. dir', 'Q3-end',  '2 distributors closed'),
        ('Cost simp.',        ACCENT_GREEN,  'Ops VP',   'Q4-mid',  'Tracking +5%'),
        ('Service uplift',    ACCENT_ORANGE, 'Service',  'Q3-mid',  'Capacity gap'),
        ('New product launch',ACCENT_RED,    'Eng VP',   'Slipped', 'Pushed to FY26'),
        ('API ecosystem',     ACCENT_GREEN,  'CTO',      'FY26',    'Concept stage'),
    ],
    source='Source: PMO dashboard',
)
```

### Pitfalls

- **Row length doesn't match headers.** The engine slices `[2:-1]` for middle values. If your row has fewer or more elements than `len(headers)`, columns mis-align silently. Validate before passing.
- **Status color not matching the visual convention.** Audience expects green = healthy, orange = at risk, red = behind. Using `ACCENT_BLUE` for "in progress" breaks that convention; pick one of the three RAG colors.
- **More than 8 rows.** Rows compress; the dot becomes hard to spot. Cap at 8; for longer portfolios, split by program / region into multiple slides.

---

## `scorecard`

Multi-dimension rating table with progress bars. Bar color auto-codes: NAVY at ≥ 70%, ACCENT_ORANGE at 50-69%, ACCENT_RED below 50%.

### Signature

```python
eng.scorecard(title, items, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `items` | list of **3-tuples** `(name, score:str, pct:float)` | yes | name ≤ 35, score ≤ 8 | `pct` is 0.0–1.0 controlling bar fill width AND bar color (auto). `score` is the textual score shown in navy bold (e.g. `'8.4/10'`, `'A-'`, `'72'`). 4–6 items recommended. |
| `source` | str | data → yes | — | — |

The auto-color thresholds: bar is `NAVY` for `pct ≥ 0.7`, `ACCENT_ORANGE` for `0.5 ≤ pct < 0.7`, `ACCENT_RED` for `pct < 0.5`.

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Capability scorecard — engineering and brand strong; service │
│ behind                                                        │
│ ─────────────────────────────────────────────────             │
│  DIMENSION              SCORE                                 │
│ ─────────────────────────────────────────────────             │
│  Engineering bench      8.4/10  ████████████████████░░░░       │ ← navy
│ ─────────────────────────────────────────────────             │
│  Brand recall           7.6/10  ███████████████████░░░░░       │ ← navy
│ ─────────────────────────────────────────────────             │
│  Channel reach          6.2/10  ███████████████░░░░░░░░░       │ ← orange
│ ─────────────────────────────────────────────────             │
│  Service capacity       4.8/10  ██████████░░░░░░░░░░░░░░       │ ← red
│ ─────────────────────────────────────────────────             │
│  Pricing discipline     7.1/10  ██████████████████░░░░░░       │ ← navy
│                                                               │
│ Source: capability assessment, Q1 2026                   8/N  │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.scorecard(
    title='Capability scorecard — engineering and brand strong; service behind',
    items=[
        ('Engineering bench', '8.4/10', 0.84),
        ('Brand recall',      '7.6/10', 0.76),
        ('Channel reach',     '6.2/10', 0.62),
        ('Service capacity',  '4.8/10', 0.48),
        ('Pricing discipline','7.1/10', 0.71),
    ],
    source='Source: capability assessment, Q1 2026',
)
```

### Pitfalls

- **Wrong tuple arity.** 3-tuples required. The textual `score` and the numeric `pct` carry different signals — the audience reads the score, the bar carries the visual weight. Both matter.
- **`score` text and `pct` value disagree.** If `score='8/10'` (= 0.8) but `pct=0.5`, the bar is half-full while the label says 80%. Validate that `pct` matches the score before passing.
- **More than 6 items.** Rows compress; the visual bar discrimination weakens. Cap at 6; for longer scorecards, group dimensions and create a separate slide per group.
- **Default header row "Domain / Score / Maturity".** When called without a custom header layout, the engine renders three column headers `['Domain', 'Score', 'Maturity']`. The `'Maturity'` column header sits above the progress bar — useful framing if your scorecard is about maturity, but odd if it's about something else. The header text is currently fixed in the engine; treat it as a generic frame.

---

## Cross-references

- **Method index:** [`../framework/engine-api.md`](../framework/engine-api.md).
- **Capacity matrix:** [`../layout-matrix.yaml`](../layout-matrix.yaml).
- **When to use comparison vs. matrix:** [`../framework/planning-guide.md`](../framework/planning-guide.md) § 3.
- **Past defects in these layouts:** [`../../experiences/`](../../experiences/).
