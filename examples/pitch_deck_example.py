#!/usr/bin/env python3
"""
Pitch deck example for MBB PPT Generator — visual-variety reference.

Demonstrates the layout mix the visual-density gate (added in v0.2.1)
expects: a 9-content-slide pitch deck that uses charts, frameworks,
process visuals, and a timeline rather than walls of text columns.

This example exists specifically to address the most common output
failure pattern: well-written but visually monotonous decks. Use it as
a starting template for fundraising, partnership, or external-facing
investor materials.

Layout mix:
    1.  cover                  (boilerplate)
    2.  three_stat             (problem in numbers)
    3.  executive_summary      (the ask + opportunity)
    4.  donut                  (market sizing)                       ★ chart
    5.  matrix_2x2             (competitive landscape)               ★ framework
    6.  horizontal_bar         (channel strategy)                    ★ chart
    7.  process_chevron        (go-to-market sequence)               ★ process
    8.  timeline               (roadmap)                              ★ process
    9.  action_items           (the ask + commitments)
    10. closing                (boilerplate)

Run:
    python3 examples/pitch_deck_example.py

Outputs:
    ppt-project-pitch/deck.pptx
    ppt-project-pitch/gate_render.json (passed: true)

Apache 2.0. The bundled mbb_ppt engine is Copyright Kaku Li (likaku); see NOTICE.
"""

from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = SKILL_ROOT / "plugins" / "mbb-ppt-generator" / "skills" / "mbb-ppt-generator"
sys.path.insert(0, str(SKILL_DIR))

from mbb_ppt import MbbEngine
from mbb_ppt.constants import (
    NAVY, ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED,
    LIGHT_BLUE, LIGHT_GREEN, LIGHT_ORANGE, LIGHT_RED, BG_GRAY,
)


PROJECT_DIR = SKILL_ROOT / "ppt-project-pitch"
PROJECT_DIR.mkdir(exist_ok=True)
DECK_PATH    = PROJECT_DIR / "deck.pptx"
GATE_RENDER  = PROJECT_DIR / "gate_render.json"
GATE_RENDER_SCRIPT = SKILL_DIR / "references" / "scripts" / "gate_check_render.py"


