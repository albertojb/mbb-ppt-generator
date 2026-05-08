#!/usr/bin/env python3
"""
Minimal end-to-end example for MBB PPT Generator.

Demonstrates the full five-stage workflow on a 6-slide Q1 strategy review:

    S1  Brief         — defined inline in this script (in production: brief.md)
    S2  Outline       — implicit (the `slides` list below is the outline)
    S3  Content       — written to ppt-project-demo/content.json
    S3 GATE           — gate_check_content.py validates the JSON
    S4  Render        — engine renders content.json into deck.pptx
    S4 GATE           — gate_check_render.py runs PptQA on the .pptx
    S5  Deliver       — confirm passed: true and report success

Run:
    python3 examples/minimal_example.py

Outputs:
    ppt-project-demo/content.json     — S3 artifact
    ppt-project-demo/gate_content.json — S3 gate result
    ppt-project-demo/deck.pptx        — rendered deck
    ppt-project-demo/gate_render.json — S4 gate result

Apache 2.0. The bundled mbb_ppt engine is Copyright Kaku Li (likaku); see NOTICE.
"""

from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

# ── Wire the bundled engine onto sys.path ──────────────────────────────────
SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from mbb_ppt import MbbEngine
from mbb_ppt.constants import NAVY, ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE


# ── Project workspace ──────────────────────────────────────────────────────
PROJECT_DIR = SKILL_ROOT / "ppt-project-demo"
PROJECT_DIR.mkdir(exist_ok=True)
CONTENT_JSON = PROJECT_DIR / "content.json"
DECK_PATH    = PROJECT_DIR / "deck.pptx"
GATE_CONTENT = PROJECT_DIR / "gate_content.json"
GATE_RENDER  = PROJECT_DIR / "gate_render.json"

GATE_CONTENT_SCRIPT = SKILL_ROOT / "references" / "scripts" / "gate_check_content.py"
GATE_RENDER_SCRIPT  = SKILL_ROOT / "references" / "scripts" / "gate_check_render.py"


# ── S1 (Brief) + S2 (Outline) inline ───────────────────────────────────────
# In production these are separate artifacts (brief.md and outline.json). For a
# self-contained example, we collapse them into the content spec below.
BRIEF = {
    "audience": "Board",
    "goal": "Approve three actions to return revenue to double-digit growth",
    "duration_minutes": 6,
    "key_messages": [
        "Growth is concentrated in two channels and one product tier.",
        "Three complementary actions can recover the gap within one planning cycle.",
        "A phased rollout reduces execution risk and accelerates learning.",
    ],
}


# ── S3 content.json (the single source of truth for what gets rendered) ────
SLIDES = [
    {
        "idx": 1,
        "layout": "cover",
        "title": "Q1 2026 strategy review",
        "subtitle": "Board update — three actions to recover growth",
        "author": "Strategy team",
        "date": "March 2026",
    },
    {
        "idx": 2,
        "layout": "executive_summary",
        "title": "Three complementary actions return revenue to growth",
        "headline": "Growth is concentrated in two channels and one product tier",
        "items": [
            ["1", "Shift mix to premium",
                  "Higher margin, limited cost impact"],
            ["2", "Expand in underused channels",
                  "Two distributors remain underpenetrated"],
            ["3", "Fund through simplification",
                  "Back-office cost can shrink without service hit"],
        ],
        "source": "Source: internal analysis, Q1 2026",
    },
    {
        "idx": 3,
        "layout": "table_insight",
        "title": "Three actions improve growth while protecting margin",
        "headers": ["Action", "Mechanism", "Expected impact"],
        "rows": [
            ["Premium bundles",     "Raise mix in high-value segments",          "Revenue +12%"],
            ["Channel expansion",   "Add distributor reach in two verticals",    "Revenue +8%"],
            ["Cost simplification", "Reduce duplication across support teams",   "Margin +3pp"],
        ],
        "insights": [
            "The actions are complementary, not sequential.",
            "The first two accelerate growth; the third funds execution.",
            "Each action is feasible within the next planning cycle.",
        ],
        "source": "Source: strategy team analysis",
    },
    {
        "idx": 4,
        "layout": "grouped_bar",
        "title": "Premium and partner channels lead growth",
        "categories": ["Q1", "Q2", "Q3", "Q4"],
        "series": [["Premium", NAVY], ["Partner", ACCENT_BLUE]],
        "data": [[120, 80], [145, 95], [160, 110], [180, 130]],
        "max_val": 200,
        "source": "Source: finance team, Q1 2026 close",
    },
    {
        "idx": 5,
        "layout": "timeline",
        "title": "A phased rollout reduces execution risk and accelerates learning",
        "milestones": [
            ["Q1", "Design and prioritization"],
            ["Q2", "Pilot launch"],
            ["Q3", "Scale-up"],
            ["Q4", "Measure and refine"],
        ],
        "source": "Source: PMO",
    },
    {
        "idx": 6,
        "layout": "closing",
        "title": "Thank you",
        "message": "Discussion and decision points",
    },
]

