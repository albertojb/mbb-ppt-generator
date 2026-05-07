# MBB PPT Generator — QA Checklist

> This checklist is the **visual layer** of QA. The **mechanical layer** is the two gate scripts (§ 0 below). The gate scripts are the source of truth for pass/fail. This checklist exists to catch things the gates cannot mechanically verify (branding text, source attribution wording, narrative quality).
>
> Every item below is binary: **PASS** or **FAIL**. The only acceptable non-binary value is **N/A**, and only for items where the layout-specific notes explicitly permit it.
>
> A deck with any FAIL must not be delivered to the audience until each FAIL is fixed and re-verified.

---

## 0. Gate scripts (run these first — they decide pass/fail)

The S3 and S4 gate scripts are mandatory before any human review. If either gate is `"passed": false`, do not even start the visual checklist — fix the gate failures and re-run.

| # | Gate | Command | PASS / FAIL |
|---|---|---|---|
| 0.1 | **S3 content gate** ran and `gate_content.json` exists | `python references/scripts/gate_check_content.py <content.json> <project_dir>` | ☐ |
| 0.2 | `gate_content.json` shows `"passed": true` | inspect file | ☐ |
| 0.3 | **S4 render gate** ran and `gate_render.json` exists | `python references/scripts/gate_check_render.py <pptx> <project_dir>` | ☐ |
| 0.4 | `gate_render.json` shows `"passed": true` | inspect file | ☐ |
| 0.5 | Any whitelisted `engine_bug_errors` in `gate_render.json` are documented in `ENGINE_BUG_WHITELIST` (verbal exemptions are forbidden) | inspect script | ☐ |

**If 0.2 or 0.4 fails, stop here and fix.** Do not proceed to the visual checklist.

---

## How to use the visual checklist

1. Confirm § 0 above passes.
2. Open the saved `.pptx` in PowerPoint (or LibreOffice Impress as a secondary check).
3. Walk through every slide and mark each item below for that slide.
4. Address every FAIL before delivering.
5. Spot-check 100% of slides for branding (item 9.1) and file integrity (item 10.x); other items can be sampled if the deck is large, but Cover, TOC, Executive Summary, and any chart slide must be checked at 100%.

---

## 1. Typography

| # | Check | PASS / FAIL |
|---|---|---|
| 1.1 | All headings render in `DM Sans`, `Inter`, or the explicit `Calibri` fallback. No serif fonts (Georgia, Times, Cambria, Garamond) appear in any heading. | ☐ |
| 1.2 | All body text renders in `Arial`. No serif fonts in body text. | ☐ |
| 1.3 | All source / footnote lines render in `Arial` at 9 pt. | ☐ |
| 1.4 | Font sizes match the size table: 44 pt (cover title), 28 pt (section), 24 pt (cover subtitle), 22 pt (action title), 18 pt (sub-header), 16 pt (emphasis), 14 pt (body), 12 pt (small), 9 pt (footnote). No other sizes unless documented as a controlled overflow shrink (Rule 13). | ☐ |
| 1.5 | Bold weight is reserved for titles, KPIs, and explicit emphasis. Body text is not bolded by default. | ☐ |

## 2. Overflow

| # | Check | PASS / FAIL |
|---|---|---|
| 2.1 | No text content visibly clips at the bottom of its container. | ☐ |
| 2.2 | No text content visibly clips at the right edge of its container. | ☐ |
| 2.3 | All text boxes containing wrapped text have a height ≥ `font_size × 1.4 × line_count + padding` (Rule 11). | ☐ |
| 2.4 | No `auto_size` text box has shrunk below 9 pt (Rule 13). | ☐ |
| 2.5 | No action title exceeds 120 characters or wraps onto more than two lines (Rule 14). | ☐ |
| 2.6 | No content extends outside the content boundary `(0.5", 1.1")` to `(9.5", 6.9")` (Rule 15). | ☐ |

## 3. Overlap

