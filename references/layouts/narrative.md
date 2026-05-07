# Layouts — Narrative

> **Loaded on demand at S4 (Render).** Open this file when rendering `executive_summary`, `key_takeaway`, `four_column`, `two_column_text`, `quote`, or `numbered_list_panel`. Two of these layouts (`executive_summary` and `key_takeaway`) anchor most of the slides 2–5 of any substantive deck; treat them as the default editorial choices.
>
> Capacity numbers are authoritative in [`../layout-matrix.yaml`](../layout-matrix.yaml).

---

## `executive_summary` ★

Navy headline band + numbered list of supporting items. The canonical opener for any deck where the recommendation has 2–4 supporting actions / arguments. Strongly preferred for slide 3 (immediately after cover and TOC).

### Signature

```python
eng.executive_summary(title, headline, items, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 (Rule 14); aim for ≤ 80 | Conclusion-led action title — usually the recommendation itself. |
| `headline` | str | yes | ≤ 60 chars | Rendered white on navy band. The governing-thought one-liner that frames the items below. |
| `items` | list of **3-tuples** `(num, item_title, description)` | yes | item_title ≤ 25, desc ≤ 80 | Max **4 items**. Tuple arity = 3 — the leading element is the visible identifier in the navy circle (`'1'`, `'A'`, `'I'`). |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Three actions return revenue to double-digit growth   ← title│
│ ─────────────────────────────────────────────────            │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓   │
│ ┃ Growth is concentrated in two channels and one tier     ┃ ← navy headline
│ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛   │
│                                                              │
│ ① Shift mix to premium    │  Higher margin, limited cost    │
│ ─────────────────────────────────────────────────            │
│ ② Expand in two channels  │  Distributors underpenetrated   │
│ ─────────────────────────────────────────────────            │
│ ③ Fund via simplification │  Back-office cost can shrink    │
│ ─────────────────────────────────────────────────            │
│                                                              │
│ Source: internal analysis, Q1 2026                       3/N │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.executive_summary(
    title='Three actions return revenue to double-digit growth',
    headline='Growth is concentrated in two channels and one product tier',
    items=[
        ('1', 'Shift mix to premium',
              'Higher margin, limited cost-to-serve impact'),
        ('2', 'Expand in two channels',
              'Two distributors are underpenetrated relative to peers'),
        ('3', 'Fund via simplification',
              'Back-office complexity can shrink without service hit'),
    ],
    source='Source: internal analysis, Q1 2026',
)
```

### Pitfalls

- **More than 4 items.** The engine doesn't crash but readability collapses — items become tightly packed at 0.6" each. Hard cap at 4. If you have 5+ supporting points, the top of the pyramid is too wide; consolidate.
- **Topic-as-item-title.** `('1', 'Market dynamics', '…')` defeats the layout. The item_title is the second-level headline of the pyramid; it must state a finding. Good: `('1', 'Shift mix to premium', '…')`. Bad: `('1', 'Premium analysis', '…')`.
- **Headline that repeats the title.** The headline is a *different* thought than the title — typically the *why*, where the title is the *what*. If they say the same thing, drop the headline or rewrite one of them.
- **Wrong tuple arity.** Engine expects 3-tuples. 2-tuples raise `ValueError`. ([`experiences/overflow.md` Experience 005](../../experiences/overflow.md).)

### Why this layout matters

`executive_summary` carries the deck's pyramid structure visibly on one slide. Done well, every other slide in the deck supports one of its items. Use it as the slide 3 anchor and refer back to its numbered structure in every section.

### Cross-references

- Capacity: `executive_summary` row in [`../layout-matrix.yaml`](../layout-matrix.yaml).
- Why slide 3: [`../framework/planning-guide.md`](../framework/planning-guide.md) § 4.

---

## `key_takeaway`

Left-side analysis paragraphs + right-side gray panel of takeaways. Use when one slide must hold both an analytical narrative and its synthesis side-by-side — typically a section closer or a synthesis slide.

### Signature

