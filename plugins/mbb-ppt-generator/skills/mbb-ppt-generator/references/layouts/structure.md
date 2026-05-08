# Layouts — Structure & Navigation

> **Loaded on demand at S4 (Render).** Open this file when you are about to render a `cover`, `toc`, `section_divider`, `closing`, or `appendix_title` slide and want the parameter contract, capacity limits, common pitfalls, and a wireframe sketch.
>
> Capacity numbers are authoritative in [`../layout-matrix.yaml`](../layout-matrix.yaml). This file's matrix references are summaries.

---

## `cover`

The first slide of every deck. Title + optional subtitle + optional author + date, with a navy accent line at top and a 2pt navy underline near the bottom.

### Signature

```python
eng.cover(title, subtitle='', author='', date='', cover_image=None)
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 40 chars per line; multi-line supported via `\n` | Rendered at 44pt navy bold in `HEADING_FONT` (DM Sans). Height auto-computed from line count. |
| `subtitle` | str | no | ≤ 60 chars | Rendered at 22pt `DARK_GRAY`. Positioned dynamically below the title. |
| `author` | str | no | ≤ 30 chars | 14pt `MED_GRAY`. |
| `date` | str | no | ≤ 30 chars | 14pt `MED_GRAY`. Format flexibly: `'March 2026'`, `'Q1 2026'`, `'2026-03-15'`. |
| `cover_image` | str/`None` | no | — | `None` (default, text only) or a local image file path (full-bleed background). |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐ ← navy top accent (0.05" tall)
│                                                              │
│                                                              │
│    Q1 2026 strategy review                  ← title (44pt)   │
│                                                              │
│    Board update — three actions to recover  ← subtitle (22pt)│
│                                                              │
│                                                              │
│    Strategy team                            ← author (14pt)  │
│    March 2026                               ← date (14pt)    │
│                                                              │
│                                                              │
│    ━━━━━━━━━━━                              ← navy 2pt rule  │
└──────────────────────────────────────────────────────────────┘
```

If a `cover_image` is provided, the text shifts to the left half; otherwise it occupies the central area.

### Example

```python
eng.cover(
    title='Q1 2026 strategy review',
    subtitle='Board update — three actions to recover growth',
    author='Strategy team',
    date='March 2026',
)
```

### Pitfalls

- **Title overflow with `\n`.** The engine auto-computes height from line count; do not hand-pad the title with whitespace. (See [`experiences/layout-pitfalls.md` Experience 002](../../experiences/layout-pitfalls.md).)
- **Cover slides do not get a page number.** This is by design (`add_page_number()` is not called for `cover`); do not patch it in.

### Cross-references

- Capacity: [`../layout-matrix.yaml`](../layout-matrix.yaml) → `cover`.
- Cover-image security posture: [`../../SKILL.md`](../../SKILL.md) § 13.

---

## `toc`

Table of contents with numbered items and short descriptions. One row per major section. Loaded after the cover; skipped in short / decision-meeting decks.

### Signature

```python
eng.toc(title='Table of Contents', items=None, source='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | no | ≤ 15 chars | Default `'Table of Contents'`. Override only if a different word fits the deck (e.g. `'Agenda'`). |
| `items` | list of 3-tuples | yes | item_title ≤ 20, desc ≤ 40 | Each item is `(num, item_title, description)`. **Tuple arity = 3.** Max 6 items. |
| `source` | str | no | — | Optional source attribution. |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│ Table of Contents                              ← action title│
│ ─────────────────────────────────────────────────            │
│                                                              │
│ ① Executive summary    Recommendation and key evidence       │
│ ─────────────────────────────────────────────────            │
│ ② Market dynamics      Where pressure and opportunity shift  │
│ ─────────────────────────────────────────────────            │
│ ③ Strategic actions    Three moves to accelerate growth      │
│ ─────────────────────────────────────────────────            │
│ ④ Implementation       Phased rollout with risk gates        │
│ ─────────────────────────────────────────────────            │
│                                                              │
│                                                            4/N│
└──────────────────────────────────────────────────────────────┘
```

The numbered circle is `add_oval()` (NAVY background, white digit).

### Example

```python
eng.toc(items=[
    ('1', 'Executive summary', 'Recommendation and key evidence'),
    ('2', 'Market dynamics',  'Where pressure and opportunity shift'),
    ('3', 'Strategic actions', 'Three moves to accelerate growth'),
    ('4', 'Implementation',    'Phased rollout with risk gates'),
])
```

### Pitfalls

- **Topic-only descriptions.** Descriptions like `'Background information'` or `'Overview of the project'` defeat the purpose. Each description should preview the section's *finding*, not name the section. Bad: `'Market dynamics'`. Good: `'Where pressure and opportunity shift'`.
- **Wrong tuple arity.** Passing `('Title', 'desc')` (2 elements) raises `ValueError`. Always include the leading number/identifier as the first element. ([`experiences/overflow.md` Experience 005](../../experiences/overflow.md).)
- **Skipping the TOC for senior audiences.** A 6-slide senior briefing should not have a TOC — it costs an entire slide of attention you cannot afford. Use the *short deck* template ([`../framework/planning-guide.md`](../framework/planning-guide.md) § 2).

