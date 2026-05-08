# Layouts — Timeline and Process

> **Loaded on demand at S4 (Render).** Open this file when rendering `timeline`, `vertical_steps`, `process_chevron`, `value_chain`, `decision_tree`, `agenda`, or `action_items`. Despite the filename, this covers all sequence / dependency layouts.
>
> Capacity in [`../layout-matrix.yaml`](../layout-matrix.yaml).

---

## `timeline`

Horizontal milestone roadmap with numbered nodes. Use for time-phased rollouts (Q1 → Q2 → Q3 → Q4) where each milestone has a short label and a description.

### Signature

```python
eng.timeline(title, milestones, source='', bottom_bar=None)
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `milestones` | list of **2-tuples** `(label, description)` | yes | label ≤ 8 chars, **last milestone label ≤ 6 chars**; desc ≤ 40 | Up to **6 milestones**. The **last milestone gets a NAVY-filled circle**; all others get `ACCENT_BLUE`. The engine right-anchors the last label and the right anchor causes labels > 6 chars to overflow the canvas — see pitfalls. |
| `source` | str | data → yes | — | — |
| `bottom_bar` | tuple `(label, text)` or `None` | no | — | Optional gray summary bar. |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ A phased rollout reduces execution risk and accelerates      │
│ learning                                                      │
│ ─────────────────────────────────────────────────             │
│                                                               │
│   Design        Pilot        Scale       Measure              │
│                                                               │
│   ────────────────────────────────────────────                │
│      ①            ②            ③            ④                 │
│   blue          blue          blue          navy ← last       │
│                                                               │
│   Prioritize   Launch        Roll out      Refine             │
│   workstreams  in 2 markets  to all        based on           │
│                              regions       data               │
│                                                               │
│ Source: PMO                                              7/N  │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.timeline(
    title='A phased rollout reduces execution risk and accelerates learning',
    milestones=[
        ('Q1',  'Design and prioritization'),
        ('Q2',  'Pilot launch in 2 markets'),
        ('Q3',  'Scale-up to all regions'),
        ('Q4',  'Measure and refine'),
    ],
    source='Source: PMO',
)
```

### Pitfalls

- **Last milestone label > 6 chars.** The engine right-anchors the last milestone's label using a fixed offset, so a 7+ char label overflows the slide right edge by ~0.47". This is a documented engine bug, whitelisted in `gate_check_render.py` for `timeline` only. Workaround: keep the last label short (`'Q4'`, `'2026'`, `'End'`). ([`experiences/overflow.md` Experience 006](../../experiences/overflow.md), [`experiences/layout-pitfalls.md` Experience 005](../../experiences/layout-pitfalls.md).)
- **Too many milestones.** Above 6, label nodes crowd the timeline. Cap at 6.
- **Description > 40 chars.** Wraps to 3+ lines and crowds adjacent milestones. Keep descriptions short.

---

## `vertical_steps`

Top-down numbered step list with title and description per step. Use when sequence matters but horizontal width is constrained, or when each step has a paragraph of detail.

### Signature

```python
eng.vertical_steps(title, steps, source='', bottom_bar=None)
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `steps` | list of **3-tuples** `(num, step_title, description)` | yes | step_title ≤ 25, desc ≤ 80 | Up to **5 steps**. Engine adapts spacing based on count; with 5+ steps, font drops to small. |
| `source` | str | data → yes | — | — |
| `bottom_bar` | tuple or `None` | no | — | Optional gray summary bar. |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Five steps to recover margin in two quarters                  │
│ ─────────────────────────────────────────────────             │
│ ① Diagnose       Identify SKU-level margin contribution       │
│ ─────────────────────────────────────────────────             │
│ ② Cluster        Group SKUs into top, mid, tail by margin     │
│ ─────────────────────────────────────────────────             │
│ ③ Decide         Reprice top, bundle mid, sunset tail         │
│ ─────────────────────────────────────────────────             │
│ ④ Execute        Roll out reprice in Q2; bundles in Q3        │
│ ─────────────────────────────────────────────────             │
│ ⑤ Measure        Weekly margin tracker; cohort analysis       │
│                                                               │
│ Source: margin recovery plan                             8/N  │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.vertical_steps(
    title='Five steps to recover margin in two quarters',
    steps=[
        ('1', 'Diagnose', 'Identify SKU-level margin contribution'),
        ('2', 'Cluster',  'Group SKUs into top, mid, tail by margin'),
        ('3', 'Decide',   'Reprice top, bundle mid, sunset tail'),
        ('4', 'Execute',  'Roll out reprice in Q2; bundles in Q3'),
        ('5', 'Measure',  'Weekly margin tracker; cohort analysis'),
    ],
    source='Source: margin recovery plan',
)
```

### Pitfalls