| # | Check | PASS / FAIL |
|---|---|---|
| 3.1 | No two text boxes occupy the same screen region. | ☐ |
| 3.2 | No two shapes occupy the same screen region unless one is a deliberate background fill (Rule 12). | ☐ |
| 3.3 | When background fills exist, they are sent to back; text and foreground shapes are brought to front (Rule 12). | ☐ |
| 3.4 | The insight bar / bottom bar does not visually intersect the last row of any table or chart (Rule 1, plus Slide content rule 2). | ☐ |
| 3.5 | Page number does not overlap any source line, insight bar, or content shape (Rule 18). | ☐ |

## 4. Title

| # | Check | PASS / FAIL |
|---|---|---|
| 4.1 | Every content slide (excluding Cover, Section Divider, Closing) has an action title. | ☐ |
| 4.2 | Every action title is conclusion-led — it states a finding, not a topic. (e.g. "Margin pressure is concentrated in two product lines", not "Margin analysis".) | ☐ |
| 4.3 | Every action title is under 120 characters. | ☐ |
| 4.4 | Every action title is followed by a 0.5 pt black title separator line, with at least 0.15" gap before the first content shape. | ☐ |
| 4.5 | Action title wraps to no more than two lines. | ☐ |
| 4.6 | Action titles use `HEADING_FONT` (DM Sans / Inter / Calibri), bold, 22 pt, color `BLACK`. | ☐ |

## 5. Spacing

| # | Check | PASS / FAIL |
|---|---|---|
| 5.1 | At least 0.15" of vertical space between the title separator line and the first content shape (Rule 1, slide content rule 1). | ☐ |
| 5.2 | At least 0.1" of vertical clear space between any two vertically adjacent content elements (Rule 16). | ☐ |
| 5.3 | At least 0.1" of inset on all four sides for text inside a filled shape (slide content rule 3). | ☐ |
| 5.4 | At least 0.6" reserved at the bottom of the content area for footnote / source lines before any insight bar begins (slide content rule 2). | ☐ |
| 5.5 | Insight bar and footnote area heights are ≥ 0.4" (Rule 17). | ☐ |
| 5.6 | No bottom-bar collision with content (Rule 1). | ☐ |
| 5.7 | Empty space between content and the bottom edge feels deliberate, not accidental (Rule 3). | ☐ |

## 6. Charts and legends

| # | Check | PASS / FAIL |
|---|---|---|
| 6.1 | Every chart legend uses colored swatch squares matching the plotted series color exactly (Rule 4). | ☐ |
| 6.2 | No legend uses monochrome glyphs, ASCII characters, or text-only series indicators. | ☐ |
| 6.3 | Donut, pie, and gauge charts use native `BLOCK_ARC` shapes — not stacks of small rectangles (Rule 9). | ☐ |
| 6.4 | Chart axis labels are centered on the full span of their axis, not at arbitrary offsets (Rule 6). | ☐ |
| 6.5 | All chart series use distinct colors from the approved palette (NAVY + accents). No two series share a color. | ☐ |
| 6.6 | Y-axis maximum is set explicitly when comparing across slides; bar heights are visually comparable. | ☐ |

## 7. Page numbers

| # | Check | PASS / FAIL |
|---|---|---|
| 7.1 | Every slide except the Cover has a page number. | ☐ |
| 7.2 | Page numbers follow the format `n/total` (e.g., `4/12`). | ☐ |
| 7.3 | Page numbers are placed at the locked position: left=9.3", top=7.05", width=0.5", height=0.25" (Rule 18). | ☐ |
| 7.4 | Page numbers render in `MED_GRAY` 9 pt, right-aligned. | ☐ |
| 7.5 | Page-number sequence is consecutive with no gaps or duplicates. | ☐ |

## 8. Source attribution

| # | Check | PASS / FAIL |
|---|---|---|
| 8.1 | Every data slide (charts, tables, KPIs, statistics) has a source line. | ☐ |
| 8.2 | Source lines render in 9 pt `Arial`, color `MED_GRAY`. | ☐ |
| 8.3 | Source lines are placed at the bottom-left of the content area (`y ≈ 7.05"`). | ☐ |
| 8.4 | Source text begins with `Source:` and identifies the data origin specifically (not "various sources" or "internal"). | ☐ |
| 8.5 | If a slide presents external benchmark data, the source is named with date or report year. | ☐ |

## 9. Branding

