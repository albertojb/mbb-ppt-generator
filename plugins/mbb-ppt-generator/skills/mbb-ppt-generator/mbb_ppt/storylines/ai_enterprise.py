# Copyright 2024-2026 Kaku Li (https://github.com/likaku) — original Mck-ppt-design-skill, Apache 2.0.
# Adapted 2026 for "MBB PPT Generator": original 33-slide Chinese AI-enterprise storyline
# replaced with a concise 12-slide English MBB-style strategy review template
# that demonstrates the same range of engine layouts. Module name retained for
# upstream import compatibility.
#
"""Strategy review storyline — 12-slide English template.

A working example storyline demonstrating engine variety: cover, TOC,
executive summary, big number, grouped bar, table insight, side-by-side,
donut, timeline, key takeaway, action items, and closing. Every slide passes
the S3 content gate and the S4 render gate.

Use this as a starting point — clone and edit for your own deck. The example
narrative is a fictional Q1 2026 strategy review; replace the content with
your own findings before delivering.

Usage:
    from mbb_ppt.deck_builder import DeckBuilder
    from mbb_ppt.storylines import ai_enterprise
    DeckBuilder.build(ai_enterprise.STORYLINE, 'output/strategy_review.pptx')
"""
from mbb_ppt.constants import (
    NAVY, ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED,
    LIGHT_BLUE, LIGHT_GREEN, LIGHT_ORANGE, LIGHT_RED,
    DARK_GRAY, MED_GRAY, BG_GRAY, WHITE,
)


