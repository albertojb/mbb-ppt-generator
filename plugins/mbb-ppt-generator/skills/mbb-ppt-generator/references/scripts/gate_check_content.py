#!/usr/bin/env python3
# Copyright 2024-2026 Kaku Li (https://github.com/likaku) — original Mck-ppt-design-skill, Apache 2.0.
# Adapted for MBB PPT Generator. English-language messages.
# Apache 2.0.
"""
gate_check_content.py — S3 content gate (machine-readable).

Usage:
    python gate_check_content.py <content_json_path> <project_dir>

Output:
    <project_dir>/gate_content.json

JSON structure:
{
    "passed": true|false,            # program-derived; do NOT verbally claim pass
    "total_slides": N,
    "verdict": "PASS — proceed to S4" | "FAIL — fix N items and re-run",
    "fail_items": [
        {"slide_idx": 6, "layout": "four_column",
         "check": "api_format",
         "message": "four_column items[0] must be a 3-tuple (num, title, desc); got 2 elements"}
    ],
    "pass_items": [...]
}

Checks:
    1. API format — items / steps / segments / quadrants tuple arity
    2. Count limits — donut ≤ 6, process_chevron ≤ 5, grouped_bar ≤ 6×3, four_column ≤ 4
    3. Layout-specific constraints — process_chevron label \\n, timeline last label ≤ 6
    4. Source attribution — every content slide has non-empty `source`
    5. Action title — > 10 characters and ≤ 120 characters
    6. two_column_text — at most one slide per deck (global)
    7. Visual density — decks with ≥ 6 content slides need ≥ 2 chart/diagram/image
       layouts; pure text-column decks fail (global)
"""

from __future__ import annotations
import sys
import os
import json
from pathlib import Path
from typing import List, Dict, Any


# ── Skip layouts that don't need source / action title ────────────────────
LAYOUTS_WITHOUT_SOURCE = {
    "cover", "toc", "section_divider", "closing", "appendix_title",
}
LAYOUTS_WITHOUT_ACTION_TITLE = LAYOUTS_WITHOUT_SOURCE

# ── Oval-bound label budget ───────────────────────────────────────────────
# add_oval() in mbb_ppt/core.py renders text inside a fixed 0.45" circle at
# 14pt. Anything over 3 characters visually clips. Layouts that pass user
# data into the oval-label slot must enforce this budget at S3 — otherwise
# the user sees fragmented text in the rendered .pptx.
MAX_OVAL_LABEL_CHARS = 3


def _check_oval_label(slide: Dict, idx: int, layout: str,
                      collection_key: str, label_slot: int = 0) -> List[Dict]:
    """Validate that the first tuple element of each item fits the oval.

    Args:
        slide: the slide dict from content.json
        idx: 1-based slide index for error messages
        layout: layout name for error messages
        collection_key: name of the items list field (e.g. "steps", "items")
        label_slot: which tuple position holds the oval label (default 0)
    """
    issues: List[Dict] = []
    items = slide.get(collection_key, [])
    for i, item in enumerate(items):
        if not isinstance(item, (list, tuple)) or len(item) <= label_slot:
            continue
        label = item[label_slot]
        try:
            label_str = str(label)
        except Exception:
            continue
        if len(label_str) > MAX_OVAL_LABEL_CHARS:
            issues.append({
                "slide_idx": idx, "layout": layout, "check": "label_too_long",
                "message": (
                    f"{layout} {collection_key}[{i}] label {label_str!r} is "
                    f"{len(label_str)} chars > {MAX_OVAL_LABEL_CHARS}; the engine "
                    f"renders this inside a 0.45\" oval and will visually clip. "
                    f"Use a number ('1','2','3'), letter, or 2–3-char code. "
                    f"Move long text into the next tuple slot (the title)."
                ),
            })
    return issues


# ── Per-layout checkers ───────────────────────────────────────────────────

