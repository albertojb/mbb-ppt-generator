# Brand Guide

> **Loaded at S1 (Brief).** Team-level constraints. Applies to every deck this skill produces — every brief begins by reading this file.
>
> Adapted to English from Likaku's `Mck-ppt-design-skill v2.3.3` `references/team/brand-guide.md`. Apache 2.0.

---

## Color palette — primary

| Name | Hex | RGB | Use |
|---|---|---|---|
| **NAVY** | `#051C2C` | `(5, 28, 44)` | Primary anchor: action titles, circles, TOC highlights, primary chart series |
| **WHITE** | `#FFFFFF` | `(255, 255, 255)` | Backgrounds, reverse text on navy |
| **BLACK** | `#000000` | `(0, 0, 0)` | Title separator lines, table header rules |
| **DARK_GRAY** | `#333333` | `(51, 51, 51)` | Body text, descriptions |
| **MED_GRAY** | `#666666` | `(102, 102, 102)` | Secondary text, source lines, axis labels |
| **LINE_GRAY** | `#CCCCCC` | `(204, 204, 204)` | Table row separators, chart gridlines |
| **BG_GRAY** | `#F2F2F2` | `(242, 242, 242)` | Insight panel backgrounds, takeaway areas |

**Key rule:** `NAVY` is the design anchor. Use it for every action title, every numbered circle, every TOC accent, every section divider. Consistency on this single color is what makes a deck look like one document instead of a stitched-together set.

## Color palette — accent

Use accents only when ≥ 3 parallel items need visual differentiation. Body text always remains `DARK_GRAY`. Card backgrounds always remain `BG_GRAY` or `WHITE`.

| Name | Hex | Paired light bg | Use |
|---|---|---|---|
| `ACCENT_BLUE` | `#006BA6` | `#E3F2FD` | First parallel item |
| `ACCENT_GREEN` | `#007A53` | `#E8F5E9` | Second parallel item |
| `ACCENT_ORANGE` | `#D46A00` | `#FFF3E0` | Third parallel item |
| `ACCENT_RED` | `#C62828` | `#FFEBEE` | Fourth parallel item / warning / negative movement |

The pairing helper `ACCENT_PAIRS` returns `[(accent, light_bg), …]` for easy iteration in `metric_cards`-style layouts.

## Color palette — additions (this skill)

| Name | Hex | Use |
|---|---|---|
| `HEADING_ACCENT` | `#051C2C` | Alias of `NAVY`, named for cover titles and large display text |
| `SECTION_BG` | `#F7F7F7` | Section divider backgrounds (lighter than `BG_GRAY`) |

## Color palette — warm (optional)

For decks where a warmer register is appropriate (heritage brands, philanthropic, hospitality). **Do not mix warm and primary accents on the same slide.** Use only when explicitly requested in the brief.

| Name | Hex | Use |
|---|---|---|
| `WARM_NAVY` | `#1A2E44` | Warm primary anchor (replaces `NAVY` deck-wide) |
| `WARM_GOLD` | `#B8860B` | Warm emphasis / accent |
| `WARM_STONE` | `#8B7355` | Warm neutral / supporting |

## Deprecated

`CYAN` (`#00A9F4`) is **deprecated** and not present in the constants module. Older decks may reference it; new content must not.

---

## Typography

```
Heading and big text: DM Sans (preferred), Inter (equivalent), Calibri (fallback)
Body text:            Arial
Source / footnote:    Arial 9pt
```

DM Sans is free under the SIL Open Font License via Google Fonts (<https://fonts.google.com/specimen/DM+Sans>). Install once on the generation host. PowerPoint falls back to Calibri automatically on viewer machines without DM Sans installed.

The previous heading font in upstream (Georgia, a transitional serif) has been replaced. Sans-paired-with-sans is consistent with modern executive presentation standards used at top-tier consulting firms.

## Type size hierarchy — strict

No other sizes are permitted unless a layout explicitly requires controlled shrinkage for overflow protection (Rule 13).

| Size | Type | Use |
|---|---|---|
| 44pt | Cover title | Cover slide only — heading font, navy, bold |
| 28pt | Section header | TOC titles, section dividers — heading font |
| 24pt | Cover subtitle | Cover slide |
| 22pt | Action title | All content slides — heading font, bold, black |
| 18pt | Sub-header | Column headers, in-slide section labels |
| 16pt | Emphasis text | Bottom-bar takeaways, bold |
| 14pt | Body text | **Primary size** — every body / detail / bullet |
| 12pt | Small text | Compact tables, dense KPI labels |
| 9pt | Footnote | Source attribution, page numbers — `MED_GRAY` only |

## Design philosophy

1. **Minimalism.** No shadows. No 3D effects. No gradients. No decorative color blocks. The default style is flat solid fill on every shape.
2. **Consistency.** Same kind of content, same font, same color, same size — every slide. Inconsistency is the most common amateur signal.
3. **Hierarchy.** 22pt action title → 18pt sub-header → 14pt body → 9pt footnote. Each level visibly distinct.
4. **Flat design.** Pure solid fills. The engine's `_clean_shape()` strips theme effects from every shape at construction time, and `full_cleanup()` strips them again at save time.