STORYLINE = [
    # ═══════════════════════════════════════════════════════
    # SLIDE 1 — Cover
    # ═══════════════════════════════════════════════════════
    {
        'type': 'cover',
        'data': {
            'title': 'Q1 2026 strategy review',
            'subtitle': 'Three actions to return revenue to growth',
            'author': 'Strategy team',
            'date': 'March 2026',
        },
    },

    # ═══════════════════════════════════════════════════════
    # SLIDE 2 — Table of Contents
    # ═══════════════════════════════════════════════════════
    {
        'type': 'toc',
        'data': {
            'title': 'Agenda',
            'items': [
                ('1', 'Executive summary',  'The recommendation and key evidence'),
                ('2', 'Market dynamics',    'Where pressure and opportunity shift'),
                ('3', 'Strategic actions',  'Three moves to accelerate growth'),
                ('4', 'Implementation',     'Phased rollout with risk gates'),
                ('5', 'Decisions',          'What we are asking the board to approve'),
            ],
        },
    },

    # ═══════════════════════════════════════════════════════
    # SLIDE 3 — Executive Summary (the answer)
    # ═══════════════════════════════════════════════════════
    {
        'type': 'executive_summary',
        'data': {
            'title': 'Three actions return revenue to double-digit growth',
            'headline': 'Growth is concentrated in two channels and one product tier',
            'items': [
                ('1', 'Shift mix to premium',
                      'Higher margin, limited cost-to-serve impact'),
                ('2', 'Expand in two channels',
                      'Two distributors are underpenetrated relative to peers'),
                ('3', 'Fund via simplification',
                      'Back-office complexity can shrink without service hit'),
            ],
            'source': 'Source: internal analysis, Q1 2026',
        },
    },

    # ═══════════════════════════════════════════════════════
    # SLIDE 4 — Big Number (a focal stat)
    # ═══════════════════════════════════════════════════════
    {
        'type': 'big_number',
        'data': {
            'title': 'Premium tier accounts for 42% of revenue from 18% of volume',
            'number': '42%',
            'unit': 'of revenue',
            'description': 'Premium products drive disproportionate revenue '
                           'and margin contribution. Mix shift is the highest-'
                           'leverage commercial action available to us.',
            'detail_items': [
                '• Premium margin runs ~7pp above standard tier',
                '• Premium cost-to-serve is comparable; no operations penalty',
                '• Premium share has grown +3pp in the last four quarters',
            ],
            'source': 'Source: finance team, Q1 close',
        },
    },

    # ═══════════════════════════════════════════════════════
    # SLIDE 5 — Grouped Bar (data exhibit)
    # ═══════════════════════════════════════════════════════
    {
        'type': 'grouped_bar',
        'data': {
            'title': 'Premium and partner channels lead growth',
            'categories': ['Q1', 'Q2', 'Q3', 'Q4'],
            'series': [('Premium', NAVY), ('Partner', ACCENT_BLUE)],
            'data': [
                [120,  80],
                [145,  95],
                [160, 110],
                [180, 130],
            ],
            'max_val': 200,
            'summary': ('CAGR', '+14% blended over the period.'),
            'source': 'Source: finance team',
        },
    },

    # ═══════════════════════════════════════════════════════
    # SLIDE 6 — Table + Insight (editorial workhorse)
    # ═══════════════════════════════════════════════════════
    {
        'type': 'table_insight',
        'data': {
            'title': 'Three actions improve growth while protecting margin',
            'headers': ['Action', 'Mechanism', 'Impact'],
            'rows': [
                ['Premium bundles',     'Raise mix in premium',           '+12%'],
                ['Channel expansion',   'Add EMEA distributors',          '+8%'],
                ['Cost simplification', 'Reduce service overlap',         '+3pp'],
            ],
            'insights': [
                'Actions are complementary, not sequential.',
                'First two accelerate growth; the third funds execution.',
                'Each is feasible within one planning cycle.',
            ],
            'source': 'Source: strategy team',
        },
    },

    # ═══════════════════════════════════════════════════════
    # SLIDE 7 — Side-by-Side (option comparison)
    # ═══════════════════════════════════════════════════════
    {
        'type': 'side_by_side',
        'data': {
            'title': 'Premium expansion wins on margin and risk balance',
            'options': [
                ('Volume push', [
                    '• +18% revenue growth',
                    '• -2pp margin pressure',
                    '• $25M capex',
                    '• 9-month payback',
                    '• Service strain risk',
                ]),
                ('Premium expansion', [
                    '• +12% revenue growth',
                    '• +3pp margin expansion',
                    '• $12M capex',
                    '• 14-month payback',
                    '• Brand uplift',
                ]),
            ],
            'source': 'Source: option analysis',
        },
    },

    # ═══════════════════════════════════════════════════════
    # SLIDE 8 — Donut (composition)
    # ═══════════════════════════════════════════════════════
    {
        'type': 'donut',
        'data': {
            'title': 'Revenue mix today — premium leads, entry compresses',
            'segments': [
                (0.42, NAVY,         'Premium'),
                (0.31, ACCENT_BLUE,  'Standard'),
                (0.18, ACCENT_GREEN, 'Entry'),
                (0.09, MED_GRAY,     'Other'),
            ],
            'center_label': '42%',
            'center_sub': 'premium share',
            'summary': 'Premium share rose +3pp YoY; entry tier compressed.',
            'source': 'Source: finance team',
        },
    },

    # ═══════════════════════════════════════════════════════
    # SLIDE 9 — Timeline (rollout)
    # ═══════════════════════════════════════════════════════
    {
        'type': 'timeline',
        'data': {
            'title': 'A phased rollout reduces risk and accelerates learning',
            'milestones': [
                ('Q1', 'Design and prioritization'),
                ('Q2', 'Pilot launch in 2 markets'),
                ('Q3', 'Scale-up to all regions'),
                ('Q4', 'Measure and refine'),
            ],
            'source': 'Source: PMO',
        },
    },

    # ═══════════════════════════════════════════════════════
    # SLIDE 10 — Key Takeaway (synthesis)
    # ═══════════════════════════════════════════════════════
    {
        'type': 'key_takeaway',
        'data': {
            'title': 'The three actions are mutually reinforcing',
            'left_text': [
                'Premium mix shift adds margin without straining service.',
                'Channel expansion adds distribution where the premium tier sells best.',
                'Cost simplification frees capacity to support both moves.',
            ],
            'takeaways': [
                'Three complementary actions, not a sequence.',
                'Each unlocks the next without blocking it.',
                'Combined effect: +12% growth, +3pp margin.',
            ],
            'source': 'Source: synthesis from sections 2-4',
        },
    },

    # ═══════════════════════════════════════════════════════
    # SLIDE 11 — Action Items (decisions)
    # ═══════════════════════════════════════════════════════
    {
        'type': 'action_items',
        'data': {
            'title': 'Four decisions and an owner for each',
            'actions': [
                ('Decision 1', 'Q2 2026', 'Approve premium pricing test',           'CEO'),
                ('Decision 2', 'Q2-Q3',   'Allocate $20M for channel expansion',   'CFO'),
                ('Decision 3', 'Q3 2026', 'Sign EMEA distributor contracts',       'VP Sales'),
                ('Decision 4', 'Q4 2026', 'Brief board on Q3 results',             'CSO'),
            ],
            'source': 'Source: strategy team',
        },
    },

    # ═══════════════════════════════════════════════════════
    # SLIDE 12 — Closing
    # ═══════════════════════════════════════════════════════
    {
        'type': 'closing',
        'data': {
            'title': 'Thank you',
            'message': 'Discussion and decision points',
        },
    },
]