def check_four_column(slide: Dict, idx: int) -> List[Dict]:
    """four_column items must be 3-tuples (num, col_title, desc); max 4 columns."""
    issues = []
    items = slide.get("items", [])
    if len(items) > 4:
        issues.append({
            "slide_idx": idx, "layout": "four_column", "check": "count",
            "message": f"four_column max 4 columns; got {len(items)}. Fix: split or merge.",
        })
    for i, item in enumerate(items):
        if not isinstance(item, (list, tuple)) or len(item) != 3:
            got = len(item) if isinstance(item, (list, tuple)) else "non-list"
            issues.append({
                "slide_idx": idx, "layout": "four_column", "check": "api_format",
                "message": (f"four_column items[{i}] must be a 3-tuple (num, col_title, desc); "
                            f"got {got} elements. Fix: prepend a number, e.g. ('1', 'Title', 'Description')."),
            })
    issues += _check_oval_label(slide, idx, "four_column", "items")
    return issues


def check_executive_summary(slide: Dict, idx: int) -> List[Dict]:
    """executive_summary items must be 3-tuples (num, item_title, desc); max 4 items."""
    issues = []
    items = slide.get("items", [])
    if len(items) > 4:
        issues.append({
            "slide_idx": idx, "layout": "executive_summary", "check": "count",
            "message": f"executive_summary max 4 items; got {len(items)}.",
        })
    for i, item in enumerate(items):
        if not isinstance(item, (list, tuple)) or len(item) != 3:
            got = len(item) if isinstance(item, (list, tuple)) else "non-list"
            issues.append({
                "slide_idx": idx, "layout": "executive_summary", "check": "api_format",
                "message": (f"executive_summary items[{i}] must be a 3-tuple "
                            f"(num, item_title, desc); got {got}. Fix: ('1', 'Action', 'Why').") ,
            })
    issues += _check_oval_label(slide, idx, "executive_summary", "items")
    return issues


def check_vertical_steps(slide: Dict, idx: int) -> List[Dict]:
    """vertical_steps: 3-tuples (label, title, desc). Label goes in an oval."""
    issues = []
    steps = slide.get("steps", [])
    for i, step in enumerate(steps):
        if not isinstance(step, (list, tuple)) or len(step) < 3:
            issues.append({
                "slide_idx": idx, "layout": "vertical_steps", "check": "api_format",
                "message": f"vertical_steps steps[{i}] must be a 3-tuple (label, title, desc).",
            })
    issues += _check_oval_label(slide, idx, "vertical_steps", "steps")
    return issues


def check_value_chain(slide: Dict, idx: int) -> List[Dict]:
    """value_chain: stages with a label that goes in the small panel header."""
    issues = []
    stages = slide.get("stages", [])
    issues += _check_oval_label(slide, idx, "value_chain", "stages")
    return issues


def check_numbered_list_panel(slide: Dict, idx: int) -> List[Dict]:
    """numbered_list_panel: items[0] is the oval-bound number."""
    return _check_oval_label(slide, idx, "numbered_list_panel", "items")


def check_toc(slide: Dict, idx: int) -> List[Dict]:
    """toc: items are (num, title, desc); num goes in oval."""
    return _check_oval_label(slide, idx, "toc", "items")


def check_matrix_2x2(slide: Dict, idx: int) -> List[Dict]:
    """matrix_2x2 quadrants must be 3-tuples (label, bg_color, desc); exactly 4."""
    issues = []
    quadrants = slide.get("quadrants", [])
    if len(quadrants) != 4:
        issues.append({
            "slide_idx": idx, "layout": "matrix_2x2", "check": "count",
            "message": f"matrix_2x2 requires exactly 4 quadrants; got {len(quadrants)}.",
        })
    for i, q in enumerate(quadrants):
        if not isinstance(q, (list, tuple)) or len(q) != 3:
            issues.append({
                "slide_idx": idx, "layout": "matrix_2x2", "check": "api_format",
                "message": (f"matrix_2x2 quadrants[{i}] must be a 3-tuple "
                            f"(label, bg_color, desc); got {q!r}."),
            })
    return issues


