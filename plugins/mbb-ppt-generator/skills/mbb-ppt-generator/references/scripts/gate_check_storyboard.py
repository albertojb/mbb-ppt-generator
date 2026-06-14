#!/usr/bin/env python3
# Copyright 2024-2026 Kaku Li (https://github.com/likaku) — original Mck-ppt-design-skill, Apache 2.0.
# Adapted for MBB PPT Generator. English-language messages.
# Apache 2.0.
"""
gate_check_storyboard.py — S2 storyboard gate (machine-readable).

Usage:
    python gate_check_storyboard.py <outline_json_path> <project_dir>

Output:
    <project_dir>/gate_storyboard.json

JSON structure:
{
    "passed": true|false,            # program-derived; do NOT verbally claim pass
    "slide_titles": ["Title 1", ...],
    "verdict": "PASS — proceed to S3" | "FAIL — set read_aloud_test: true in outline.json",
    "error": null | "description of what is missing"
}

Pass logic:
    passed = (outline_json["read_aloud_test"] is True)

Purpose:
    Forces the operator to read all slide titles aloud in order before
    committing to S3. Skipping storyboarding is the #1 cause of bad decks
    (post-mortem finding). This gate makes it a machine-enforced step.

    To pass: open outline.json, read all titles under "slides" aloud in order,
    confirm the narrative flows, then set "read_aloud_test": true and re-run.
"""

from __future__ import annotations
import sys
import json
from pathlib import Path


def run_gate(outline_path: str, project_dir: str) -> dict:
    """Run S2 storyboard gate. Returns a result dict."""
    outline_file = Path(outline_path)

    if not outline_file.exists():
        return {
            "passed": False,
            "slide_titles": [],
            "verdict": "FAIL — outline.json file not found",
            "error": f"file not found: {outline_path}",
        }

    try:
        outline = json.loads(outline_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {
            "passed": False,
            "slide_titles": [],
            "verdict": "FAIL — outline.json is not valid JSON",
            "error": str(e),
        }

    slides = outline.get("slides", [])
    titles = [s.get("title", f"(slide {i + 1} — no title)") for i, s in enumerate(slides)]

    read_aloud = outline.get("read_aloud_test")

    if read_aloud is not True:
        title_list = "\n".join(f"  {i + 1}. {t}" for i, t in enumerate(titles))
        return {
            "passed": False,
            "slide_titles": titles,
            "verdict": "FAIL — set read_aloud_test: true in outline.json",
            "error": (
                "read_aloud_test is missing or false.\n\n"
                "Read these slide titles aloud in order and confirm the narrative flows:\n"
                f"{title_list}\n\n"
                "Then set \"read_aloud_test\": true in outline.json and re-run."
            ),
        }

    return {
        "passed": True,
        "slide_titles": titles,
        "verdict": "PASS — proceed to S3",
        "error": None,
    }


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: gate_check_storyboard.py <outline_json_path> <project_dir>")
        return 2

    outline_path = sys.argv[1]
    project_dir = sys.argv[2]
    Path(project_dir).mkdir(parents=True, exist_ok=True)
    out = Path(project_dir) / "gate_storyboard.json"

    print(f"[gate_storyboard] checking: {outline_path}")
    result = run_gate(outline_path, project_dir)

    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[gate_storyboard] slides: {len(result['slide_titles'])}")
    print(f"[gate_storyboard] verdict: {result['verdict']}")

    if not result["passed"] and result.get("error"):
        print(f"\n[gate_storyboard] action required:\n{result['error']}")

    print(f"[gate_storyboard] result written to: {out}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
