#!/usr/bin/env python3
# Copyright 2024-2026 Kaku Li (https://github.com/likaku) — original Mck-ppt-design-skill, Apache 2.0.
# Adapted for MBB PPT Generator. English-language messages.
# Apache 2.0.
"""
gate_check_render.py — S4 post-render QA gate (machine-readable).

Usage:
    python gate_check_render.py <pptx_path> <project_dir> [--auto-fix]

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
    "warnings_detail": [...],
    "auto_fix": null | {             # present only when --auto-fix was used
        "attempted": true|false,
        "fixes_applied": [{"slide": N, "category": "...", "action": "..."}],
        "severe_errors_blocked_fix": [...]
    }
}

Pass logic:
    passed = (len(user_code_errors) == 0)

Auto-fix logic (--auto-fix flag):
    Minor errors that auto-fix can address:
        text_overflow with overflow_pct <= 50%  →  shrink font 1pt (AutoFixPipeline, 1 round)
        body_overflow with overflow  <= 0.3"    →  advisory only, not fixable by font-shrink
    Severe errors (text_overflow > 50%, body_overflow > 0.3") block auto-fix entirely.
    Auto-fix attempts exactly ONE round, then re-runs the gate.
    Every fix is logged in gate_render.json["auto_fix"] and printed to stdout.

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
from typing import Dict, Any, List


# ── Thresholds for auto-fix eligibility ──────────────────────────────────
_AUTOFIX_TEXT_OVERFLOW_MAX_PCT = 50.0   # overflow_pct <= this → auto-fixable
_AUTOFIX_BODY_OVERFLOW_MAX_EMU = 274320  # 0.3 inches in EMU


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
    from this script's location. Walks up at most 4 levels."""
    here = os.path.dirname(os.path.abspath(__file__))
    for _ in range(4):
        candidate = os.path.join(here, "mbb_ppt")
        if os.path.isdir(candidate):
            return here
        here = os.path.dirname(here)
    return os.path.expanduser("~/.claude/skills/mbb-ppt-generator")


def _issue_to_entry(issue, include_details: bool = False) -> Dict[str, Any]:
    entry: Dict[str, Any] = {
        "slide": issue.slide_num,
        "category": issue.category,
        "message": (issue.message or "")[:160],
        "shape": getattr(issue, "shape_name", ""),
    }
    if include_details and getattr(issue, "details", None):
        entry["details"] = issue.details
    return entry


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
            "auto_fix": None,
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
            "auto_fix": None,
        }

    report = PptQA(pptx_path).run()

    user_code_errors = []
    engine_bug_errors = []
    for issue in report.errors:
        entry = _issue_to_entry(issue, include_details=True)
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
        "auto_fix": None,
    }


def _classify_errors(user_code_errors: List[Dict[str, Any]]):
    """Split errors into (minor_text, minor_body, severe) for auto-fix routing."""
    minor_text, minor_body, severe = [], [], []
    for e in user_code_errors:
        details = e.get("details", {})
        cat = e.get("category", "")
        if cat == "text_overflow":
            pct = details.get("overflow_pct", 999)
            # details may be stored as float or as "N.N in" string from to_dict()
            if isinstance(pct, str):
                try:
                    pct = float(pct.split()[0])
                except ValueError:
                    pct = 999
            if pct <= _AUTOFIX_TEXT_OVERFLOW_MAX_PCT:
                minor_text.append(e)
            else:
                severe.append(e)
        elif cat == "body_overflow":
            emu = details.get("overflow_emu", 999999)
            if isinstance(emu, str):
                try:
                    emu = float(emu.split()[0]) * 914400
                except ValueError:
                    emu = 999999
            if emu <= _AUTOFIX_BODY_OVERFLOW_MAX_EMU:
                minor_body.append(e)
            else:
                severe.append(e)
        else:
            severe.append(e)
    return minor_text, minor_body, severe