- **More than 5 steps.** Step rows compress; the description font drops below 14pt and crowds. 5 is the soft cap.
- **Step titles longer than ~25 chars.** Title row is 0.4" tall; long titles wrap and collide with the description.
- **Using when sequence doesn't matter.** If the steps could be done in any order, use `four_column` or `metric_cards` instead — vertical_steps implies sequence, and using it for parallel items confuses the audience.

---

## `process_chevron`

Horizontal chevron / arrow flow. The most visually distinctive process layout — each step is a chevron-shaped box connected by a `→` arrow. The **last step gets navy fill** (the destination signal); all others get `BG_GRAY`.

### Signature

```python
eng.process_chevron(title, steps, source='', bottom_bar=None)
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `steps` | list of **3-tuples** `(label, step_title, description)` | yes | label ≤ 10 (no `\n`), step_title ≤ 20, desc ≤ 50 | **Max 5 steps** (S3 gate enforces). Step `label` is the small badge text — typically `'1'`, `'A'`, `'Q1'`, or a short phase name. **Cannot contain `\n`** (Oval shape can't accommodate multi-line). |
| `source` | str | data → yes | — | — |
| `bottom_bar` | tuple or `None` | no | — | Optional gray summary bar. |

The engine implements Rule 10 (horizontal overflow protection) here: chevron widths shrink dynamically so gaps stay positive even at 5 steps.

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Four phases of digital transformation                         │
│ ─────────────────────────────────────────────────             │
│  ┌─────────┐ → ┌─────────┐ → ┌─────────┐ → ┌─────────┐         │
│  │ ①       │   │ ②       │   │ ③       │   │ ④       │         │
│  │ Define  │   │ Build   │   │ Pilot   │   │ Scale   │ ← navy  │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘         │
│                                                                │
│  Stakeholder   Build MVP    Test in 2     Roll out             │
│  alignment     in 12 weeks  markets       to all               │
│  and KPIs                                  regions             │
│                                                                │
│ Source: digital transformation plan                       9/N │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.process_chevron(
    title='Four phases of digital transformation',
    steps=[
        ('1', 'Define', 'Stakeholder alignment and KPIs'),
        ('2', 'Build',  'Build MVP in 12 weeks'),
        ('3', 'Pilot',  'Test in 2 markets'),
        ('4', 'Scale',  'Roll out to all regions'),
    ],
    source='Source: digital transformation plan',
)
```

### Pitfalls

- **More than 5 steps.** Chevron arrow spacing collapses to negative values; the file may corrupt or render with overlapping shapes. **Hard cap: 5.** S3 gate enforces. ([`experiences/overflow.md` Experience 003](../../experiences/overflow.md).)
- **`\n` in step `label`.** Oval label has fixed 0.45" height; a multi-line label overflows by ~21%. S3 gate enforces. ([`experiences/overflow.md` Experience 004](../../experiences/overflow.md).)
- **Description > 50 chars.** Wraps and crowds adjacent chevrons. Keep terse.
- **Using for non-sequential items.** The `→` arrow implies causation / sequence. If the four items could be done in any order or are alternatives, use `four_column` or `metric_cards`.

---

## `value_chain`

Horizontal flow of accent-colored stages connected by light arrows. Use for end-to-end process / pipeline narratives (procurement → production → distribution → sales → service).

### Signature

```python
eng.value_chain(title, stages, source='', bottom_bar=None)
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `stages` | list of **3-tuples** `(stage_title, description, accent_color)` | yes | stage_title ≤ 15, desc ≤ 60 | Up to **5 stages**. Each stage gets a colored top accent (your `accent_color`) and a numbered circle. Stages auto-fill the full content width. |
| `source` | str | data → yes | — | — |
| `bottom_bar` | tuple or `None` | no | — | Optional gray summary bar. |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ End-to-end value chain — service is the under-invested stage │
│ ─────────────────────────────────────────────────             │
│ ┌───────┐ → ┌───────┐ → ┌───────┐ → ┌───────┐ → ┌───────┐     │
│ │■━━━━━━│   │■━━━━━━│   │■━━━━━━│   │■━━━━━━│   │■━━━━━━│     │
│ │①      │   │②      │   │③      │   │④      │   │⑤      │     │
│ │       │   │       │   │       │   │       │   │       │     │
│ │ Procure│   │ Build │   │ Ship  │   │ Sell  │   │ Serve │     │
│ │       │   │       │   │       │   │       │   │       │     │
│ │   80   │   │   85  │   │   90  │   │   88  │   │   62  │     │
│ │ NPS    │   │ qual. │   │ on-tm │   │ NPS   │   │ NPS   │     │
│ └───────┘   └───────┘   └───────┘   └───────┘   └───────┘     │
│                                                               │
│ Source: cross-functional review                          10/N │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
from mbb_ppt.constants import NAVY, ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED

eng.value_chain(
    title='End-to-end value chain — service is the under-invested stage',
    stages=[
        ('Procure', 'Supplier NPS 80; on-time delivery 92%', NAVY),
        ('Build',   'Quality score 85; defect rate 1.4%',    ACCENT_BLUE),
        ('Ship',    'On-time 90%; cost +3% vs plan',         ACCENT_GREEN),
        ('Sell',    'NPS 88; close rate 32%',                ACCENT_ORANGE),
        ('Serve',   'NPS 62; resolution time 4.2 days',      ACCENT_RED),
    ],
    source='Source: cross-functional review',
)
```

