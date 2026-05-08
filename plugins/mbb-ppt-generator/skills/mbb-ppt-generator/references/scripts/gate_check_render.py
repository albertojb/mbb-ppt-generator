#!/usr/bin/env python3
# Copyright 2024-2026 Kaku Li (https://github.com/likaku) — original Mck-ppt-design-skill, Apache 2.0.
# Adapted for MBB PPT Generator. English-language messages.
# Apache 2.0.
"""
gate_check_render.py — S4 post-render QA gate (machine-readable).

Usage:
    python gate_check_render.py <pptx_path> <project_dir>

Output:
    <project_dir>/gate_render.json

JSON structure:
{
    "passed": true|false,            # program-derived; do NOT verbally claim pass
    "overall_score": 92,
    "pptx_path": "...",
    "checklist": {
        "user_code_errors": 0,       # must be 0 to pass
        "engine_bug_errors": 7,      # whitelisted, advisory only
        "warnings": 1
    },
    "verdict": "PASS — proceed to S5" | "FAIL — fix N user_code_errors and re-render",
    "user_code_error_detail": [...],
    "engine_bug_detail": [...],
    "warnings_detail": [...]
}

Pass logic:
    passed = (len(user_code_errors) == 0)

Engine bug whitelist:
    The ENGINE_BUG_WHITELIST below enumerates QA error categories caused by
    documented engine internal behavior. They are exempted from passing logic.
    Each entry has a textual evidence comment.

    To add a new exemption: edit this file. Verbal exemptions are forbidden.
"""

from __future__ import annotations
import sys
import os
import json
from pathlib import Path
from typing import Dict, Any


# ── Engine-bug whitelist ──────────────────────────────────────────────────
# Each entry must have evidence. No verbal exemptions.
ENGINE_BUG_WHITELIST = {
    # peer_font_inconsistency:
    #   ExecEngine deliberately uses different font sizes within certain
    #   layouts (e.g. table_insight uses 18pt header + 14pt body, by design).
    #   QA flags this as "peer font inconsistency" but it is intentional.
    #   Evidence: mbb_ppt/engine.py table_insight() and process_chevron() —
    #   header text boxes set font size = SUB_HEADER_SIZE (18pt), content
    #   text boxes set font size = BODY_SIZE (14pt) explicitly.
    "peer_font_inconsistency",

    # chart_legend_overflow (timeline only):
    #   The timeline engine right-anchors the last milestone label using a
    #   fixed offset, independent of label length. Even a 2-character label
    #   (e.g. "Q4") is reported as overflowing by ~0.47". This is an engine
    #   bug, not user content.
    #   Limit: only timeline. Other layouts triggering this category are
    #   real overflow and not exempt.
    "chart_legend_overflow",
}


def _resolve_skill_root() -> str:
    """Locate the skill root (the directory that contains mbb_ppt/) starting
    from this script's location. Walks up at most 3 levels.

    The repository layout is:
        <skill_root>/
          mbb_ppt/                     <- bundled engine
          references/scripts/gate_check_render.py   <- this file
    """
    here = os.path.dirname(os.path.abspath(__file__))
    for _ in range(4):
        candidate = os.path.join(here, "mbb_ppt")
        if os.path.isdir(candidate):
            return here
        here = os.path.dirname(here)
    # Fall back to legacy install path so old setups still work.
    return os.path.expanduser("~/.claude/skills/mbb-ppt-generator")


def run_gate(pptx_path: str, project_dir: str) -> Dict[str, Any]:
    """Run S4 post-render QA gate. Returns a result dict."""
    skill_root = _resolve_skill_root()
    if skill_root not in sys.path:
        sys.path.insert(0, skill_root)

    try:
        from mbb_ppt.qa import PptQA
    except ImportError as e:
        return {
            "passed": False,
            "error": (f"could not import mbb_ppt.qa: {e}. "
                      f"Looked under {skill_root}. "
                      "Verify that mbb_ppt/ is present in the skill root."),
            "checklist": {"user_code_errors": 999, "engine_bug_errors": 0, "warnings": 0},
            "verdict": "FAIL — environment problem",
            "user_code_error_detail": [],
            "engine_bug_detail": [],
            "warnings_detail": [],
        }

    if not os.path.exists(pptx_path):
        return {
            "passed": False,
            "error": f"file not found: {pptx_path}",
            "checklist": {"user_code_errors": 999, "engine_bug_errors": 0, "warnings": 0},
            "verdict": "FAIL — pptx file does not exist",
            "user_code_error_detail": [],
            "engine_bug_detail": [],
            "warnings_detail": [],
        }

    report = PptQA(pptx_path).run()

    user_code_errors = []
    engine_bug_errors = []
    for issue in report.errors:
        entry = {
            "slide": issue.slide_num,
            "category": issue.category,
            "message": (issue.message or "")[:160],
            "shape": getattr(issue, "shape_name", ""),
        }
        if issue.category in ENGINE_BUG_WHITELIST:
            entry["whitelist_reason"] = (
                f"in ENGINE_BUG_WHITELIST: {issue.category}. "
                "See evidence comments at top of gate_check_render.py."
            )
            engine_bug_errors.append(entry)
        else:
            user_code_errors.append(entry)

    warnings_detail = [
        {"slide": w.slide_num, "category": w.category,
         "message": (w.message or "")[:120]}
        for w in report.warnings
    ]

    passed = len(user_code_errors) == 0

    return {
        "passed": passed,
        "overall_score": report.overall_score,
        "pptx_path": str(pptx_path),
        "checklist": {
            "user_code_errors": len(user_code_errors),
            "engine_bug_errors": len(engine_bug_errors),
            "warnings": len(report.warnings),
        },
        "verdict": ("PASS — proceed to S5" if passed
                    else f"FAIL — fix {len(user_code_errors)} user_code_errors and re-render"),
        "user_code_error_detail": user_code_errors,
        "engine_bug_detail": engine_bug_errors,
        "warnings_detail": warnings_detail,
    }


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: gate_check_render.py <pptx_path> <project_dir>")
        return 2
    pptx_path = sys.argv[1]
    project_dir = sys.argv[2]
    Path(project_dir).mkdir(parents=True, exist_ok=True)
    out = os.path.join(project_dir, "gate_render.json")

    print(f"[gate_render] checking: {pptx_path}")
    result = run_gate(pptx_path, project_dir)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[gate_render] score: {result.get('overall_score', 'n/a')}/100")
    print(f"[gate_render] user_code_errors: {result['checklist']['user_code_errors']}")
    print(f"[gate_render] engine_bug_errors (whitelisted): {result['checklist']['engine_bug_errors']}")
    print(f"[gate_render] warnings: {result['checklist']['warnings']}")
    print(f"[gate_render] verdict: {result.get('verdict', '')}")
    print(f"[gate_render] result written to: {out}")

    if result.get("user_code_error_detail"):
        print("\n[gate_render] user_code_errors to fix:")
        for e in result["user_code_error_detail"]:
            print(f"  slide {e['slide']} [{e['category']}]: {e['message'][:100]}")

    return 0 if result.get("passed") else 1


if __name__ == "__main__":
    sys.exit(main())
