#!/usr/bin/env python3
"""
Board QBR (Quarterly Business Review) example for MBB PPT Generator.

Demonstrates a different layout family from minimal_example.py — focuses on
operating-cadence layouts: dashboard, RAG status, Pareto, Harvey Ball
evaluation, case study. Useful as a starting template for board / steering-
committee meetings where the audience needs operational visibility plus
specific decisions.

Workflow is the same five-stage gate cycle as minimal_example.py, but the
content shape is more dashboard-heavy.

Run:
    python3 examples/board_qbr_example.py

Outputs:
    ppt-project-board-qbr/content.json
    ppt-project-board-qbr/gate_content.json
    ppt-project-board-qbr/deck.pptx
    ppt-project-board-qbr/gate_render.json

Apache 2.0. The bundled mck_ppt engine is Copyright Kaku Li (likaku); see NOTICE.
"""

from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

# ── Wire the bundled engine onto sys.path ──────────────────────────────────
SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT))

from mck_ppt import MckEngine
from mck_ppt.constants import (
    NAVY, ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED,
    LIGHT_BLUE, LIGHT_GREEN, LIGHT_ORANGE, LIGHT_RED, BG_GRAY,
)


# ── Project workspace ──────────────────────────────────────────────────────
PROJECT_DIR = SKILL_ROOT / "ppt-project-board-qbr"
PROJECT_DIR.mkdir(exist_ok=True)
DECK_PATH    = PROJECT_DIR / "deck.pptx"
GATE_RENDER  = PROJECT_DIR / "gate_render.json"

GATE_RENDER_SCRIPT = SKILL_ROOT / "references" / "scripts" / "gate_check_render.py"


