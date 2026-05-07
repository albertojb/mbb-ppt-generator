# Production Guard Rails

> **Loaded at S3 (Content) and re-checked at S4 (Render).** Eighteen rules drawn from real-world defects. The render gate (`gate_check_render.py`) enforces most of these mechanically; the content gate (`gate_check_content.py`) enforces the rest at S3.
>
> Rules 1–10 originate in the upstream skill ([Likaku, `Mck-ppt-design-skill v1.9 / v2.0`](https://github.com/likaku/Mck-ppt-design-skill)). Rules 11–18 were added in this adaptation to harden the model against text overflow, z-order bugs, and inconsistent page-number placement.

---

## How to read this file

Every rule has a **statement**, an **enforcement** column, and (where useful) a **code pattern**. The enforcement column tells you *who* checks it: the model (you), the content gate (S3), or the render gate (S4).

If a rule is "code" enforced, the engine method already implements it — call the method correctly and the rule is satisfied. If a rule is "gate" enforced, the gate will fail your `passed` flag if you violate it. If a rule says "model", it is on the operator to comply because the gate cannot detect the violation.

---

## Rule 1 — Bottom-bar spacing

**Statement:** Maintain ≥ `0.15"` between the last content block and any bottom summary bar.

**Enforcement:** S4 render gate (overlap and dead-whitespace checks).

**Code pattern (engine internal):**

```python
bar_y = max(last_row_bottom + Inches(0.2), Inches(6.1))
bar_y = min(bar_y, Inches(6.4))
```

The engine uses dynamic computation in tables and lists; manual layout code must do the same.

---

## Rule 2 — Overflow protection

**Statement:** Every shape, text box, and chart stays inside the content boundary defined in Rule 15. Text inside a filled box must be inset (Rule 11), never edge-to-edge.

**Enforcement:** S4 render gate (out-of-bounds detection).

---

## Rule 3 — Bottom whitespace control

**Statement:** Empty space between the last content row and the bottom edge must feel deliberate. The render gate flags > 55% empty content area as a `whitespace` warning.

**Enforcement:** S4 render gate (whitespace check).

**Fix when triggered:** add an insight bar, increase row heights with dynamic sizing (Rule 8), or split the slide and add a real second one — do not simply pad with empty bullet points.

---

## Rule 4 — Legend color consistency

**Statement:** Chart legends must use colored swatch squares matching the plotted series exactly. Do not fake legends with monochrome glyphs (`■`, `●`) or text-only series indicators.

**Enforcement:** code (engine `add_color_legend()` + render gate).

**Code pattern:**

```python
from mck_ppt.core import add_color_legend
add_color_legend(slide,
    items=[('Premium', NAVY), ('Partner', ACCENT_BLUE)],
    x=Inches(7.5), y=Inches(6.5))
```

---

## Rule 5 — Title style consistency

**Statement:** `add_action_title()` is the default and only sanctioned title pattern for content slides. Reserve alternate title bars (e.g., `add_navy_title_bar`) for explicit user requests.

**Enforcement:** code (default in every layout method).

---

## Rule 6 — Axis label centering

**Statement:** In matrix and grid charts (`matrix_2x2`, `risk_matrix`, `swot`), axis labels are centered on the full span of their axis, not at arbitrary offsets.

**Enforcement:** code (default in matrix layout methods) + S4 render gate.

---

## Rule 7 — Visual-relief slide

**Statement:** Decks of ≥ 8 slides include at least one image-containing or image-placeholder slide to break up walls of text and charts.

**Enforcement:** S3 content gate (deck-level check) — recommended; warning, not block.

**Suggested layouts:** `content_right_image`, `case_study_image`, `quote_bg_image`, `full_width_image`.

---

## Rule 8 — Dynamic sizing for variable counts

**Statement:** Whenever the number of rows, stages, or parallel cards varies, compute dimensions dynamically. Never use fixed widths/heights for variable content.

**Enforcement:** code (engine internals).

**Code pattern:**

```python
# Horizontal: divide the content width across N items minus the gaps
gap = Inches(0.15)
item_w = (CW - gap * (N - 1)) / N

# Vertical: cap at a max but shrink to fit available height
row_h = min(Inches(0.85), available_h / n_rows)
```

When you write custom layout code outside the engine, use this exact pattern.

---

## Rule 9 — `BLOCK_ARC` for circular charts

**Statement:** Circular charts (`donut`, retired `pie`, retired `gauge`) use native PowerPoint `BLOCK_ARC` shapes. Do not simulate arcs with hundreds of small rectangles.

**Enforcement:** code (engine `add_block_arc()`).

**Why this rule exists:** the older approach used 2,000+ rectangles per chart. File size ballooned, generation took 30s–2min, and rendering quality was jagged. `BLOCK_ARC` produces 3–4 shapes per chart and renders crisply.

---

## Rule 10 — Horizontal overflow protection

**Statement:** For horizontal item layouts (`process_chevron`, `value_chain`, `four_column`, etc.), compute item widths dynamically so gaps never become negative and shapes never acquire invalid dimensions.

**Enforcement:** code (engine internals).

**Anti-pattern:** hardcoded `stage_w = Inches(2.0)` — leaves whitespace at low counts and causes negative gaps at high counts. Use the formula in Rule 8.

---

## Rule 11 — Minimum text-box height (v2.0)

**Statement:** Every text box must have a minimum height of:

```
height ≥ font_size × 1.4 × expected_line_count + top_pad + bottom_pad
```

Never assume single-line content unless you've explicitly capped the content to one line and truncated overflow.

**Enforcement:** S4 render gate (text-overflow detection compares text height against box height).

**Constant:** `TEXTBOX_LINE_HEIGHT_FACTOR = 1.4` in `constants.py`.

**Why:** wrapping doubles the rendered height while the box height stays fixed. The text disappears off the bottom edge, often invisibly when the slide is reviewed in PowerPoint at 100% zoom.

---

## Rule 12 — Z-order discipline (v2.0)

**Statement:** When multiple shapes occupy the same region, document intended z-order in the engine method. Background fills must be sent to back; text boxes must be brought to front. Verify at save time.

**Enforcement:** code (shape-add order is z-order in `python-pptx`; engine methods add background fills before text).

**Code pattern:**

```python
# Background (back of stack)
add_rect(slide, x, y, w, h, BG_GRAY)
# Text (front)
add_text(slide, x + Inches(0.2), y + Inches(0.1), w, h, "Insight…")
```

---

## Rule 13 — Dynamic font shrink guard (v2.0)

**Statement:** If `auto_size` is enabled on a text box, set a minimum font-size floor of `9pt`. Disable `auto_size` entirely on title text boxes — enforce a character limit (Rule 14) and truncate with an ellipsis instead.

**Enforcement:** code (default in `add_text()` and `add_action_title()`).

**Constant:** `AUTO_SIZE_FONT_FLOOR = Pt(9)` in `constants.py`.

**Why:** uncapped auto-shrink can render titles at 6pt before bailing. The deck looks fine in the editor but is illegible when projected.

---

## Rule 14 — Title character limit (v2.0)

**Statement:** Action titles must not exceed **120 characters**. If a generated title is longer, the engine must trim it and log a warning. This prevents wrap collisions with the body area.

**Enforcement:** S3 content gate (`check_action_title`) + code (engine warning).

**Constant:** `ACTION_TITLE_MAX_CHARS = 120` in `constants.py`.

**Practical guideline:** aim for ≤ 80 chars for visual safety. The 120-char hard limit is a backstop, not a target.

---

## Rule 15 — Content area boundary (v2.0)

**Statement:** Define a hard content boundary:

```
CONTENT_LEFT        = Inches(0.5)
CONTENT_TOP_BOUND   = Inches(1.1)
CONTENT_RIGHT       = Inches(9.5)
CONTENT_BOTTOM      = Inches(6.9)
```

No shape, text box, or chart may be placed outside these coordinates. The engine validates this at slide-generation time, not only at save time.

**Enforcement:** S4 render gate (`_check_body_overflow`).

**Note:** the legacy `LM` / `RM` margins (0.8" each) define the inner *typographic* margin used by most layout methods. Rule 15 defines the *outer* envelope. They coexist — a shape can use `LM` at 0.8" and still satisfy Rule 15 because 0.8" > 0.5".

---

## Rule 16 — Inter-element gap minimum (v2.0)

**Statement:** Two vertically adjacent content elements must have ≥ `0.1"` of clear space between them. Compute programmatically; do not estimate visually.

**Enforcement:** S4 render gate (overlap-tolerance check).

**Constant:** `INTER_ELEMENT_GAP_MIN = Inches(0.1)` in `constants.py`.

---

## Rule 17 — Insight bar height floor (v2.0)

**Statement:** Insight bars and footnote areas must have a minimum height of `0.4"`. Do not compress them below this regardless of available space.

**Enforcement:** code (engine sets `BOTTOM_BAR_H = Inches(0.65)` by default; never override below the floor).

**Constant:** `INSIGHT_BAR_HEIGHT_MIN = Inches(0.4)` in `constants.py`.

---

## Rule 18 — Page number placement lock (v2.0)

**Statement:** Page numbers are placed at a fixed position:

```
left   = Inches(9.3)
top    = Inches(7.05)
width  = Inches(0.5)
height = Inches(0.25)
```

Never compute page-number position dynamically. Lock it.

**Enforcement:** code (engine `add_page_number()` reads `PAGE_NUM_LEFT` / `PAGE_NUM_TOP` from constants).

**Why locked:** drift in page-number position between slides is the most visible "amateur deck" tell. Page numbers are the audience's anchor; they must not move.

---

## Rules summary table

| # | Rule | Enforced by | Constant in `constants.py` |
|---|---|---|---|
| 1 | Bottom-bar spacing ≥ 0.15" | render gate | — |
| 2 | Stay inside Rule 15 boundary | render gate | (see Rule 15) |
| 3 | Bottom whitespace ≤ 55% | render gate (warning) | — |
| 4 | Colored legend swatches | code | — |
| 5 | `add_action_title()` for content | code | — |
| 6 | Axis labels centered | code + render gate | — |
| 7 | ≥ 1 visual-relief slide in 8+ decks | content gate (warning) | — |
| 8 | Dynamic sizing for variable counts | code | — |
| 9 | BLOCK_ARC for circular charts | code | — |
| 10 | Horizontal layout dynamic widths | code | — |
| 11 | Min textbox height = font × 1.4 × lines | render gate | `TEXTBOX_LINE_HEIGHT_FACTOR` |
| 12 | Z-order: bg back, text front | code | — |
| 13 | `auto_size` floor 9pt; disabled on titles | code | `AUTO_SIZE_FONT_FLOOR` |
| 14 | Action title ≤ 120 chars | content gate + code | `ACTION_TITLE_MAX_CHARS` |
| 15 | Content boundary (0.5,1.1)–(9.5,6.9) | render gate | `CONTENT_LEFT`, `CONTENT_TOP_BOUND`, `CONTENT_RIGHT`, `CONTENT_BOTTOM` |
| 16 | Inter-element gap ≥ 0.1" | render gate | `INTER_ELEMENT_GAP_MIN` |
| 17 | Insight bar height ≥ 0.4" | code | `INSIGHT_BAR_HEIGHT_MIN` |
| 18 | Page number locked (9.3, 7.05, 0.5×0.25) | code | `PAGE_NUM_LEFT`, `PAGE_NUM_TOP`, `PAGE_NUM_WIDTH`, `PAGE_NUM_HEIGHT` |

---

## Cross-references

- **Capacity limits per layout** (max items, char_budget): [`../layout-matrix.yaml`](../layout-matrix.yaml).
- **Anti-patterns and historic defects:** [`../../experiences/`](../../experiences/) — read at S3 before writing content.
- **Gate scripts:** [`../scripts/gate_check_content.py`](../scripts/gate_check_content.py) (S3), [`../scripts/gate_check_render.py`](../scripts/gate_check_render.py) (S4).
- **Engine source (authoritative):** `../../mck_ppt/engine.py`, `../../mck_ppt/core.py`.