```python
eng.key_takeaway(title, left_text, takeaways, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `left_text` | list[str] | yes | ≤ 80 chars per paragraph | 3 paragraphs is the visual sweet spot; the left panel allocates ~4" of vertical space. |
| `takeaways` | list[str] | yes | ≤ 60 chars each | 2–4 short, declarative bullet takeaways shown on the right gray panel. |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Pricing power is concentrated where service quality is high │
│ ─────────────────────────────────────────────────            │
│ Synergy analysis              ┌──────────────────────────┐   │
│ ───────────────               │ Key Takeaways            │   │
│                               │ ─────────────────        │   │
│ Customers who rate service    │                          │   │
│ ≥ 8/10 accept 6–9% price      │ • Service NPS predicts   │   │
│ increases without churn.      │   pricing latitude       │   │
│                               │                          │   │
│ Below 8, churn rises 3× per   │ • The 8/10 threshold is  │   │
│ percentage point of price.    │   non-linear, not a      │   │
│                               │   gradient               │   │
│ Implication: pricing is a     │                          │   │
│ service-quality lever, not    │ • Invest in service in   │   │
│ a finance lever.              │   accounts before        │   │
│                               │   raising price          │   │
│                               └──────────────────────────┘   │
│ Source: customer cohort analysis                         8/N │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.key_takeaway(
    title='Pricing power is concentrated where service quality is high',
    left_text=[
        'Customers who rate service ≥ 8/10 accept 6–9% price increases without churn.',
        'Below 8, churn rises 3× per percentage point of price.',
        'Implication: pricing is a service-quality lever, not a finance lever.',
    ],
    takeaways=[
        'Service NPS predicts pricing latitude.',
        'The 8/10 threshold is non-linear, not a gradient.',
        'Invest in service in accounts before raising price.',
    ],
    source='Source: customer cohort analysis',
)
```

### Pitfalls

- **Hardcoded "Synergy analysis" left header.** The current engine renders `'Synergy analysis'` as the left-panel title — this is a fixed string in `engine.py`. If your slide is not about synergy, the header reads oddly. Workaround until a parameterizable version lands: keep the slide content phrased so "Synergy analysis" is plausible, or accept the mismatch as low-impact. (Tracked as a known UX issue; the right-panel "Key Takeaways" header is also fixed but is generic enough to fit any slide.)
- **Left text too long.** > 80 chars per paragraph at 14pt wraps to multiple lines and crowds the panel. Aim for sentence-length paragraphs.
- **Takeaways that restate the analysis verbatim.** Takeaways must be the synthesis — what the audience should *carry forward* — not a recap. If a takeaway is a paraphrase of a left_text line, drop it.
- **Using when content is one-sided.** If you don't have both an analytical narrative and a separate synthesis, use `executive_summary` (numbered + headline) or `table_insight` (data + insight) instead.

---

## `four_column`

Four parallel cards with numbered circles. Use for 3–4 parallel pillars / dimensions / capabilities where each item needs equal visual weight.

### Signature

```python
eng.four_column(title, items, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `items` | list of **3-tuples** `(num, col_title, description)` | yes | col_title ≤ 20, desc ≤ 120 | **Max 4 columns** — beyond 4, columns shrink below readable width. `description` accepts str or list[str]. |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Four pillars of the FY26 operating plan               ← title│
│ ─────────────────────────────────────────────────            │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│ │    ①     │ │    ②     │ │    ③     │ │    ④     │          │
│ │          │ │          │ │          │ │          │          │
│ │ Premium  │ │ Channel  │ │  Cost    │ │ Talent   │          │
│ │   mix    │ │ growth   │ │   disc.  │ │  bench   │          │
│ │ ───────  │ │ ───────  │ │ ───────  │ │ ───────  │          │
│ │ Reprice  │ │ Add 2    │ │ Reduce   │ │ Hire 12  │          │
│ │ premium  │ │ EMEA     │ │ overlap  │ │ senior   │          │
│ │ Q2-Q3.   │ │ distrs.  │ │ in svc.  │ │ engineers│          │
│ │ Margin   │ │ Reach +  │ │ ~$3M     │ │ by Q4.   │          │
│ │ +3-5pp.  │ │ 12% in   │ │ savings. │ │ Bench    │          │
│ │          │ │ mid-mkt. │ │          │ │ +20%.    │          │
│ │ (gray)   │ │ (gray)   │ │ (gray)   │ │ (gray)   │          │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
│                                                              │
│ Source: FY26 plan                                       4/N  │
└──────────────────────────────────────────────────────────────┘
```

All four cards use `BG_GRAY` background by default — visually parallel.

### Example

```python
eng.four_column(
    title='Four pillars of the FY26 operating plan',
    items=[
        ('1', 'Premium mix',
              'Reprice premium Q2–Q3. Margin +3-5pp.'),
        ('2', 'Channel growth',
              'Add 2 EMEA distributors. Reach +12% in mid-market.'),
        ('3', 'Cost discipline',
              'Reduce overlap in shared services. ~$3M savings.'),
        ('4', 'Talent bench',
              'Hire 12 senior engineers by Q4. Bench +20%.'),
    ],
    source='Source: FY26 plan',
)
```