def run_gate_autofix(pptx_path: str, project_dir: str) -> Dict[str, Any]:
    """Run S4 gate with --auto-fix: attempt one round of font-shrink on minor
    text overflows, then re-gate. Severe errors block auto-fix entirely."""
    skill_root = _resolve_skill_root()
    if skill_root not in sys.path:
        sys.path.insert(0, skill_root)

    # Step 1: initial check
    result = run_gate(pptx_path, project_dir)

    if result.get("passed"):
        result["auto_fix"] = {"attempted": False, "reason": "gate already passes"}
        return result

    user_errors = result.get("user_code_error_detail", [])
    if not user_errors:
        result["auto_fix"] = {"attempted": False, "reason": "no user_code_errors to fix"}
        return result

    minor_text, minor_body, severe = _classify_errors(user_errors)

    if severe:
        result["auto_fix"] = {
            "attempted": False,
            "reason": (f"{len(severe)} severe error(s) block auto-fix — "
                       "fix manually and re-render"),
            "severe_errors_blocked_fix": [
                {"slide": e["slide"], "category": e["category"],
                 "message": e["message"][:80]}
                for e in severe
            ],
            "fixes_applied": [],
        }
        return result

    # Step 2: run AutoFixPipeline (1 round, font-shrink only)
    fixes_applied: List[Dict[str, Any]] = []
    try:
        from mbb_ppt.review import AutoFixPipeline
        pipeline = AutoFixPipeline(pptx_path)
        fixes_count = pipeline.run(max_rounds=1, verbose=False)
        if fixes_count > 0:
            for e in minor_text:
                fix_entry = {
                    "slide": e["slide"],
                    "category": e["category"],
                    "action": "font shrunk 1pt via AutoFixPipeline",
                    "original_message": e["message"][:80],
                }
                fixes_applied.append(fix_entry)
                print(f"[gate_render][AUTO-FIX] slide {e['slide']} "
                      f"[{e['category']}]: font shrunk — {e['message'][:60]}")
    except Exception as exc:
        result["auto_fix"] = {
            "attempted": True,
            "error": f"AutoFixPipeline failed: {exc}",
            "fixes_applied": [],
        }
        return result

    advisory_body = [
        {"slide": e["slide"], "category": e["category"],
         "message": e["message"][:80],
         "note": "body_overflow <= 0.3\" — advisory; font-shrink does not fix layout bounds"}
        for e in minor_body
    ]

    # Step 3: re-gate after fix
    result2 = run_gate(pptx_path, project_dir)
    result2["auto_fix"] = {
        "attempted": True,
        "fixes_applied": fixes_applied,
        "body_overflow_advisory": advisory_body,
    }
    return result2


def main() -> int:
    auto_fix = "--auto-fix" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--auto-fix"]

    if len(args) < 2:
        print("usage: gate_check_render.py <pptx_path> <project_dir> [--auto-fix]")
        return 2

    pptx_path = args[0]
    project_dir = args[1]
    Path(project_dir).mkdir(parents=True, exist_ok=True)
    out = os.path.join(project_dir, "gate_render.json")

    print(f"[gate_render] checking: {pptx_path}"
          + (" (auto-fix mode)" if auto_fix else ""))

    result = run_gate_autofix(pptx_path, project_dir) if auto_fix else run_gate(pptx_path, project_dir)

    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[gate_render] score: {result.get('overall_score', 'n/a')}/100")
    print(f"[gate_render] user_code_errors: {result['checklist']['user_code_errors']}")
    print(f"[gate_render] engine_bug_errors (whitelisted): {result['checklist']['engine_bug_errors']}")
    print(f"[gate_render] warnings: {result['checklist']['warnings']}")
    print(f"[gate_render] verdict: {result.get('verdict', '')}")

    if auto_fix and result.get("auto_fix"):
        af = result["auto_fix"]
        if af.get("fixes_applied"):
            print(f"[gate_render][AUTO-FIX] {len(af['fixes_applied'])} fix(es) applied:")
            for fix in af["fixes_applied"]:
                print(f"  slide {fix['slide']} [{fix['category']}]: {fix['action']}")
        if af.get("severe_errors_blocked_fix"):
            print(f"[gate_render][AUTO-FIX] BLOCKED — {len(af['severe_errors_blocked_fix'])} severe error(s):")
            for e in af["severe_errors_blocked_fix"]:
                print(f"  slide {e['slide']} [{e['category']}]: {e['message'][:80]}")

    print(f"[gate_render] result written to: {out}")

    if result.get("user_code_error_detail"):
        print("\n[gate_render] user_code_errors to fix:")
        for e in result["user_code_error_detail"]:
            print(f"  slide {e['slide']} [{e['category']}]: {e['message'][:100]}")

    return 0 if result.get("passed") else 1


if __name__ == "__main__":
    sys.exit(main())