def check_process_chevron(slide: Dict, idx: int) -> List[Dict]:
    """process_chevron: ≤ 5 steps, label has no \\n, desc ≤ 50 chars."""
    issues = []
    steps = slide.get("steps", [])
    if len(steps) > 5:
        issues.append({
            "slide_idx": idx, "layout": "process_chevron", "check": "count",
            "message": (f"process_chevron max 5 steps; got {len(steps)}. "
                        "Fix: merge or split across slides."),
        })
    for i, step in enumerate(steps):
        if not isinstance(step, (list, tuple)) or len(step) < 3:
            issues.append({
                "slide_idx": idx, "layout": "process_chevron", "check": "api_format",
                "message": f"process_chevron steps[{i}] must be a 3-tuple (label, title, desc).",
            })
            continue
        label, _title, desc = step[0], step[1], step[2]
        if "\n" in str(label):
            issues.append({
                "slide_idx": idx, "layout": "process_chevron", "check": "label_newline",
                "message": (f"process_chevron steps[{i}] label cannot contain '\\n'. "
                            f"Got: {label!r}. Fix: single-line label like '1990-2010'."),
            })
        if len(str(desc)) > 50:
            issues.append({
                "slide_idx": idx, "layout": "process_chevron", "check": "desc_length",
                "message": (f"process_chevron steps[{i}] desc {len(str(desc))} chars > 50. "
                            f"Preview: {str(desc)[:40]!r}"),
            })
    issues += _check_oval_label(slide, idx, "process_chevron", "steps")
    return issues


def check_donut(slide: Dict, idx: int) -> List[Dict]:
    """donut max 6 segments."""
    issues = []
    segments = slide.get("segments", [])
    if len(segments) > 6:
        issues.append({
            "slide_idx": idx, "layout": "donut", "check": "count",
            "message": (f"donut max 6 segments; got {len(segments)}. "
                        "Fix: keep top-5 and merge the rest into 'Other'."),
        })
    return issues


def check_grouped_bar(slide: Dict, idx: int) -> List[Dict]:
    """grouped_bar: ≤ 6 categories × ≤ 3 series."""
    issues = []
    cats = slide.get("categories", [])
    series = slide.get("series", [])
    if len(cats) > 6:
        issues.append({
            "slide_idx": idx, "layout": "grouped_bar", "check": "count",
            "message": f"grouped_bar max 6 categories; got {len(cats)}.",
        })
    if len(series) > 3:
        issues.append({
            "slide_idx": idx, "layout": "grouped_bar", "check": "count",
            "message": f"grouped_bar max 3 series; got {len(series)}.",
        })
    return issues


def check_timeline_last_label(slide: Dict, idx: int) -> List[Dict]:
    """timeline: last milestone label ≤ 6 chars (engine pins it right)."""
    issues = []
    milestones = slide.get("milestones", [])
    if milestones:
        last = milestones[-1]
        if isinstance(last, (list, tuple)) and last:
            label = str(last[0])
            if len(label) > 6:
                issues.append({
                    "slide_idx": idx, "layout": "timeline", "check": "last_label_length",
                    "message": (f"timeline last milestone label {label!r} is "
                                f"{len(label)} chars > 6; will overflow right edge. "
                                "Fix: shorten to something like '2026' or 'Q4'."),
                })
    return issues


def check_source(slide: Dict, idx: int) -> List[Dict]:
    """Every content slide has a non-empty source string."""
    layout = slide.get("layout", "")
    if layout in LAYOUTS_WITHOUT_SOURCE:
        return []
    source = slide.get("source", "")
    if not source or not str(source).strip():
        return [{
            "slide_idx": idx, "layout": layout, "check": "source_missing",
            "message": f"slide {idx} ({layout}) has no source line; required on every content slide.",
        }]
    return []