def render_deck() -> None:
    """Build the QBR deck directly with the engine. (No content.json round-trip
    — this example shows the imperative path; minimal_example.py shows the
    declarative content.json path.)"""
    eng = MckEngine(total_slides=10)

    # ── 1. Cover ──────────────────────────────────────────────────────────
    eng.cover(
        title='Q4 2025 board QBR',
        subtitle='Operational dashboard and Q1 2026 priorities',
        author='Operations team',
        date='January 2026',
    )

    # ── 2. Executive summary — the headline ───────────────────────────────
    eng.executive_summary(
        title='Q4 closed strong; three priorities for Q1',
        headline='Revenue and margin both ahead of plan; one risk requires action',
        items=[
            ('1', 'Lock in Q4 wins',
                  'Renew premium accounts ahead of Q1 cycle'),
            ('2', 'Address service capacity',
                  'Hire 8 senior service reps in Q1'),
            ('3', 'Launch EMEA expansion',
                  'Sign 2 distributor contracts by end of February'),
        ],
        source='Source: Q4 close + Q1 plan, January 2026',
    )

    # ── 3. KPI dashboard ──────────────────────────────────────────────────
    eng.dashboard_kpi_chart(
        title='Q4 dashboard — revenue and margin ahead',
        kpi_cards=[
            ('$1.24B', 'Revenue',   '+24%',   NAVY),
            ('31%',    'Margin',    '+7pp',   ACCENT_BLUE),
            ('+8',     'NPS pts',   '+2.2',   ACCENT_GREEN),
            ('-57%',   'TTR',       'vs Q1',  ACCENT_ORANGE),
        ],
        chart_data={
            'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
            'actual': [220, 240, 285, 310],
            'target': [250, 250, 250, 280],
            'max_val': 350,
            'legend': [('Actual', NAVY), ('Target', BG_GRAY)],
        },
        summary='All KPIs ahead of plan.',
        source='Source: company financials',
    )

    # ── 4. RAG status — portfolio of initiatives ──────────────────────────
    eng.rag_status(
        title='Portfolio — 3 of 5 initiatives green',
        headers=['Project', 'Status', 'Owner', 'ETA', 'Note'],
        rows=[
            ('Premium relaunch', ACCENT_GREEN,  'Sales',  'Q2',  'On plan'),
            ('EMEA expansion',   ACCENT_GREEN,  'Reg.',   'Q3',  '2 closed'),
            ('Cost simp.',       ACCENT_GREEN,  'Ops',    'Q4',  '+5%'),
            ('Service uplift',   ACCENT_ORANGE, 'Service','Q3',  'Capacity gap'),
            ('New launch',       ACCENT_RED,    'Eng',    'FY26','Slipped'),
        ],
        source='Source: PMO weekly',
    )

    # ── 5. Pareto — what's driving service complaints ─────────────────────
    eng.pareto(
        title='Two issues drive 70% of service complaints',
        items=[
            ('Resolution time', 4200),
            ('First contact',   2100),
            ('Hold time',        640),
            ('Routing',          320),
            ('Tone',             180),
            ('Other',            130),
        ],
        summary='Time-to-resolve and first-contact resolution are the levers; '
                'service capacity hire addresses both.',
        source='Source: customer service tickets, Q4 2025',
    )

    # ── 6. Harvey Ball — scoring options for service capacity ─────────────
    eng.harvey_ball_table(
        title='Three options for service capacity expansion',
        criteria=[
            'Speed to impact',
            'Cost per FTE',
            'Capability fit',
            'Retention risk',
            'Quality of hires',
        ],
        options=['Internal hire', 'Contract', 'BPO partner'],
        scores=[
            [3, 4, 2],   # speed
            [2, 3, 4],   # cost
            [4, 3, 2],   # capability
            [4, 2, 3],   # retention (high score = low risk)
            [4, 3, 2],   # quality
        ],
        legend_text=['● Strong', '◑ Partial', '○ Weak'],
        summary='Internal hire scores best on capability and retention; '
                'BPO is fastest but weakest on quality.',
        source='Source: HR and Operations evaluation',
    )

    # ── 7. Case study — proof of approach ─────────────────────────────────
    eng.case_study(
        title='Acme reduced TTR by 57% in two quarters using the same playbook',
        sections=[
            ('S', 'Situation',
             'TTR at 4.2 days; service NPS at 6.2/10; rising churn'),
            ('A', 'Action',
             'Service redesign + 30 senior internal hires + retention bonuses'),
            ('R', 'Result',
             'TTR 1.8 days; NPS 8.4/10; churn -40%; net retention +110%'),
        ],
        result_box=(
            'Implication',
            'The approach is reproducible. We propose the same playbook for '
            'Q1 service capacity expansion, scaled to our footprint.',
        ),
        source='Source: Acme post-implementation review',
    )

    # ── 8. Decision matrix — what we are asking ───────────────────────────
    eng.matrix_2x2(
        title='Q1 priorities — high-value high-effort items first',
        quadrants=[
            ('Strategic bets', LIGHT_BLUE,
             'Service capacity hire ($4.2M, 8 senior FTE)'),
            ('Win zone', LIGHT_GREEN,
             'EMEA distributor contracts (2 deals, ~$8M annual revenue)'),
            ('Defer', LIGHT_RED,
             'API ecosystem — push to FY26 plan'),
            ('Quick wins', LIGHT_ORANGE,
             'Premium account renewals (Q1 cycle, ~$60M ARR)'),
        ],
        axis_labels=('Effort →', 'Value ↑'),
        bottom_bar=('Decision request',
                    'Approve Q1 budget for strategic bets and EMEA contracts.'),
        source='Source: Q1 plan',
    )

    # ── 9. Action items — concrete asks ───────────────────────────────────
    eng.action_items(
        title='Three decisions and an owner for each',
        actions=[
            ('Decision 1', 'Q1 W4',  'Approve $4.2M service capacity budget',  'CFO'),
            ('Decision 2', 'Q1 W6',  'Sign EMEA distributor contracts',         'VP Sales'),
            ('Decision 3', 'Q1 W8',  'Brief board on Q1 results vs. plan',     'CEO'),
        ],
        source='Source: operations team',
    )

    # ── 10. Closing ───────────────────────────────────────────────────────
    eng.closing(
        title='Discussion',
        message='Decision request and Q&A',
    )

    eng.save(str(DECK_PATH))
    print(f"[render] saved {DECK_PATH}")


def run_render_gate() -> bool:
    """Invoke the S4 render gate as a subprocess. Returns True if passed."""
    print(f"[gate] running gate_check_render.py …")
    result = subprocess.run(
        [sys.executable, str(GATE_RENDER_SCRIPT), str(DECK_PATH), str(PROJECT_DIR)],
        cwd=str(SKILL_ROOT),
    )
    return result.returncode == 0


def main() -> int:
    print("=" * 70)
    print("  MBB PPT Generator — board QBR example")
    print(f"  Project dir: {PROJECT_DIR.relative_to(SKILL_ROOT)}")
    print("=" * 70)

    render_deck()
    passed = run_render_gate()

    if not passed:
        print(f"\n❌ S4 gate FAILED. See {GATE_RENDER}.")
        return 1

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