CONTENT = {"brief": BRIEF, "slides": SLIDES}


# ── Stage runners ──────────────────────────────────────────────────────────

def write_content_json() -> None:
    """S3 artifact: persist content spec for the gate to validate."""
    CONTENT_JSON.write_text(json.dumps(CONTENT, indent=2, ensure_ascii=False))
    print(f"[S3] wrote {CONTENT_JSON}")


def run_gate(script: Path, *args: str, label: str) -> bool:
    """Invoke a gate script as a subprocess; return True if passed."""
    print(f"[{label}] running {script.name} …")
    result = subprocess.run(
        [sys.executable, str(script), *args],
        cwd=str(SKILL_ROOT),
    )
    return result.returncode == 0


def render_deck() -> None:
    """S4: drive the engine from CONTENT['slides']."""
    eng = MbbEngine(total_slides=len(SLIDES))
    for slide in SLIDES:
        spec = {k: v for k, v in slide.items() if k not in ("idx", "layout")}
        layout = slide["layout"]
        method = getattr(eng, layout, None)
        if method is None:
            raise RuntimeError(f"Unknown layout {layout!r} on slide {slide['idx']}")
        # Convert nested lists back to tuples where the engine expects them
        # (e.g. (color, name) pairs in series). The engine accepts both, but
        # this keeps the call signature clean.
        if "series" in spec:
            spec["series"] = [tuple(s) for s in spec["series"]]
        method(**spec)
    eng.save(str(DECK_PATH))
    print(f"[S4] rendered {DECK_PATH}")


# ── Main pipeline ──────────────────────────────────────────────────────────

def main() -> int:
    print("=" * 70)
    print("  MBB PPT Generator — minimal example")
    print(f"  Project dir: {PROJECT_DIR.relative_to(SKILL_ROOT)}")
    print("=" * 70)

    # S3: write content + run content gate
    write_content_json()
    if not run_gate(GATE_CONTENT_SCRIPT, str(CONTENT_JSON), str(PROJECT_DIR),
                    label="S3 GATE"):
        print(f"\n❌ S3 gate FAILED. See {GATE_CONTENT}.")
        return 1

    # S4: render + run render gate
    render_deck()
    if not run_gate(GATE_RENDER_SCRIPT, str(DECK_PATH), str(PROJECT_DIR),
                    label="S4 GATE"):
        print(f"\n❌ S4 gate FAILED. See {GATE_RENDER}.")
        return 1

    # S5: deliver
    render_result = json.loads(GATE_RENDER.read_text())
    print()
    print("=" * 70)
    print(f"  ✅ DELIVERED — {DECK_PATH}")
    print(f"     score: {render_result.get('overall_score', 'n/a')}/100")
    print(f"     user_code_errors: 0   (whitelisted engine_bug_errors: "
          f"{render_result['checklist']['engine_bug_errors']})")
    print(f"     warnings: {render_result['checklist']['warnings']}")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