| # | Check | PASS / FAIL |
|---|---|---|
| 9.1 | No occurrence of "McKinsey", "McK", "Mck", or "mck" in any visible slide text — including titles, body, footnotes, source lines, image captions, and headers. (Use Find / `Ctrl+F` to verify.) | ☐ |
| 9.2 | No occurrence of "BCG", "Boston Consulting Group", "Bain", or other consulting-firm names in any visible slide text, unless the deck is explicitly about that firm. | ☐ |
| 9.3 | No client-identifying logo, photo, or trademark appears unless the deck is being delivered to that client and the asset is licensed for the use. | ☐ |
| 9.4 | Cover title, subtitle, author, and date are factually correct and free of placeholder strings ("TBD", "Lorem ipsum", "Sample"). | ☐ |
| 9.5 | No CJK characters (Chinese, Japanese, Korean) appear anywhere in the deck. | ☐ |

## 10. File integrity

| # | Check | PASS / FAIL |
|---|---|---|
| 10.1 | The `.pptx` opens in PowerPoint without a "Repair" or "Recover" prompt. | ☐ |
| 10.2 | The `.pptx` opens in LibreOffice Impress without rendering errors. | ☐ |
| 10.3 | File size is under 10 MB unless image-heavy by design. | ☐ |
| 10.4 | No theme shadow, gradient, reflection, or 3D effect appears on any shape (`full_cleanup()` verified). | ☐ |
| 10.5 | All shapes have `p:style` removed (no theme effect leaks). | ☐ |
| 10.6 | No `add_connector()` was used — all lines are thin rectangles via `add_hline()`. | ☐ |

## 11. Communication architecture

| # | Check | PASS / FAIL |
|---|---|---|
| 11.1 | A storyboard was produced *before* slide generation (numbered list of action titles). | ☐ |
| 11.2 | Reading the action titles in order, the deck functions as a 90-second spoken briefing. | ☐ |
| 11.3 | Slide 3 (or the first content slide after Cover and TOC) leads with the answer / recommendation, not background. | ☐ |
| 11.4 | The deck has at least 8 slides for any substantive topic. | ☐ |
| 11.5 | Each major section answers an explicit audience question. | ☐ |
| 11.6 | Slides 2–5 use insight-led layouts (`table_insight`, `executive_summary`, `big_number`, `key_takeaway`) rather than plain text. | ☐ |
| 11.7 | The deck contains a clear recommendation, decision, or call-to-action by the final content slide. | ☐ |
| 11.8 | Layout diversity rule: no two adjacent content slides use the same layout method without a clear analytical reason. | ☐ |
| 11.9 | At least one visual-relief slide (image or image placeholder) is present in any deck of 8+ slides (Rule 7). | ☐ |

## 12. Security and privacy (only if outbound integrations were used)

> Mark **N/A** for the entire section if the deck was generated in local-only mode.

| # | Check | PASS / FAIL / N/A |
|---|---|---|
| 12.1 | Every outbound API call was explicitly enabled in configuration. | ☐ |
| 12.2 | No client-identifying information was sent to a cloud image-generation prompt. | ☐ |
| 12.3 | No `.pptx` was sent to a chat or messaging channel without the user's explicit permission. | ☐ |
| 12.4 | No deck content, notes, or metadata was uploaded to a third-party service. | ☐ |

---

## Sign-off

| Field | Value |
|---|---|
| Deck filename |  |
| Slide count |  |
| QA reviewer |  |
| Review date |  |
| Gate scripts run? (§ 0) | ☐ both passed / ☐ failed |
| Total FAILs (visual checklist) |  |
| Status (Approved / Hold) |  |

**A deck is "Approved for delivery" only when every applicable item is PASS, including § 0 gate scripts.** Any FAIL → Hold → fix → re-run the gate scripts and the visual checklist for changed slides.

---

## Self-Refinement after delivery

If any failure was a **pattern-level issue** (likely to recur in future decks), append an `Experience NNN` entry to the matching file:

- Overflow / character budget → `experiences/overflow.md`
- Layout-specific trap → `experiences/layout-pitfalls.md`
- Chart capacity issue → `experiences/chart-limits.md`

If the rule is mechanizable, also propose a check to add to `gate_check_content.py` or `gate_check_render.py`. The gate scripts are how this skill gets stronger over time — a missed defect today should be a blocked defect tomorrow.
