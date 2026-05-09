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
    7. executive_summary cap — ≤ 15% of content slides (global)
    8. Visual density — decks with ≥ 6 content slides need
       max(2, N // 4) chart/diagram/image layouts (global)
"""

from __future__ import annotations
import sys
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover — yaml is a hard dep of the engine
    yaml = None  # type: ignore


# ── Skip layouts that don't need source / action title ────────────────────
LAYOUTS_WITHOUT_SOURCE = {
    "cover", "cover_centered", "toc", "section_divider", "closing", "appendix_title",
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


# ── Schema loader (api-schemas.yaml is the single source of truth) ───────
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "api-schemas.yaml"
_SCHEMA_CACHE: Optional[Dict[str, Any]] = None


def _schema() -> Dict[str, Any]:
    """Load api-schemas.yaml once and cache. Empty dict if unavailable."""
    global _SCHEMA_CACHE
    if _SCHEMA_CACHE is not None:
        return _SCHEMA_CACHE
    if yaml is None or not SCHEMA_PATH.exists():
        _SCHEMA_CACHE = {}
        return _SCHEMA_CACHE
    try:
        _SCHEMA_CACHE = yaml.safe_load(SCHEMA_PATH.read_text()) or {}
    except Exception:
        _SCHEMA_CACHE = {}
    return _SCHEMA_CACHE


def _layout_spec(layout: str) -> Optional[Dict[str, Any]]:
    return (_schema().get("layouts") or {}).get(layout)


def check_schema_structure(slide: Dict, idx: int) -> List[Dict]:
    """Schema-driven structural validation (counts, tuple arity, oval labels).

    Walks the layout's params spec and validates:
      - required scalars/lists are present
      - lists obey ``max`` / ``exact`` count limits
      - list items obey their declared tuple arity or list shape
      - tuple slots flagged ``role: oval_label`` obey ``max_chars`` (the
        ``label_too_long`` check)

    Char-budget enforcement on non-oval slots is intentionally soft (no
    issue raised) — those are budgets, not hard limits, and many decks
    already brush them.
    """
    layout = slide.get("layout", "")
    spec = _layout_spec(layout)
    if not spec or spec.get("status") == "retired":
        return []

    params = spec.get("params") or {}
    issues: List[Dict] = []
    for pname, pspec in params.items():
        if pname == "title" or not isinstance(pspec, dict):
            continue
        value = slide.get(pname)
        kind = pspec.get("kind", "scalar")
        required = pspec.get("required", False)

        if value is None or value == "":
            if required:
                issues.append({
                    "slide_idx": idx, "layout": layout, "check": "required_missing",
                    "message": f"{layout}.{pname} is required.",
                })
            continue

        if kind == "list":
            if not isinstance(value, (list, tuple)):
                issues.append({
                    "slide_idx": idx, "layout": layout, "check": "api_format",
                    "message": f"{layout}.{pname} must be a list; got {type(value).__name__}.",
                })
                continue
            n = len(value)
            exact = pspec.get("exact")
            cap = pspec.get("max")
            if exact is not None and n != exact:
                issues.append({
                    "slide_idx": idx, "layout": layout, "check": "count",
                    "message": f"{layout}.{pname} requires exactly {exact}; got {n}.",
                })
            elif cap is not None and n > cap:
                issues.append({
                    "slide_idx": idx, "layout": layout, "check": "count",
                    "message": f"{layout}.{pname} max {cap}; got {n}.",
                })
            issues += _check_list_items(slide, idx, layout, pname,
                                        value, pspec.get("item") or {})

    return issues


def _check_list_items(slide: Dict, idx: int, layout: str, pname: str,
                      items: List[Any], item_spec: Dict[str, Any]) -> List[Dict]:
    """Validate each element of a list parameter against its item spec."""
    issues: List[Dict] = []
    item_kind = item_spec.get("kind")
    if item_kind != "tuple":
        return issues
    arity = item_spec.get("arity")
    slots = item_spec.get("slots") or []
    for i, elem in enumerate(items):
        if not isinstance(elem, (list, tuple)):
            issues.append({
                "slide_idx": idx, "layout": layout, "check": "api_format",
                "message": f"{layout}.{pname}[{i}] must be a tuple/list; got {type(elem).__name__}.",
            })
            continue
        if arity is not None and len(elem) != arity:
            issues.append({
                "slide_idx": idx, "layout": layout, "check": "api_format",
                "message": (f"{layout}.{pname}[{i}] must be a {arity}-tuple; "
                            f"got {len(elem)} elements."),
            })
            continue
        # Per-slot checks: only enforce max_chars on oval_label slots.
        for slot_idx, slot in enumerate(slots):
            if slot_idx >= len(elem):
                break
            if slot.get("role") != "oval_label":
                continue
            slot_max = slot.get("max_chars")
            if not slot_max:
                continue
            slot_val = elem[slot_idx]
            try:
                slot_str = str(slot_val)
            except Exception:
                continue
            if len(slot_str) > slot_max:
                issues.append({
                    "slide_idx": idx, "layout": layout, "check": "label_too_long",
                    "message": (
                        f"{layout}.{pname}[{i}] slot[{slot_idx}] "
                        f"({slot.get('name','label')}) is {slot_str!r} ({len(slot_str)} chars > "
                        f"{slot_max}); rendered inside a 0.45\" oval and will visually clip. "
                        "Use a number, letter, or 2–3-char code; move long text into the title slot."
                    ),
                })
    return issues


# ── Per-layout checkers ───────────────────────────────────────────────────

def check_process_chevron_quirks(slide: Dict, idx: int) -> List[Dict]:
    """process_chevron-specific rules NOT covered by the schema:
    - step label cannot contain ``\\n`` (overflows the oval)
    - step desc ≤ 50 chars (geometry)

    Count and tuple-arity are handled by check_schema_structure.
    """
    issues: List[Dict] = []
    steps = slide.get("steps", [])
    for i, step in enumerate(steps):
        if not isinstance(step, (list, tuple)) or len(step) < 3:
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


# ── executive_summary frequency cap ───────────────────────────────────────
# executive_summary is the most permissive layout (3-tuple items, free-form
# desc), so the model funnels everything into it — the post-mortem v1 deck
# used it 9× in 30 slides. Capping at 15% of content slides forces variety.
EXEC_SUMMARY_CAP_PCT = 0.15


def check_executive_summary_cap_global(slides: List[Dict]) -> List[Dict]:
    """Cap ``executive_summary`` at 15% of content slides.

    Acceptance (per v0.5.0 spec):
        30 content slides + 5 executive_summary → fail (5/30 = 16.7% > 15%)
        30 content slides + 4 executive_summary → pass (4/30 = 13.3%)
    Small decks: at least one executive_summary is always allowed.
    """
    content_slides = [
        s for s in slides if s.get("layout") not in BOILERPLATE_LAYOUTS
    ]
    n_content = len(content_slides)
    if n_content == 0:
        return []
    es_count = sum(1 for s in content_slides if s.get("layout") == "executive_summary")
    max_allowed = max(1, int(EXEC_SUMMARY_CAP_PCT * n_content))
    if es_count <= max_allowed:
        return []
    return [{
        "slide_idx": "(global)",
        "layout": "executive_summary",
        "check": "executive_summary_cap",
        "message": (
            f"executive_summary used {es_count}× in {n_content} content slides "
            f"({es_count / n_content:.0%}); cap is {EXEC_SUMMARY_CAP_PCT:.0%} "
            f"(max {max_allowed} for this deck). executive_summary is the most "
            "permissive layout, so over-using it produces visually monotonous decks. "
            "Replace by content shape: "
            "(a) 3–4 numbered actions with rationale → four_column or vertical_steps; "
            "(b) one headline number + supporting detail → big_number_callout or "
            "content_right_image; "
            "(c) numbered items with a side panel → numbered_list_panel; "
            "(d) two contrasting positions → side_by_side or two_col_image_grid; "
            "(e) ranked findings → horizontal_bar or table_insight; "
            "(f) closing decisions / asks → executive_summary is fine for the final "
            "ask slide. See references/framework/planning-guide.md."
        ),
    }]


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
    # v0.5.3 new layouts that read as visual / framework
    "concept_three", "journey_map",
    # v0.5.4 new layouts
    "pyramid_staircase", "cycle_4stage",
}

# Boilerplate slides excluded from the content-slide count for density purposes.
BOILERPLATE_LAYOUTS = {"cover", "cover_centered", "toc", "section_divider", "closing", "appendix_title"}

VISUAL_DENSITY_THRESHOLD_SLIDES = 6   # ≥ 6 content slides triggers the rule


def _visual_density_min(n_content: int) -> int:
    """Linear floor: max(2, N // 4) visual slides for N content slides.

    Examples:
        6 slides → 2     12 slides → 3     20 slides → 5     30 slides → 7
    """
    return max(2, n_content // 4)


def check_visual_density_global(slides: List[Dict]) -> List[Dict]:
    """Reject decks whose visual-layout count falls below the linear floor.

    Rationale: the most common output failure of MBB-style skills is a deck
    that is well-written but visually monotonous — every slide is a text
    column or a card grid. The floor scales with deck length so a 30-slide
    deck needs visibly more variety than a 6-slide deck.
    """
    content_slides = [
        s for s in slides
        if s.get("layout") not in BOILERPLATE_LAYOUTS
    ]
    n_content = len(content_slides)
    if n_content < VISUAL_DENSITY_THRESHOLD_SLIDES:
        return []
    min_visual = _visual_density_min(n_content)
    visual_count = sum(
        1 for s in content_slides if s.get("layout") in VISUAL_LAYOUTS
    )
    if visual_count >= min_visual:
        return []
    return [{
        "slide_idx": "(global)",
        "layout": "(deck-level)",
        "check": "visual_density",
        "message": (
            f"Visual-density floor: deck has {n_content} content slides "
            f"but only {visual_count} visual (chart/diagram/image) layout(s); "
            f"≥ {min_visual} required (floor scales as max(2, N // 4)). "
            "Pick from charts (grouped_bar / line_chart / donut / pareto / "
            "horizontal_bar / waterfall), frameworks (matrix_2x2 / swot / "
            "risk_matrix / harvey_ball_table), images (case_study_image / "
            "three_images), or process visuals (process_chevron / timeline / "
            "value_chain). See references/framework/planning-guide.md § "
            "'Layout selection by task'."
        ),
    }]


# ── Routing ───────────────────────────────────────────────────────────────

# Layout-specific *quirks* that cannot be expressed in the schema. Structural
# checks (count, tuple arity, oval-label budget) come from check_schema_structure
# and run automatically for every slide.
LAYOUT_CHECKERS = {
    "process_chevron":     [check_process_chevron_quirks, check_source, check_action_title],
    "timeline":            [check_timeline_last_label,    check_source, check_action_title],
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
        # Schema-driven structural check runs for every slide before the
        # layout-specific quirks (process_chevron \n, timeline last-label, …).
        slide_issues.extend(check_schema_structure(slide, idx))
        for fn in checkers:
            slide_issues.extend(fn(slide, idx))
        if slide_issues:
            all_issues.extend(slide_issues)
        else:
            passed_items.append({"slide_idx": idx, "layout": layout, "status": "ok"})

    all_issues.extend(check_two_column_text_global(slides))
    all_issues.extend(check_executive_summary_cap_global(slides))
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