def render_deck() -> None:
    """Build the pitch deck imperatively. The narrative is intentionally
    chart-heavy to demonstrate visual variety."""
    eng = MbbEngine(total_slides=10)

    # ── 1. Cover ──────────────────────────────────────────────────────────
    eng.cover(
        title='Northwind sports academies',
        subtitle='The operating system for LATAM grassroots academies',
        author='Founders, Northwind',
        date='Q2 2026',
    )

    # ── 2. Three-stat — problem in numbers ────────────────────────────────
    eng.three_stat(
        title='Community sports academies in LATAM run on spreadsheets and hope',
        stats=[
            ('20+ hrs', 'manual ops per month per academy', False),
            ('27%', 'of revenue lost to payment friction', True),
            ('< 5%', 'have any digital ops platform', False),
        ],
        detail_items=[
            'Owners reconcile bank transfers by hand each Monday',
            'Parents miss payments because reminders are WhatsApp ad-hoc',
            'No incumbent platform fits LATAM payment rails or pricing',
        ],
        source='Source: founder interviews with 32 academy owners across MX, CO, CR, 2026',
    )

    # ── 3. Executive summary — the opportunity ────────────────────────────
    eng.executive_summary(
        title='Northwind replaces spreadsheet chaos with one LATAM-native platform',
        headline='Operations, payments, and parent comms in one product',
        items=[
            ('1', 'Operations',
                  'Seasons, teams, fees; instant debtor view'),
            ('2', 'Payments',
                  'SINPE, OXXO, bank transfer with one-tap reconciliation'),
            ('3', 'Parent portal',
                  'Mobile calendar, reminders, payments in a few taps'),
        ],
        source='Source: company materials, May 2026',
    )

    # ── 4. Donut — TAM in segments (CHART) ────────────────────────────────
    eng.donut(
        title='LATAM TAM: 50K academies × $480 ARPA = $24M ARR opportunity',
        segments=[
            (0.42, ACCENT_BLUE,   'Mexico (21K)'),
            (0.20, ACCENT_GREEN,  'Brazil (10K)'),
            (0.14, ACCENT_ORANGE, 'Colombia (7K)'),
            (0.09, NAVY,          'Argentina (4.5K)'),
            (0.07, ACCENT_RED,    'Costa Rica (3.5K)'),
            (0.08, BG_GRAY,       'Other (4K)'),
        ],
        center_label='50K',
        center_sub='academies',
        summary='Mexico is the beachhead — 42% of TAM and shared payment rails with Costa Rica',
        source='Source: FIFA Connect, Sport England LATAM, founder market sizing 2026',
    )

    # ── 5. Matrix 2x2 — competitive positioning (FRAMEWORK) ───────────────
    eng.matrix_2x2(
        title='Global tools fail on LATAM payments; no local alternative exists',
        quadrants=[
            ('Global, full-featured',  LIGHT_RED,    'TeamSnap, SportsEngine — strong product but no LATAM payments, USD pricing'),
            ('LATAM-native, simple',   LIGHT_GREEN,  'Northwind — local payments, Spanish-first, USD priced for LATAM ARPU'),
            ('Global, simple',         LIGHT_ORANGE, 'Generic scheduling apps — Calendly clones; no payments, no parent comms'),
            ('LATAM-native, complex',  LIGHT_BLUE,   '(empty quadrant) — academies cannot afford complex on-prem'),
        ],
        axis_labels=('Product depth →', 'LATAM-native ↑'),
        source='Source: competitive teardown, March 2026',
    )

    # ── 6. Horizontal bar — channel strategy (CHART) ──────────────────────
    eng.horizontal_bar(
        title='Founder referrals and league partnerships drive 80% of pipeline',
        items=[
            ('Founder referral',     90, ACCENT_BLUE),
            ('League partnership',   62, ACCENT_GREEN),
            ('Coach community',      38, ACCENT_ORANGE),
            ('Content / SEO',        14, NAVY),
            ('Paid social',           8, ACCENT_RED),
        ],
        summary=('Channel mix', 'Phase 1 stays inside the top three; paid acquisition unlocks at 30+ academies'),
        source='Source: pilot CAC payback analysis, Q1 2026',
    )

    # ── 7. Process chevron — GTM (PROCESS) ────────────────────────────────
    eng.process_chevron(
        title='Founder-led sales prove unit economics before any paid acquisition',
        steps=[
            ('1', '0–10',
                  'Direct sales to known academies; hands-on onboarding; validate pricing'),
            ('2', '10–30',
                  'League referrals in same city; structured onboarding playbook'),
            ('3', '30–100',
                  'Sales hire + implementation runbook; expand to 2nd country'),
        ],
        source='Source: founder GTM plan, 2026',
    )

    # ── 8. Timeline — roadmap (PROCESS VISUAL) ────────────────────────────
    eng.timeline(
        title='Path to 200 academies and Series A in 24 months',
        milestones=[
            ('0–3 mo',  'MVP live — 10 paying academies'),
            ('3–9 mo',  '40 academies — pricing validated'),
            ('9–18 mo', '120 academies — 2 countries'),
            ('Y2',      '200+ — Series A'),
        ],
        source='Source: founder execution plan, 2026',
    )

    # ── 9. Action items — the ask ─────────────────────────────────────────
    eng.action_items(
        title='Seeking $1.2M seed to fund MVP completion and 30-academy beachhead',
        actions=[
            ('Close $1.2M seed',
             'By 2026-07-31',
             'Lead + 2 angels at $8M post-money cap',
             'Founders'),
            ('Hit 30 paying academies',
             'By 2027-Q1',
             '$10K MRR · 90% gross retention · validated SINPE/OXXO rails',
             'Sales + CS'),
            ('Series A milestone',
             'By 2028-Q2',
             '200+ academies · $80K MRR · 2 LATAM countries live',
             'Whole team'),
        ],
        source='Source: financial model v3, May 2026',
    )

    # ── 10. Closing ───────────────────────────────────────────────────────
    eng.closing(
        title='Northwind sports academies',
        message='Every grassroots sports academy deserves enterprise-grade software',
    )

    eng.save(str(DECK_PATH))
    print(f"[render] saved {DECK_PATH}")


def run_render_gate() -> bool:
    print("[gate] running gate_check_render.py …")
    result = subprocess.run(
        [sys.executable, str(GATE_RENDER_SCRIPT), str(DECK_PATH), str(PROJECT_DIR)],
        cwd=str(SKILL_ROOT),
    )
    return result.returncode == 0


def main() -> int:
    print("=" * 70)
    print("  MBB PPT Generator — pitch deck example (visual variety)")
    print(f"  Project dir: {PROJECT_DIR.relative_to(SKILL_ROOT)}")
    print("=" * 70)

    render_deck()
    if not run_render_gate():
        print(f"\n❌ Render gate FAILED. See {GATE_RENDER}.")
        return 1

    render_result = json.loads(GATE_RENDER.read_text())
    print()
    print("=" * 70)
    if render_result.get("passed"):
        score = render_result.get("overall_score", "?")
        ue = render_result.get("checklist", {}).get("user_code_errors", "?")
        eb = render_result.get("checklist", {}).get("engine_bug_errors", "?")
        wn = render_result.get("checklist", {}).get("warnings", "?")
        print(f"  ✅ DELIVERED — {DECK_PATH}")
        print(f"     score: {score}/100")
        print(f"     user_code_errors: {ue}   (whitelisted engine_bug_errors: {eb})")
        print(f"     warnings: {wn}")
    else:
        print("  ❌ NOT DELIVERED — gate failed")
    print("=" * 70)

    return 0 if render_result.get("passed") else 1


if __name__ == "__main__":
    sys.exit(main())