### Pitfalls

- **More than 4 columns.** Hard limit. The S3 gate flags this. ([`experiences/overflow.md` Experience 002](../../experiences/overflow.md).)
- **Wrong tuple arity.** 3-tuples required. 2-tuples raise `ValueError`. ([`experiences/overflow.md` Experience 005](../../experiences/overflow.md).)
- **Imbalanced description lengths.** A column with 30 chars of description next to one with 110 chars looks broken. Aim for descriptions within ±20% of each other.
- **Confusing with `metric_cards`.** `four_column` cards are uniformly gray (no accent strip, no metric value); `metric_cards` have a colored accent strip and emphasize a value. Use `four_column` for *parallel narrative chunks*, `metric_cards` for *parallel KPIs*.

### Cross-references

- Capacity: `four_column` row in [`../layout-matrix.yaml`](../layout-matrix.yaml).

---

## `two_column_text`

Two lettered columns with bullet lists. **At most one slide of this type per deck** (`global_max_per_deck = 1` in the layout matrix).

### Signature

```python
eng.two_column_text(title, columns, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `columns` | list of 2 × **3-tuples** `(letter, col_title, points)` | yes | col_title ≤ 25, point ≤ 60 chars | Exactly 2 columns. `letter` is the visible circle label (`'A'`, `'B'`). `points` is `list[str]` of bullets, max 5 each. |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Pricing approach differs across regulated and free markets   │
│ ─────────────────────────────────────────────────            │
│  Ⓐ  Regulated markets               Ⓑ  Free markets          │
│ ───────────────────────             ────────────────────     │
│  • Price ceilings set by regulator   • Price set by market   │
│  • Margin compression annual         • Margin tracks demand  │
│  • Volume growth via mandate         • Volume tracks brand   │
│  • Service is a compliance lever     • Service is a price    │
│  • Innovation differentiates           lever                 │
│                                      • Innovation drives mix │
│                                                              │
│ Source: regional team analysis                          7/N  │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.two_column_text(
    title='Pricing approach differs across regulated and free markets',
    columns=[
        ('A', 'Regulated markets', [
            '• Price ceilings set by regulator',
            '• Margin compression annual',
            '• Volume growth via mandate',
            '• Service is a compliance lever',
            '• Innovation differentiates',
        ]),
        ('B', 'Free markets', [
            '• Price set by market',
            '• Margin tracks demand',
            '• Volume tracks brand',
            '• Service is a price lever',
            '• Innovation drives mix',
        ]),
    ],
    source='Source: regional team analysis',
)
```

### Pitfalls