def check_action_title(slide: Dict, idx: int) -> List[Dict]:
    """Action title is a complete clause: > 10 chars and ≤ 120 chars."""
    layout = slide.get("layout", "")
    if layout in LAYOUTS_WITHOUT_ACTION_TITLE:
        return []
    title = str(slide.get("title", ""))
    issues = []
    if len(title) <= 10:
        issues.append({
            "slide_idx": idx, "layout": layout, "check": "title_too_short",
            "message": (f"slide {idx} title {title!r} is too short (≤ 10 chars). "
                        "Action titles must be conclusion-led clauses, e.g. "
                        "'Margin pressure is concentrated in two product lines'."),
        })
    if len(title) > 120:
        issues.append({
            "slide_idx": idx, "layout": layout, "check": "title_too_long",
            "message": (f"slide {idx} title is {len(title)} chars > 120. "
                        "Will wrap and collide with body. Trim or split."),
        })
    return issues


def check_two_column_text_global(slides: List[Dict]) -> List[Dict]:
    """At most one two_column_text slide per deck."""
    count = sum(1 for s in slides if s.get("layout") == "two_column_text")
    if count > 1:
        return [{
            "slide_idx": "(global)", "layout": "two_column_text", "check": "global_max",
            "message": (f"two_column_text used {count} times; max 1 per deck. "
                        "Replace extras with table_insight, four_column, or side_by_side."),
        }]
    return []


# ── Visual-density gate ──────────────────────────────────────────────────
# Layouts that produce a chart, diagram, image, or dashboard. A deck without
# at least two of these in 6+ content slides reads as a wall of text columns
# regardless of how good the writing is.

VISUAL_LAYOUTS = {
    # Charts
    "grouped_bar", "stacked_bar", "horizontal_bar", "line_chart", "waterfall",
    "pareto", "stacked_area", "donut", "bubble", "kpi_tracker", "multi_bar_panel",
    "pie",  # retired but still visual
    # Frameworks / diagrams
    "matrix_2x2", "swot", "temple", "pyramid", "stakeholder_map", "risk_matrix",
    "decision_tree", "harvey_ball_table", "venn",  # venn retired
    # Images
    "content_right_image", "three_images", "image_four_points", "full_width_image",
    "case_study_image", "two_col_image_grid", "goals_illustration", "quote_bg_image",
    "case_study",  # case_study includes image placeholder by default
    # Dashboards
    "dashboard_kpi_chart", "dashboard_table_chart",
    # Process / flow visuals (visually distinct from text columns)
    "process_chevron", "timeline", "value_chain", "cycle",  # cycle retired
}

# Boilerplate slides excluded from the content-slide count for density purposes.
BOILERPLATE_LAYOUTS = {"cover", "toc", "section_divider", "closing", "appendix_title"}

VISUAL_DENSITY_THRESHOLD_SLIDES = 6   # ≥ 6 content slides triggers the rule
VISUAL_DENSITY_MIN_VISUAL = 2         # ≥ 2 visual slides required


def check_visual_density_global(slides: List[Dict]) -> List[Dict]:
    """Reject decks ≥ 6 content slides that contain < 2 visual layouts.

    Rationale: the most common output failure of MBB-style skills is a deck
    that is well-written but visually monotonous — every slide is a text
    column or a card grid. A hard floor of 2 chart/diagram/image layouts in
    a 6+ slide deck is the simplest mechanism that rules out that failure.
    """
    content_slides = [
        s for s in slides
        if s.get("layout") not in BOILERPLATE_LAYOUTS
    ]
    if len(content_slides) < VISUAL_DENSITY_THRESHOLD_SLIDES:
        return []
    visual_count = sum(
        1 for s in content_slides if s.get("layout") in VISUAL_LAYOUTS
    )
    if visual_count >= VISUAL_DENSITY_MIN_VISUAL:
        return []
    return [{
        "slide_idx": "(global)",
        "layout": "(deck-level)",
        "check": "visual_density",
        "message": (
            f"Visual-density floor: deck has {len(content_slides)} content slides "
            f"but only {visual_count} visual (chart/diagram/image) layout(s); "
            f"≥ {VISUAL_DENSITY_MIN_VISUAL} required. "
            "Pick at least one chart (grouped_bar / line_chart / donut / pareto / "
            "horizontal_bar / waterfall) and at least one framework or image layout "
            "(matrix_2x2 / swot / risk_matrix / harvey_ball_table / case_study_image / "
            "process_chevron / timeline / dashboard_kpi_chart). See "
            "references/framework/planning-guide.md § 'Layout selection by task'."
        ),
    }]


