# Layouts — Image and Visual

> **Loaded on demand at S4 (Render).** Open this file when rendering `content_right_image`, `three_images`, `image_four_points`, `full_width_image`, `case_study_image`, `quote_bg_image`, `goals_illustration`, or `two_col_image_grid`.
>
> All image layouts use `add_image_placeholder()` — a gray rectangle with crosshair lines and a label. **Users replace these with real images in PowerPoint after generation.** The engine does not embed real images automatically. The `image_label` parameter on each method controls what text appears inside the placeholder.

---

## `content_right_image`

Text on the left (subtitle + bullets + optional takeaway), image placeholder on the right. Use for slides where text is the primary content but a supporting visual reinforces.

### Signature

```python
eng.content_right_image(title, subtitle, bullets, takeaway='',
                        image_label='Image', source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `subtitle` | str | yes | ≤ 40 | Sub-header above the bullets, navy bold. |
| `bullets` | list[str] | yes | each ≤ 60 chars | Body bullets. ≤ 6 items. Pre-format with `•` prefix. |
| `takeaway` | str | no | ≤ 100 chars | Optional gray panel below the bullets with the slide takeaway. |
| `image_label` | str | no | ≤ 20 chars | Placeholder label visible on the gray rectangle. |
| `source` | str | data → yes | — | — |

### Example

```python
eng.content_right_image(
    title='Premium customers value service over feature breadth',
    subtitle='Survey findings, n=1,200',
    bullets=[
        '• 74% rate service quality as primary driver',
        '• 52% would pay 8% more for guaranteed response time',
        '• Only 18% cite feature breadth as a top-3 driver',
        '• Brand reputation matters more for first purchase than for renewal',
    ],
    takeaway='Invest in service throughput before adding features.',
    image_label='Customer survey infographic',
    source='Source: customer survey, Q4 2025',
)
```

### Pitfalls

- **Image placeholder forgotten in delivery.** Operators sometimes deliver the `.pptx` with the gray placeholder still showing because they forgot to swap in the real image. Either swap the image before sending OR remove the placeholder if you don't have a real image to add.
- **Bullets > 60 chars.** Wraps and crowds. Keep terse — narrative goes in `key_takeaway` instead.

---

## `three_images`

Three-column image+caption layout. Use for product comparisons, case-study triads, or any visual triplet with parallel structure.

### Signature

```python
eng.three_images(title, items, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `items` | list of **3 × 3-tuples** `(caption_title, description, image_label)` | yes | caption_title ≤ 25, desc ≤ 60, image_label ≤ 20 | Exactly 3 items. Each renders as a column with image on top and text below. |
| `source` | str | data → yes | — | — |

### Example

```python
eng.three_images(
    title='Three product tiers — premium drives margin, entry drives volume',
    items=[
        ('Premium',  '15% volume share, 38% margin contribution',
                     'Premium product photo'),
        ('Standard', '50% volume share, 45% margin contribution',
                     'Standard product photo'),
        ('Entry',    '35% volume share, 17% margin contribution',
                     'Entry-level product photo'),
    ],
    source='Source: product portfolio analysis',
)
```

### Pitfalls

- **More or fewer than 3 items.** Layout is fixed 3-column. Pass exactly 3.
- **Mixed parallel structures.** All three captions should follow the same template — same kind of metric, same length, same tone. Inconsistency reads as imbalance.

---

## `image_four_points`

Center image with 4 callout cards in the corners. Use for "this image illustrates these four properties" — typical for diagram annotations or "anatomy of X" slides.

### Signature

```python
eng.image_four_points(title, image_label, points, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `image_label` | str | yes | ≤ 20 chars | Label on the central placeholder. |
| `points` | list of **4 × 3-tuples** `(point_title, description, accent_color)` | yes | point_title ≤ 18, desc ≤ 50 | Exactly 4 points. The fourth element (`accent_color`) is optional — defaults cycle through ACCENT_BLUE / GREEN / ORANGE / RED. |
| `source` | str | data → yes | — | — |

### Example

```python
from mbb_ppt.constants import ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED

eng.image_four_points(
    title='Four properties of a healthy operating model',
    image_label='Operating-model diagram',
    points=[
        ('Clarity',    'Roles and decision rights are explicit',  ACCENT_BLUE),
        ('Cadence',    'Regular review meetings with KPI focus',  ACCENT_GREEN),
        ('Capability', 'Skills match the role expectations',      ACCENT_ORANGE),
        ('Culture',    'Values reinforce desired behaviors',      ACCENT_RED),
    ],
    source='Source: operating-model framework',
)
```

### Pitfalls

- **Tuple arity.** 3-tuples; 4th element (accent color) optional. The engine picks defaults, but specifying explicit colors matches the deck's color discipline better.
- **More or fewer than 4 points.** Fixed 4-corner layout. Pass exactly 4.
- **Image in the placeholder doesn't match the four points.** The slide's logic is "image illustrates these properties." If the image is decorative rather than illustrative, use `content_right_image` or `four_column` instead.

---

## `full_width_image`

Edge-to-edge hero image with a semi-transparent overlay band carrying a title and attribution. Editorial / opener / section-divider slide.

### Signature

```python
eng.full_width_image(title, image_label, overlay_text='', attribution='',
                     source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | — | The action title is *not rendered* on this layout — see pitfalls. Pass it for the page-number / source machinery, but don't expect it on screen. |
| `image_label` | str | yes | ≤ 20 chars | Label on the full-bleed placeholder. |
| `overlay_text` | str | no | ≤ 80 chars | Large white-on-navy-overlay text (28pt, bold, centered). |
| `attribution` | str | no | ≤ 60 chars | Small light-gray text below the overlay. Format: `'— Source / Photographer / Year'`. |
| `source` | str | no | — | Optional bottom source line. |

The overlay band sits at `y = 4.0"` to `y = 6.0"` with 70% opacity; text inside the band reads white-on-navy.

### Example

```python
eng.full_width_image(
    title='Section divider — market backdrop',
    image_label='Hero image of Tokyo skyline at dusk',
    overlay_text='The next decade will be won in Asia-Pacific',
    attribution='— industry analyst, 2026',
    source='Source: market backdrop',
)
```

### Pitfalls

- **No action title rendered.** This layout is intentionally headerless — the overlay text replaces the title bar. Don't expect the engine's normal title-bar treatment.
- **Overlay text too long.** > 80 chars wraps onto 3+ lines and the overlay band loses its impact.
- **Confusing with `quote`.** `full_width_image` carries an image; `quote` is text-only. Use `full_width_image` when the visual matters; use `quote` when the words alone carry the slide.

---

## `case_study_image`

Left column with stacked text sections, right column with image and KPI cards. Use for case-study deep-dives that need both narrative and quantitative anchors.

### Signature

```python
eng.case_study_image(title, sections, image_label, kpis=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `sections` | list of **3-tuples** `(label, text, accent_color)` | yes | label ≤ 14, text ≤ 100 | 2–3 sections recommended. Each gets a colored vertical strip and a label header. Conventional pattern: Situation / Action / Result (S/A/R). |
| `image_label` | str | yes | ≤ 20 chars | Label on the right-side placeholder. |
| `kpis` | list of `(value, label)` 2-tuples or `None` | no | value ≤ 8, label ≤ 18 | Optional bottom-right KPI strip. 2–4 KPIs recommended. |
| `source` | str | data → yes | — | — |

### Example

```python
from mbb_ppt.constants import ACCENT_BLUE, ACCENT_ORANGE, ACCENT_GREEN

eng.case_study_image(
    title='Case study — Acme reduced churn 40% in 18 months',
    sections=[
        ('Situation', 'Churn at 24% annually; service NPS 6.2/10', ACCENT_BLUE),
        ('Action',    'Service redesign + 30 senior hires + retention bonuses',
                      ACCENT_ORANGE),
        ('Result',    'Churn at 14%; NPS 8.4/10; net retention 110%',
                      ACCENT_GREEN),
    ],
    image_label='Acme service team photo',
    kpis=[
        ('-40%', 'Churn'),
        ('+22',  'NPS pts'),
        ('110%', 'Net retention'),
    ],
    source='Source: Acme case file, FY25',
)
```

### Pitfalls

- **More than 3 sections.** Sections compress vertically and lose the S/A/R cadence.
- **KPIs not aligned with the result section.** The KPI strip exists to numerically reinforce the result. If the KPIs don't tie back to "Result", they look like an afterthought.

---

## `quote_bg_image`

Top half image, bottom half white card with quote and attribution between two navy rules. More editorial than `quote` (no image) — use when the speaker / context image strengthens the rhetorical effect.

### Signature

```python
eng.quote_bg_image(image_label, quote_text, attribution='', source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `image_label` | str | yes | ≤ 20 chars | Label on the top-half placeholder. |
| `quote_text` | str | yes | ≤ 180 chars | Centered navy bold 24pt. |
| `attribution` | str | no | ≤ 60 chars | Speaker / context citation under the quote. |
| `source` | str | no | — | Optional small footer. |

Note: there is no `title` parameter — the layout is title-free by design.

### Example

```python
eng.quote_bg_image(
    image_label='Photo of executive offsite',
    quote_text='"We did not lose to better products. We lost to better service.”',
    attribution='— VP Sales, customer offsite, Q4 2025',
    source='Source: offsite transcript',
)
```

### Pitfalls

- **Quote longer than ~180 chars.** Crowds the white panel. Trim or split into two slides.
- **No attribution.** Anonymous quotes weaken rhetorical effect.

---

## `goals_illustration`

Left column of numbered goals (with colored vertical strip + circle), right column image. Use for OKR / goal-setting slides where each goal needs a one-line description plus a supporting visual.

### Signature

```python
eng.goals_illustration(title, goals, image_label, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `goals` | list of **3-tuples** `(goal_title, description, accent_color)` | yes | goal_title ≤ 25, desc ≤ 60 | 4–5 goals recommended. Each gets a numbered circle + colored strip. |
| `image_label` | str | yes | ≤ 20 chars | Right-side placeholder label. |
| `source` | str | data → yes | — | — |

### Example

```python
from mbb_ppt.constants import ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED, NAVY

eng.goals_illustration(
    title='FY26 OKRs — five goals across growth, margin, and capability',
    goals=[
        ('Revenue growth +12%',  'Premium mix shift + EMEA expansion', NAVY),
        ('Margin +3pp',          'Cost simplification + repricing',    ACCENT_BLUE),
        ('NPS +5 pts',           'Service capacity + tooling',         ACCENT_GREEN),
        ('Talent bench +20%',    '12 senior hires + 30 internal moves',ACCENT_ORANGE),
        ('Sustainability score', 'Top-quartile in industry index',     ACCENT_RED),
    ],
    image_label='Strategic priorities visual',
    source='Source: FY26 plan',
)
```

### Pitfalls

- **More than 5 goals.** Rows compress; the numbered circles get cramped. Cap at 5; consider whether you really have 6+ true OKRs or just a list of activities.

---

## `two_col_image_grid`

2×2 grid of image + text cards. Use for product / capability / region grids where each item has an image and a short description.

### Signature

```python
eng.two_col_image_grid(title, items, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 120 | — |
| `items` | list of **4 × 4-tuples** `(card_title, description, accent_color, image_label)` | yes | card_title ≤ 25, desc ≤ 80, image_label ≤ 18 | Exactly 4 items (fills a 2×2 grid). Each card has an image on the left and text on the right with a colored strip. |
| `source` | str | data → yes | — | — |

### Example

```python
from mbb_ppt.constants import ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED

eng.two_col_image_grid(
    title='Four regional growth stories',
    items=[
        ('North America', 'Mature; mid-single-digit growth',          ACCENT_BLUE,
         'NA office photo'),
        ('EMEA',          'Two distributors closing; +12% addressable',ACCENT_GREEN,
         'EMEA team photo'),
        ('LATAM',         'New hire, ramp expected H2',                ACCENT_ORANGE,
         'LATAM site photo'),
        ('APAC',          'Joint venture under negotiation',           ACCENT_RED,
         'APAC partner photo'),
    ],
    source='Source: regional pipeline review',
)
```

### Pitfalls

- **Wrong tuple arity.** 4-tuples — easy to forget the `image_label`.
- **More or fewer than 4 items.** Layout is fixed 2×2; pass exactly 4.
- **Decorative-only images.** Each card's image should reinforce its specific text — generic stock photos applied to all four cards weaken the slide.

---

## Cross-references

- **Method index:** [`../framework/engine-api.md`](../framework/engine-api.md).
- **Capacity matrix:** [`../api-schemas.yaml`](../api-schemas.yaml).
- **Visual-relief slide rule (Rule 7 — at least one image slide in 8+ decks):** [`../framework/guard-rails.md`](../framework/guard-rails.md).
- **`add_image_placeholder()` implementation:** `mbb_ppt/core.py`.
