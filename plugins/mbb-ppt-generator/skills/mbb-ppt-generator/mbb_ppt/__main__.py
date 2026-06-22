# Copyright 2026 albertojb. Licensed under the Apache License, Version 2.0.
"""mbb-ppt CLI — one-shot render + gate runner.

Subcommands:
    mbb-ppt render <content.json> [--out deck.pptx] [--skip-gates]
    mbb-ppt gate-content <content.json>
    mbb-ppt gate-render <deck.pptx>
    mbb-ppt version

The CLI exits non-zero if any gate fails so it composes cleanly with shells
and CI. Run ``python -m mbb_ppt --help`` for the full reference.

content.json schema (minimum):
    {
      "slides": [
        {"layout": "cover", "title": "...", "subtitle": "...", ...},
        {"layout": "executive_summary", "title": "...", "items": [...], ...},
        ...
      ]
    }

Every slide dict must have a ``layout`` key matching an MbbEngine method name.
All other keys are passed through as kwargs to that method (after coercing
list-of-list → list-of-tuple where the engine expects tuples).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from mbb_ppt import gates as _gates


def _is_rgb_triple(v) -> bool:
    """Return True if v looks like a [r, g, b] triple of ints in [0, 255]."""
    return (
        isinstance(v, list)
        and len(v) == 3
        and all(isinstance(x, int) and 0 <= x <= 255 for x in v)
    )


def _is_hex_color(v) -> bool:
    return isinstance(v, str) and len(v) in (4, 7) and v.startswith("#")


def _to_color(v):
    from pptx.dml.color import RGBColor
    if _is_rgb_triple(v):
        return RGBColor(*v)
    if _is_hex_color(v):
        h = v.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    return None


def _resolve_color_name(name: str):
    """Resolve a `mbb_ppt.constants` color name (e.g. 'NAVY') to its RGBColor."""
    from mbb_ppt import constants as C
    val = getattr(C, name, None)
    from pptx.dml.color import RGBColor
    return val if isinstance(val, RGBColor) else None


def _coerce_for_engine(value):
    """Recursively convert JSON-friendly types into engine-friendly types.

    - Lists of lists become lists of tuples (engine signatures expect tuples for
      items/series/segments/cards/quadrants/etc.).
    - [r, g, b] triples and "#RRGGBB" strings are converted to RGBColor.
    - Strings matching a name in mbb_ppt.constants (e.g. "NAVY", "ACCENT_BLUE")
      are also converted to the corresponding RGBColor.
    """
    color = _to_color(value)
    if color is not None:
        return color
    if isinstance(value, str) and value.isupper() and value.replace("_", "").isalnum():
        named = _resolve_color_name(value)
        if named is not None:
            return named
    if isinstance(value, list):
        if value and all(isinstance(v, list) for v in value):
            return [tuple(_coerce_for_engine(v) for v in inner) for inner in value]
        return [_coerce_for_engine(v) for v in value]
    if isinstance(value, dict):
        return {k: _coerce_for_engine(v) for k, v in value.items()}
    return value


def _render(content_path: Path, out_path: Path) -> int:
    from mbb_ppt import MbbEngine

    with open(content_path) as f:
        content = json.load(f)
    slides = content.get("slides")
    if not slides:
        print(f"ERROR: {content_path} has no 'slides' array.", file=sys.stderr)
        return 2

    eng = MbbEngine(total_slides=len(slides))
    for i, slide in enumerate(slides, 1):
        layout = slide.get("layout")
        if not layout:
            print(f"ERROR: slide {i} missing 'layout'", file=sys.stderr)
            return 2
        method = getattr(eng, layout, None)
        if method is None or not callable(method):
            print(f"ERROR: slide {i} layout '{layout}' is not a valid MbbEngine method.", file=sys.stderr)
            return 2
        kwargs = {k: _coerce_for_engine(v) for k, v in slide.items() if k not in ("layout", "idx")}
        try:
            method(**kwargs)
        except TypeError as e:
            print(f"ERROR: slide {i} layout '{layout}' rejected kwargs: {e}", file=sys.stderr)
            return 2

    out_path.parent.mkdir(parents=True, exist_ok=True)
    eng.save(str(out_path))
    return 0


def _run_content_gate(content_path: str, project_dir: str) -> int:
    Path(project_dir).mkdir(parents=True, exist_ok=True)
    try:
        result = _gates.run_content_gate(content_path, project_dir)
    except Exception as e:
        print(f"ERROR: content gate raised: {e}", file=sys.stderr)
        return 2
    out = Path(project_dir) / "gate_content.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"[gate_content] checking: {content_path}")
    print(f"[gate_content] slides: {result.get('total_slides', '?')}")
    print(f"[gate_content] fail items: {len(result.get('fail_items', []))}")
    print(f"[gate_content] verdict: {result.get('verdict', '')}")
    print(f"[gate_content] result written to: {out}")
    return 0 if result.get("passed") else 1


def _run_render_gate(pptx_path: str, project_dir: str) -> int:
    Path(project_dir).mkdir(parents=True, exist_ok=True)
    try:
        result = _gates.run_render_gate(pptx_path, project_dir)
    except Exception as e:
        print(f"ERROR: render gate raised: {e}", file=sys.stderr)
        return 2
    out = Path(project_dir) / "gate_render.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    cl = result.get("checklist", {})
    print(f"[gate_render] checking: {pptx_path}")
    print(f"[gate_render] score: {result.get('overall_score', 'n/a')}/100")
    print(f"[gate_render] user_code_errors: {cl.get('user_code_errors', 0)}")
    print(f"[gate_render] engine_bug_errors (whitelisted): {cl.get('engine_bug_errors', 0)}")
    print(f"[gate_render] warnings: {cl.get('warnings', 0)}")
    print(f"[gate_render] verdict: {result.get('verdict', '')}")
    print(f"[gate_render] result written to: {out}")
    return 0 if result.get("passed") else 1


def cmd_render(args) -> int:
    content_path = Path(args.content_json).resolve()
    if not content_path.is_file():
        print(f"ERROR: {content_path} not found.", file=sys.stderr)
        return 2

    out_path = Path(args.out).resolve() if args.out else content_path.parent / "deck.pptx"
    project_dir = out_path.parent

    if not args.skip_gates:
        rc = _run_content_gate(str(content_path), str(project_dir))
        if rc != 0:
            print("S3 content gate failed; not rendering.", file=sys.stderr)
            return rc

    rc = _render(content_path, out_path)
    if rc != 0:
        return rc
    print(f"Rendered: {out_path}")

    if not args.skip_gates:
        rc = _run_render_gate(str(out_path), str(project_dir))
        if rc != 0:
            print("S4 render gate failed.", file=sys.stderr)
            return rc
        print("Both gates passed.")
    return 0


def cmd_gate_content(args) -> int:
    content_path = Path(args.content_json).resolve()
    return _run_content_gate(str(content_path), str(content_path.parent))


def cmd_gate_render(args) -> int:
    deck_path = Path(args.deck_pptx).resolve()
    return _run_render_gate(str(deck_path), str(deck_path.parent))


def cmd_version(args) -> int:
    from mbb_ppt import __version__
    print(__version__)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="mbb-ppt",
        description="MBB PPT Generator CLI — render content.json into a .pptx and run both QA gates.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    p_render = sub.add_parser("render", help="Render content.json -> deck.pptx and run both gates.")
    p_render.add_argument("content_json", help="Path to content.json")
    p_render.add_argument("--out", help="Output .pptx path (default: <content_dir>/deck.pptx)")
    p_render.add_argument("--skip-gates", action="store_true", help="Skip S3 + S4 gates (debug only)")
    p_render.set_defaults(func=cmd_render)

    p_gc = sub.add_parser("gate-content", help="Run only the S3 content gate.")
    p_gc.add_argument("content_json")
    p_gc.set_defaults(func=cmd_gate_content)

    p_gr = sub.add_parser("gate-render", help="Run only the S4 render gate.")
    p_gr.add_argument("deck_pptx")
    p_gr.set_defaults(func=cmd_gate_render)

    p_v = sub.add_parser("version", help="Print the installed mbb_ppt version.")
    p_v.set_defaults(func=cmd_version)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