### Pitfalls

- **More than 5 stages.** Stage widths shrink below readable. Cap at 5.
- **Confusing with `process_chevron`.** Both render horizontal sequences. Distinction:
  - `process_chevron` → typically 4-step *project phases* (Define → Build → Pilot → Scale). Last step navy.
  - `value_chain` → typically 5-stage *enterprise value chain* (Procure → Build → Ship → Sell → Serve). Each stage gets its own accent color.
  - If your sequence is project-phase-like (each phase advances the *same* thing), use `process_chevron`. If it's enterprise-flow-like (each stage *transforms* something into the next), use `value_chain`.

---

## `decision_tree`

Hierarchical decision tree: root box → 2–4 L1 branches → multiple L2 children per branch. Use for issue-tree analysis or branching diagnostic frameworks.

### Signature

```python
eng.decision_tree(title, root, branches, right_panel=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `root` | tuple `(label,)` | yes | label ≤ 18 | Single-element tuple; the root question or hypothesis. Rendered in a navy box on the left. |
| `branches` | list of **4-tuples** `(L1_title, L1_metric, L1_color, children)` | yes | L1_title ≤ 14, L1_metric ≤ 8 | 2–4 L1 branches. `children` is `list[(name, metric)]` — the L2 leaves. Each L1 gets a colored box; L2 leaves get gray boxes. |
| `right_panel` | tuple `(panel_title, points)` or `None` | no | panel_title ≤ 20, point ≤ 60 | Optional right-side panel — typically the conclusion or implication of the tree. |
| `source` | str | data → yes | — | — |

### Example

```python
from mbb_ppt.constants import ACCENT_BLUE, ACCENT_ORANGE, ACCENT_GREEN