### Cross-references

- Capacity: `toc` row in [`../layout-matrix.yaml`](../layout-matrix.yaml).

---

## `section_divider`

Chapter transition. Used between major sections in a 10+ slide deck. Visual: navy bar down the left edge, large section label, large title.

### Signature

```python
eng.section_divider(section_label, title, subtitle='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `section_label` | str | yes | short, e.g. `'01'`, `'Part II'`, `'Section A'` | 18pt `MED_GRAY` `HEADING_FONT`. Sits above the title. |
| `title` | str | yes | ≤ 40 chars | 28pt navy bold. The section's headline. |
| `subtitle` | str | no | ≤ 80 chars | 14pt `DARK_GRAY`. Use to preview the section's argument. |

### Wireframe

```
┌──┬───────────────────────────────────────────────────────────┐
│  │                                                           │
│  │  01                              ← section_label (18pt)   │
│  │                                                           │
│  │  Strategic actions               ← title (28pt navy bold) │
│  │                                                           │
│  │  Three complementary moves       ← subtitle (14pt)        │
│  │  to recover growth                                        │
│  │                                                           │
│  │                                                           │
│  │                                                       3/N │
└──┴───────────────────────────────────────────────────────────┘
   ↑
   navy 0.6" left bar runs full slide height
```

### Example

```python
eng.section_divider(
    section_label='02',
    title='Strategic actions',
    subtitle='Three complementary moves to recover growth',
)
```

### Pitfalls

- **Using as a content slide.** `section_divider` has no body area — do not try to cram bullets or charts. If you need content, use `executive_summary` or `key_takeaway`.
- **Generic section labels.** `'Section'` or `'Part'` alone is wasted space. Either use a number (`'02'`) or omit the label entirely (pass `''`).
- **Subtitle as topic name.** Like the TOC, the subtitle should preview the *finding*, not the topic. Bad: `'Market overview'`. Good: `'Share is shifting toward low-cost entrants'`.

---

## `closing`

Final slide. Centered title + optional message + accent rules. Conventional uses: "Thank you", "Discussion and decision points", "Q&A".

### Signature

```python
eng.closing(title, message='', source_text='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 30 chars | 28pt navy bold, centered. |
| `message` | str | no | ≤ 60 chars | 18pt `DARK_GRAY`, centered. |
| `source_text` | str | no | — | Optional small-text citation at the bottom. Rare. |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐ ← navy top accent
│                                                              │
│                                                              │
│                                                              │
│                       Thank you                              │
│                       ━━━━━━                                 │
│                                                              │
│            Discussion and decision points                    │
│                                                              │
│                                                              │
│                                                              │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━              │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.closing(
    title='Thank you',
    message='Discussion and decision points',
)
```

### Pitfalls

- **Including action items on the closing.** If the audience needs to leave with action items, the slide *before* the closing should be `action_items`. The closing itself is for closure, not work assignment.
- **No page number.** Like the cover, the closing does not get a page number. By design.
- **Long titles.** A closing title over 30 chars wraps awkwardly because the layout centers it. Keep it short — the message line carries any longer phrasing.

---

## `appendix_title`

Back-matter separator. Used between the main deck and an appendix of supporting tables / detailed data / glossary. Visual: centered title with thin accent lines top and bottom.

### Signature

```python
eng.appendix_title(title, subtitle='')
```

### Parameters

| Name | Type | Required | Char budget | Notes |
|---|---|---|---|---|
| `title` | str | yes | ≤ 40 chars | 28pt navy bold, centered. |
| `subtitle` | str | no | — | 14pt `DARK_GRAY`, centered, below the title. |

### Wireframe

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│                                                              │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━              │
│                                                              │
│                       Appendix                               │
│                                                              │
│             Supporting analysis and details                  │
│                                                              │
│   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━              │
│                                                              │
│                                                       12/N   │
└──────────────────────────────────────────────────────────────┘
```

### Example

```python
eng.appendix_title(
    title='Appendix',
    subtitle='Supporting analysis and detailed exhibits',
)
```

### Pitfalls

- **Appendix slide without an appendix.** If you do not have at least 2–3 appendix slides to follow, drop the divider. A standalone appendix slide with nothing after it is confusing.
- **Confusing with section_divider.** Use `section_divider` between *main* sections (chapters); use `appendix_title` only at the boundary between the main deck and back-matter.

---

## Cross-references

- **Method index for these and all other layouts:** [`../framework/engine-api.md`](../framework/engine-api.md).
- **Capacity matrix:** [`../layout-matrix.yaml`](../layout-matrix.yaml).
- **Production rules these layouts must satisfy:** [`../framework/guard-rails.md`](../framework/guard-rails.md).
- **Slide-2-through-5 priority (which layouts to lead with after cover/TOC):** [`../framework/planning-guide.md`](../framework/planning-guide.md) § 4.
- **Engine source (authoritative):** `../../mbb_ppt/engine.py`.
