# Presentation Convention

> **Loaded optionally at S4 (Render+QA)** for margin and source-line confirmation. Team-level layout convention. Applies to every deck.
>
> Adapted to English from Likaku's `Mck-ppt-design-skill v2.3.3` `references/team/presentation-convention.md`. Apache 2.0.

---

## Slide dimensions — 16:9 wide

```python
prs.slide_width  = Inches(13.333)   # 16:9 widescreen
prs.slide_height = Inches(7.5)
```

The engine sets these in `MckEngine.__init__()`; do not override.

## Standard margins

| Position | Size | Use |
|---|---|---|
| Left margin (`LM`) | `0.8"` | Default left edge for all content |
| Right margin (`RM`) | `0.8"` | Default right edge |
| Content width (`CW`) | `11.733"` | `slide_width − LM − RM` |
| Action title top | `0.15"` | Top of title bar |
| Action title height | `0.9"` | Height of title bar |
| Title separator line | `1.05"` | y-coordinate of the under-title rule |
| Content area start | `1.3–1.4"` | First content shape begins below the separator |
| Source line | `7.05"` | Bottom-left source attribution baseline |
| Page number | `(9.3", 7.05")` | Locked bottom-right per Rule 18 |

## Hard content boundary (Rule 15, this skill)

```
CONTENT_LEFT        = Inches(0.5)
CONTENT_TOP_BOUND   = Inches(1.1)
CONTENT_RIGHT       = Inches(9.5)
CONTENT_BOTTOM      = Inches(6.9)
```

No shape, text box, or chart may be placed outside these coordinates. The render gate validates this. The legacy `LM` / `RM` margins (0.8") sit *inside* this hard boundary, so a shape using `LM` is automatically inside Rule 15's envelope.

## Mandatory slide elements

Every content slide (everything except `cover` and `closing`) **must** include:

| Element | Method | Position |
|---|---|---|
| Action title | `add_action_title()` (called automatically by every layout method) | Top, `y = 0.15"`, height `0.9"` |
| Title separator line | Drawn by `add_action_title()` | `y = 1.05"`, full content width |
| Content area | Layout-specific — see `references/layouts/*.md` | `y = 1.3"` to `~6.5"` |
| Source attribution | `add_source(slide, "Source: …")` (called via `_footer()` when caller passes `source=`) | Bottom-left, `y = 7.05"` |
| Page number | `add_page_number(slide, n, total)` (called via `_footer()`) | Bottom-right, locked at `(9.3", 7.05")` |

**Action title is the only sanctioned title style for content slides.** The deprecated `add_navy_title_bar()` (dark navy band + white text) is forbidden for content; reserve it for explicit user requests on cover-style introduction slides only. Rule 5 enforces.

## Source attribution

Required on every content slide that displays data, claims, or external facts. Format:

```
Source: <origin>, <year/date>
```

Examples:

- `Source: internal analysis, Q1 2026`
- `Source: McKinsey Global Institute, 2024`
- `Source: company financials, FY2025`

The S3 content gate (`gate_check_content.py`) flags any non-cover, non-toc, non-divider, non-closing slide missing a non-empty `source` string.

## Page numbering

```python
def add_page_number(slide, num, total):
    add_text(slide, PAGE_NUM_LEFT, PAGE_NUM_TOP, PAGE_NUM_WIDTH, PAGE_NUM_HEIGHT,
             f"{num}/{total}", font_size=Pt(9), font_color=MED_GRAY,
             alignment=PP_ALIGN.RIGHT)
```

Position is locked per Rule 18 — never compute dynamically. Page-number drift across slides is the most visible "amateur deck" signal; the audience uses the page number as their anchor.

## Slide count guidelines

- **Standard deck:** 10–12 slides for a 60–90 min senior audience.
- **Short deck:** 6–8 slides for a 15–30 min update.
- **Decision-meeting deck:** 4–6 slides when one decision is being asked.
- **Minimum substantive deck:** 8 slides — anything less is rarely substantive enough to merit slides over a memo.
- **Time budget:** ~ 1 minute per slide as a planning heuristic. A 12-slide deck targets a 12-minute presentation, leaving room for Q&A in a 30-min slot.

## Engine path and import

```python
import sys, os
sys.path.insert(0, '/path/to/mbb-ppt-generator')      # the skill root that contains mck_ppt/
from mck_ppt import MckEngine as ExecEngine
```

The skill is self-contained — no external installation of the upstream Likaku skill is required. The bundled `mck_ppt/` package preserves Kaku Li's copyright headers per Apache 2.0.

`eng.save(outpath)` runs three-layer XML cleanup automatically:

1. Removes `p:style` references from every shape (theme-effect leak prevention).
2. Strips theme shadow / 3D effects from `theme*.xml`.
3. Repacks the OOXML zip with deterministic ordering.

Do not call `full_cleanup()` separately — `save()` already does it.

## File delivery

- **Local-only mode** (default): `eng.save()` writes the `.pptx` and exits.
- **Optional channel delivery** (off by default): a `deliver_to_channel()` helper exists for sending the file to a chat / messaging system. Disabled in the default security posture; enable only when the operator's confidentiality context allows.
