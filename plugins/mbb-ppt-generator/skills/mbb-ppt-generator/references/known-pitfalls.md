# Known pitfalls

> One page of implicit constraints that the schema and cheatsheet do not capture in user-readable form. Read this before writing `content.json`. Every entry below is a real failure mode the gates have caught at S3 or S4.

## 1. The 3-char oval rule (only some layouts)

Several layouts render a small oval at the top-left of each item. The oval is a fixed 0.45" circle at 14pt — anything over 3 characters visually clips inside it.

**Layouts where the user supplies the oval value** (this is the rule to honor):

- `four_column.items[i][0]`        — `(num, col_title, desc)`
- `executive_summary.items[i][0]`  — `(num, item_title, desc)`
- `vertical_steps.steps[i][0]`     — `(label, step_title, desc)`
- `process_chevron.steps[i][0]`    — `(label, step_title, desc)`. Also: no `\n` allowed.
- `toc.items[i][0]`                — `(num, item_title, desc)`

**Layouts where the engine ignores user content for the oval** (no rule):

- `value_chain.stages` — engine renders `str(i + 1)`. The first slot is `stage_title` and is free-form.
- `numbered_list_panel.items` — engine renders `str(i + 1)`. The first slot is `item_title` and is free-form.

If you put `"Operating model"` in `value_chain.stages[0][0]`, that is the stage title — *not* the oval label. The S3 gate used to flag this incorrectly; v0.5.0 fixed it.

## 2. `cover.title` wrap behavior

The cover renders the title at 44pt across an 11" line. That fits **~28 effective characters before wrapping**. Longer titles wrap into 2 lines and may overflow the title box vertically. The matrix used to advertise 40 chars; treat 28 as the practical ceiling.

Cover supports `\n` if you want explicit two-line layout — that's the safe choice for ≥ 30-char titles.

## 3. Chart sub-title duplication (`grouped_bar`, `stacked_bar`)

Both chart layouts render the action title once at the top of the slide AND again at 13pt inside a 5"×0.3" box above the plot. With long action titles (≥ 38 chars), the inner sub-title wraps and pushes the chart down, triggering body-overflow at the render gate.

Workaround until this is fixed in the engine: keep `title` ≤ 30 chars on chart slides, or accept the auto-fix shrink at S4.

## 4. `executive_summary.desc` real budget is ~55, not 80

The matrix advertises 80-char `desc` for `executive_summary`. The geometry of the description box at 14pt only fits ~55 chars before wrapping into the separator below. The schema (api-schemas.yaml) uses 55. Don't push toward 80.

## 5. `harvey_ball_table` total-width discipline

Default columns are 2.8" + 2.5" per option. With 4+ options the table previously overflowed the 11.733" content area; v0.5.0 made the option column dynamic. If you supply explicit `first_col_w` / `opt_col_w`, make sure `first_col_w + n_options × opt_col_w ≤ CW` (= 11.733").

## 6. `timeline.milestones[-1][0]` ≤ 6 chars

Engine right-aligns the last milestone label. Anything longer than 6 chars overflows the canvas. Use `'2026'`, `'Q4 26'`, or similar.

## 7. `two_column_text` — at most one slide per deck

Two columns of unbroken prose is the most monotonous layout; the global S3 gate caps it at one occurrence per deck. Replace extras with `table_insight`, `four_column`, or `side_by_side`.

## 8. `executive_summary` cap — ≤ 15% of content slides

`executive_summary` is the most permissive layout (3-tuple items, free-form desc) so the model funnels everything into it. The global gate caps it at 15% of content slides (≥ 1 always allowed). Substitute by content shape:

- 3–4 numbered actions with rationale → `four_column` or `vertical_steps`
- One headline number + supporting detail → `big_number_callout` or `content_right_image`
- Numbered items + side panel → `numbered_list_panel`
- Two contrasting positions → `side_by_side` or `two_col_image_grid`
- Ranked findings → `horizontal_bar` or `table_insight`
- Closing decisions / asks → `executive_summary` is the right answer for the final ask slide

## 9. Visual-density floor scales with deck length

Decks ≥ 6 content slides need at least `max(2, N // 4)` chart/diagram/image layouts:

- 6 content slides → 2
- 12 → 3
- 20 → 5
- 30 → 7

The visual layouts that count are listed in `gate_check_content.py:VISUAL_LAYOUTS`. Card grids (`four_column`, `metric_cards`, `executive_summary`) do NOT count.

## 10. `three_stat.stats[i][2]` is a bool, not a string

Third tuple slot of each stat is `is_navy: bool`. Set exactly one stat's flag to `True` to highlight it; engine renders that stat in the primary color. This is undocumented in the cheatsheet's signature and frequently confused with a third text label.

## 11. `process_chevron.steps[i][0]` can't contain `\n`

A newline in the label overflows the oval and breaks the chevron geometry. Use a single short token like `'1990-2010'`, never `'1990\n2010'`.

## 12. `donut.segments` should sum to ~1.0

Engine doesn't normalize. If your percentages sum to 0.97, the donut will have a 3% wedge of background bleeding through.

## 13. Color slots accept three forms

Anything in the schema with `role: color` accepts:

- a named constant from `mbb_ppt.constants` (`PRIMARY`, `NAVY`, `ACCENT_BLUE`, …)
- a python-pptx `RGBColor` instance
- a `'#RRGGBB'` hex string (engine converts)

Don't pass an integer; the engine doesn't auto-convert from `0xRRGGBB`.

## 14. `harvey_ball_table.scores` is `int 0-4`

Score values map to fill levels:

- `0` → empty
- `1` → quarter
- `2` → half
- `3` → three-quarters
- `4` → full

Anything else clamps or renders as empty.

## 15. Why the S3 gate ever shows `label_too_long` errors

The gate enforces `max_chars` on tuple slots tagged `role: oval_label` in `api-schemas.yaml`. Char-budget violations on other slots are *not* hard-failed — they are budgets, not rules. If you see `label_too_long`, check that the value really is in slot 0 and not what you think is the title.