eng.decision_tree(
    title='Where does the margin gap come from?',
    root=('Margin -300 bps',),
    branches=[
        ('Volume',     '-50 bps',  ACCENT_BLUE,
         [('Premium', '-20 bps'), ('Standard', '-30 bps')]),
        ('Mix',        '-180 bps', ACCENT_ORANGE,
         [('Premium share',  '-90 bps'),
          ('Tail dilution', '-60 bps'),
          ('Channel mix',   '-30 bps')]),
        ('Cost',       '-70 bps',  ACCENT_GREEN,
         [('Input',     '-40 bps'),
          ('Logistics', '-30 bps')]),
    ],
    right_panel=('Implication',
                 ['Mix is 60% of the gap.',
                  'Premium share is the single largest lever.',
                  'Cost discipline is necessary but not sufficient.']),
    source='Source: margin diagnostic, Q1 2026',
)
```

### Pitfalls

- **Too many L1 branches.** Engine cycles through 4 colors (blue, orange, green, red); 5+ branches re-use colors and the visual breaks. Cap at 4.
- **L2 children unevenly distributed.** A branch with 1 child and another with 5 makes the slide visually lopsided. Aim for 2–3 children per branch.
- **Tree without conclusions.** A pure tree with no `right_panel` reads as analytical noise. Add the synthesis on the right.

---

## `agenda`

Time-allocated meeting agenda table. Items have variable arity — last element is `'key'` / `'normal'` / `'break'` to control visual treatment (key items get a star indicator; breaks get gray background).

### Signature

```python
eng.agenda(title, headers, items, footer_text='', source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `headers` | list of **2-tuples** `(label, width)` | yes | label ≤ 18 | Each header is `(label, Inches(width))`. **Last header is reserved for the type indicator** — its label can be empty. |
| `items` | list of variable-length tuples ending in type | yes | values match middle headers | `(*values, item_type)` where `item_type` ∈ `'key'`, `'normal'`, `'break'`. The `*values` length must equal `len(headers) - 1` (the last column is for the type indicator, rendered automatically). |
| `footer_text` | str | no | ≤ 80 | Optional footer line below the table. |
| `source` | str | data → yes | — | — |

### Example

```python
from pptx.util import Inches

eng.agenda(
    title='Board meeting agenda — Q1 review',
    headers=[
        ('Time',    Inches(1.4)),
        ('Item',    Inches(5.5)),
        ('Owner',   Inches(2.0)),
        ('Output',  Inches(2.8)),
        ('',        Inches(1.5)),   # type-indicator column
    ],
    items=[
        ('09:00', 'Welcome and Q1 highlights',       'CEO',         '—',           'normal'),
        ('09:15', 'Strategic recommendation',         'Strategy VP', 'Decision',    'key'),
        ('10:00', 'Coffee break',                     '',            '',            'break'),
        ('10:15', 'Financial review',                 'CFO',         'Awareness',   'normal'),
        ('11:00', 'Operational dashboard',            'COO',         'Awareness',   'normal'),
        ('11:30', 'Q&A and decision request',         'CEO',         'Approval',    'key'),
    ],
    footer_text='Decisions 1 and 5 require board vote.',
    source='Source: chair of the board',
)
```

### Pitfalls

- **`item` length doesn't match header count.** The engine pulls `*vals, itype = item` — if your items have 4 values but you have 6 headers (5 data + type), the trailing columns render empty. Validate.
- **Empty type column header.** Counterintuitively, the **last header column is for the type indicator** (the `★ Key` / blank / break visual), not a data column. Pass an empty string or short label.
- **Too many items.** 6–8 fits the slide comfortably; beyond 10, rows compress.

---

## `action_items`

Numbered action cards with timeline and owner. Up to 4 cards per slide. Use as the closing slide for a recommendation deck — gives the audience a concrete decision/action set.

### Signature

```python
eng.action_items(title, actions, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `actions` | list of **4-tuples** `(action_title, timeline, description, owner)` | yes | action_title ≤ 25, timeline ≤ 15, desc ≤ 80, owner ≤ 15 | Up to **4 actions**. Each action renders as a card: navy header (action_title), gray timeline strip, body description, and `Owner: {owner}` at the bottom. |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Four decisions and an owner for each                          │
│ ─────────────────────────────────────────────────             │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│ │ Decision 1 │ │ Decision 2 │ │ Decision 3 │ │ Decision 4 │   │
│ ├────────────┤ ├────────────┤ ├────────────┤ ├────────────┤   │
│ │ Q2 2026    │ │ Q2-Q3      │ │ Q3 2026    │ │ Q4 2026    │   │
│ ├────────────┤ ├────────────┤ ├────────────┤ ├────────────┤   │
│ │            │ │            │ │            │ │            │   │
│ │ Approve    │ │ Allocate   │ │ Sign       │ │ Brief      │   │
│ │ premium    │ │ $20M for   │ │ EMEA       │ │ board on   │   │
│ │ pricing    │ │ channel    │ │ distrib.   │ │ Q3 results │   │
│ │ test       │ │ expansion  │ │ contract   │ │            │   │
│ │            │ │            │ │            │ │            │   │
│ ├────────────┤ ├────────────┤ ├────────────┤ ├────────────┤   │
│ │ Owner: CEO │ │ Owner: CFO │ │ Owner: VP  │ │ Owner: CSO │   │
│ └────────────┘ └────────────┘ └────────────┘ └────────────┘   │
│                                                               │
│ Source: strategy team                                    11/N │
└───────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.action_items(
    title='Four decisions and an owner for each',
    actions=[
        ('Decision 1', 'Q2 2026',  'Approve premium pricing test',         'CEO'),
        ('Decision 2', 'Q2-Q3',    'Allocate $20M for channel expansion', 'CFO'),
        ('Decision 3', 'Q3 2026',  'Sign EMEA distributor contract',       'VP Sales'),
        ('Decision 4', 'Q4 2026',  'Brief board on Q3 results',            'CSO'),
    ],
    source='Source: strategy team',
)
```

### Pitfalls

- **More than 4 actions.** Cards shrink below readable. Cap at 4. If you have 5+ actions, prioritize and split into "this quarter" / "next quarter" slides.
- **Vague owners.** `'TBD'` or `'Various'` defeats the purpose. The audience should leave the slide knowing who's accountable for each.
- **Action without a deadline.** A timeline of `'TBD'` reads as not-actually-decided. If the deadline is genuinely uncertain, say so explicitly in the description.
- **Description that just restates the action title.** Use the description to add the *mechanism* or *expected outcome*, not to repeat the action.

---

## Cross-references

- **Method index:** [`../framework/engine-api.md`](../framework/engine-api.md).
- **Capacity matrix:** [`../layout-matrix.yaml`](../layout-matrix.yaml).
- **Past process-layout defects:** [`../../experiences/overflow.md`](../../experiences/overflow.md), [`../../experiences/layout-pitfalls.md`](../../experiences/layout-pitfalls.md).
- **Rule 8 (dynamic sizing for variable counts) + Rule 10 (horizontal overflow):** [`../framework/guard-rails.md`](../framework/guard-rails.md).