# ── Routing ───────────────────────────────────────────────────────────────

LAYOUT_CHECKERS = {
    "four_column":         [check_four_column,         check_source, check_action_title],
    "executive_summary":   [check_executive_summary,   check_source, check_action_title],
    "matrix_2x2":          [check_matrix_2x2,          check_source, check_action_title],
    "process_chevron":     [check_process_chevron,     check_source, check_action_title],
    "donut":               [check_donut,               check_source, check_action_title],
    "grouped_bar":         [check_grouped_bar,         check_source, check_action_title],
    "timeline":            [check_timeline_last_label, check_source, check_action_title],
    "vertical_steps":      [check_vertical_steps,      check_source, check_action_title],
    "value_chain":         [check_value_chain,         check_source, check_action_title],
    "numbered_list_panel": [check_numbered_list_panel, check_source, check_action_title],
    "toc":                 [check_toc],  # toc skips source/action_title (boilerplate)
}
DEFAULT_CHECKERS = [check_source, check_action_title]


def run_gate(content_json_path: str, project_dir: str) -> Dict[str, Any]:
    if not os.path.exists(content_json_path):
        return {
            "passed": False,
            "verdict": f"FAIL — {content_json_path} does not exist",
            "fail_items": [{"check": "file_missing", "message": f"not found: {content_json_path}"}],
            "pass_items": [],
        }

    with open(content_json_path, "r", encoding="utf-8") as f:
        try:
            content = json.load(f)
        except json.JSONDecodeError as e:
            return {
                "passed": False,
                "verdict": "FAIL — content.json failed to parse",
                "fail_items": [{"check": "json_parse", "message": str(e)}],
                "pass_items": [],
            }

    slides = content.get("slides", [])
    all_issues: List[Dict] = []
    passed_items: List[Dict] = []

    for slide in slides:
        idx = slide.get("idx", "?")
        layout = slide.get("layout", "unknown")
        checkers = LAYOUT_CHECKERS.get(layout, DEFAULT_CHECKERS)
        slide_issues: List[Dict] = []
        for fn in checkers:
            slide_issues.extend(fn(slide, idx))
        if slide_issues:
            all_issues.extend(slide_issues)
        else:
            passed_items.append({"slide_idx": idx, "layout": layout, "status": "ok"})

    all_issues.extend(check_two_column_text_global(slides))
    all_issues.extend(check_visual_density_global(slides))

    passed = len(all_issues) == 0
    return {
        "passed": passed,
        "total_slides": len(slides),
        "verdict": ("PASS — proceed to S4" if passed
                    else f"FAIL — fix {len(all_issues)} items and re-run"),
        "fail_items": all_issues,
        "pass_items": passed_items,
    }


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: gate_check_content.py <content.json> <project_dir>")
        return 2
    content_path = sys.argv[1]
    project_dir = sys.argv[2]
    Path(project_dir).mkdir(parents=True, exist_ok=True)
    out = os.path.join(project_dir, "gate_content.json")

    print(f"[gate_content] checking: {content_path}")
    result = run_gate(content_path, project_dir)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[gate_content] slides: {result.get('total_slides', '?')}")
    print(f"[gate_content] fail items: {len(result.get('fail_items', []))}")
    print(f"[gate_content] verdict: {result.get('verdict', '')}")
    print(f"[gate_content] result written to: {out}")

    if result.get("fail_items"):
        print("\n[gate_content] items to fix:")
        for item in result["fail_items"]:
            print(f"  slide {item.get('slide_idx')} [{item.get('layout', '-')}] "
                  f"[{item.get('check')}]: {item.get('message', '')[:120]}")

    return 0 if result.get("passed") else 1


if __name__ == "__main__":
    sys.exit(main())