- **Used more than once per deck.** Hard rule. The S3 gate enforces. ([`experiences/layout-pitfalls.md` Experience 001](../../experiences/layout-pitfalls.md).) Reason: visual monotony — a deck with multiple two_column_text slides reads as bullet-heavy and unargued. Use `side_by_side` (which this layout's name doesn't suggest but isn't equivalent to — `side_by_side` is for option comparisons; `two_column_text` is for parallel topics with bullets).
- **One column much longer than the other.** The columns render top-aligned, so a long left column and short right column leave visible right-side whitespace. Balance bullet counts within ±1.
- **Bullet text without `•` prefix.** The engine does NOT auto-prefix; pass the bullet character in the string. Otherwise the lines render flat without visual enumeration.

---

## `quote`

Centered quotation with accent rules above and below. Editorial slide — no action title, no source line, no traditional content area.

### Signature

```python
eng.quote(quote_text, attribution='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `quote_text` | str | yes | ≤ 200 chars; aim for ≤ 120 | Rendered at 24pt `DARK_GRAY`, centered, in body font. |
| `attribution` | str | no | ≤ 60 chars | 14pt `MED_GRAY`, centered, below the quote. Format: `'— Name, Role'` or `'— Source, Year'`. |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐ ← navy top accent
│                                                              │
│                   ━━━━━━━━━━━━━                              │
│                                                              │
│                                                              │
│       "We were not losing to better products. We were        │
│        losing to better service in the same product."        │
│                                                              │
│                                                              │
│                   ━━━━━━━━━━━━━                              │
│                                                              │
│              — VP Sales, customer offsite, Q4 2025           │
│                                                              │
│                                                          5/N │
└──────────────────────────────────────────────────────────────┘
```

Note: `quote` does NOT call `add_action_title()` — the slide intentionally has no title bar. It also does NOT add a source line (the attribution serves that role).

### Example

```python
eng.quote(
    quote_text='"We were not losing to better products. We were losing '
               'to better service in the same product."',
    attribution='— VP Sales, customer offsite, Q4 2025',
)
```

### Pitfalls

- **Long quotes.** > ~200 chars wraps to 4+ lines and the centered alignment becomes hard to read. Trim or split into two quotes on consecutive slides.
- **No attribution.** A quote without attribution reads as anonymous and weakens the rhetorical effect. Always attribute.
- **Using as a section divider substitute.** `quote` is a punctuation slide — one in a 12-slide deck, maybe two. Multiple consecutive quotes feel theatrical; use `section_divider` for transitions.
- **Quote that paraphrases the action title elsewhere.** The quote should stand alone. If it just restates a finding from another slide, it's redundant.

---

## `numbered_list_panel`

Left-side numbered list (5–7 items with title + description) + optional right-side navy panel with metrics. Use for recommendations, action lists, or capabilities where the item count is too high for `executive_summary` (≤ 4) but each item still needs a short description.

### Signature

```python
eng.numbered_list_panel(title, items, panel=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `items` | list of **2-tuples** `(item_title, description)` | yes | item_title ≤ 30, desc ≤ 80 | Note: 2-tuples (different from `executive_summary`'s 3-tuples — the engine auto-numbers). 5–7 items recommended. |
| `panel` | dict or `None` | no | — | Optional right-side panel. Keys: `'subtitle'` (gray text), `'big_number'` (large white), `'big_label'` (small gray under number), `'metrics'` (list of `(label, value)` rows). |
| `source` | str | data → yes | — | — |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Six recommendations to recover growth                  ← title│
│ ─────────────────────────────────────────────────            │
│  ① Reprice premium tier              ┌──────────────────┐   │
│     +3-5pp margin, no volume hit     │ FY26 Plan        │   │
│ ─────────────────────────────────    │                  │   │
│  ② Add EMEA distributors             │   $1.2B          │   │
│     Reach +12% in mid-market         │   target revenue │   │
│ ─────────────────────────────────    │   ───────        │   │
│  ③ Reduce shared-service overlap     │   Margin   31%   │   │
│     ~$3M annualized savings          │   Growth   +12%  │   │
│ ─────────────────────────────────    │   NPS      +8    │   │
│  ④ Hire 12 senior engineers          │                  │   │
│     Capability bench +20%            │                  │   │
│ ─────────────────────────────────    │                  │   │
│  ⑤ Pilot 2 new product bundles       │                  │   │
│     Q3 launch, Q4 measure            │                  │   │
│                                      └──────────────────┘   │
│ Source: FY26 plan                                       9/N  │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.numbered_list_panel(
    title='Six recommendations to recover growth',
    items=[
        ('Reprice premium tier',          '+3-5pp margin, no volume hit'),
        ('Add EMEA distributors',         'Reach +12% in mid-market'),
        ('Reduce shared-service overlap', '~$3M annualized savings'),
        ('Hire 12 senior engineers',      'Capability bench +20%'),
        ('Pilot 2 new product bundles',   'Q3 launch, Q4 measure'),
    ],
    panel={
        'subtitle': 'FY26 Plan',
        'big_number': '$1.2B',
        'big_label': 'target revenue',
        'metrics': [
            ('Margin', '31%'),
            ('Growth', '+12%'),
            ('NPS',    '+8'),
        ],
    },
    source='Source: FY26 plan',
)
```

### Pitfalls

- **Wrong tuple arity.** This layout uses **2-tuples** for items (different from `executive_summary` and `four_column` which use 3-tuples). Numbering is automatic.
- **Too few items.** With < 4 items, `executive_summary` gives a tighter visual. Use `numbered_list_panel` only when you have 5+ items that each need a description.
- **Panel without data.** If you don't have a meaningful big_number / metrics for the panel, omit `panel=` entirely. An empty navy panel reads as a placeholder.
- **Item descriptions that just rephrase the title.** Each description must add information beyond the title — typically the *expected impact* or *mechanism*. If it just paraphrases the title, drop it and let the title carry alone.

---

## Cross-references

- **Method index:** [`../framework/engine-api.md`](../framework/engine-api.md).
- **Capacity matrix:** [`../layout-matrix.yaml`](../layout-matrix.yaml).
- **Production rules:** [`../framework/guard-rails.md`](../framework/guard-rails.md).
- **When to lead with `executive_summary` vs `key_takeaway`:** [`../framework/planning-guide.md`](../framework/planning-guide.md) § 4.
- **Past defects in these layouts:** [`../../experiences/`](../../experiences/).
