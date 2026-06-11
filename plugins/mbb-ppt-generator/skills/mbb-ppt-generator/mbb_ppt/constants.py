# Copyright 2024-2026 Kaku Li (https://github.com/likaku)
# Licensed under the Apache License, Version 2.0 — see LICENSE and NOTICE.
# Originally from "Mck-ppt-design-skill"; bundled in mbb-ppt-generator
# NOTICE: This file must be retained in all copies or substantial portions.
#
# Adapted 2026 by albertojb for "MBB PPT Generator":
#   - Heading font changed from Georgia (transitional serif) to DM Sans (modern
#     neutral sans-serif), with a Calibri fallback for systems without DM Sans.
#   - Primary color changed from McKinsey-style navy (#051C2C) to a sober
#     forest green (#1B4332). The constant `NAVY` is retained as the canonical
#     primary-color name (its value is forest green); `PRIMARY` is provided
#     as a synonym for code that prefers a brand-neutral identifier.
#   - Accent palette retuned to muted earth tones (slate, olive, rust,
#     burgundy) for a sober non-consulting aesthetic.
#   - Added HEADING_ACCENT, SECTION_BG, and warm-palette colors.
#   - Added content-area boundary (Rule 15), page-number lock (Rule 18),
#     and guard-rail constants (Rules 11, 13, 14, 16, 17).
#   - FONT_EA retained for backward compatibility but defaults to a Latin
#     font; CJK rendering is no longer a feature of this skill.
"""Design system — color palette, typography, layout constants, and guard rails."""
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor

# ═══════════════════════════════════════════
# COLOR PALETTE — primary
# ═══════════════════════════════════════════
# `NAVY` is the canonical primary-color name (kept for engine compatibility).
# Its actual value is forest green (#1B4332): deep, sober, suitable for
# executive decks on white backgrounds. `PRIMARY` is a brand-neutral synonym.

PRIMARY    = RGBColor(0x1B, 0x43, 0x32)   # forest green — primary brand color
NAVY       = PRIMARY                       # alias retained for engine compatibility

BLACK      = RGBColor(0x00, 0x00, 0x00)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)

DARK_GRAY  = RGBColor(0x33, 0x33, 0x33)
MED_GRAY   = RGBColor(0x66, 0x66, 0x66)
LINE_GRAY  = RGBColor(0xCC, 0xCC, 0xCC)
BG_GRAY    = RGBColor(0xF2, 0xF2, 0xF2)

# ═══════════════════════════════════════════
# COLOR PALETTE — accent (≥3 parallel items)
# ═══════════════════════════════════════════
# Muted earth tones — slate, olive, rust, burgundy. Use only when ≥3 parallel
# items need differentiation. Never replace `PRIMARY`/`NAVY` as the anchor.

ACCENT_BLUE   = RGBColor(0x3B, 0x56, 0x70)   # slate blue
ACCENT_GREEN  = RGBColor(0x6B, 0x8E, 0x4E)   # olive — distinct from forest primary
ACCENT_ORANGE = RGBColor(0xA0, 0x52, 0x2D)   # rust / terracotta
ACCENT_RED    = RGBColor(0x8B, 0x26, 0x35)   # burgundy

LIGHT_BLUE    = RGBColor(0xE8, 0xED, 0xF2)
LIGHT_GREEN   = RGBColor(0xEF, 0xF2, 0xE8)
LIGHT_ORANGE  = RGBColor(0xF4, 0xE8, 0xDC)
LIGHT_RED     = RGBColor(0xF2, 0xE2, 0xE5)

ACCENT_PAIRS = [
    (ACCENT_BLUE,   LIGHT_BLUE),
    (ACCENT_GREEN,  LIGHT_GREEN),
    (ACCENT_ORANGE, LIGHT_ORANGE),
    (ACCENT_RED,    LIGHT_RED),
]

# ═══════════════════════════════════════════
# COLOR PALETTE — additions
# ═══════════════════════════════════════════

# HEADING_ACCENT is an alias of PRIMARY, named for cover titles and large
# display text where the semantic role is "heading emphasis".
HEADING_ACCENT = PRIMARY

# Lighter neutral than BG_GRAY for section dividers that need to feel
# airier without losing tonal anchoring.
SECTION_BG     = RGBColor(0xF7, 0xF7, 0xF7)

# Optional warm palette — heritage / philanthropic / hospitality decks.
# Do not mix warm and primary accents on the same slide.
WARM_NAVY      = RGBColor(0x1A, 0x2E, 0x44)
WARM_GOLD      = RGBColor(0xB8, 0x86, 0x0B)
WARM_STONE     = RGBColor(0x8B, 0x73, 0x55)

# ═══════════════════════════════════════════
# SLIDE DIMENSIONS
# ═══════════════════════════════════════════

SW = Inches(13.333)  # Slide width (16:9)
SH = Inches(7.5)     # Slide height
LM = Inches(0.8)     # Left margin
RM = Inches(0.8)     # Right margin
CW = Inches(11.733)  # Content width = SW - LM - RM

# ═══════════════════════════════════════════
# VERTICAL GRID
# ═══════════════════════════════════════════

TITLE_TOP       = Inches(0.15)   # Action title top
TITLE_H         = Inches(0.9)    # Action title height
TITLE_LINE_Y    = Inches(1.05)   # Separator under title
CONTENT_TOP     = Inches(1.3)    # Content area start
SOURCE_Y        = Inches(7.05)   # Source attribution line
PAGE_NUM_X      = Inches(12.2)   # Page number left (legacy; use PAGE_NUM_LEFT below)
BOTTOM_BAR_Y    = Inches(6.2)    # Default bottom summary bar
BOTTOM_BAR_H    = Inches(0.65)   # Bottom bar height

# ═══════════════════════════════════════════
# LEGACY 4:3-ERA CONSTANTS (unused — kept for import compatibility)
# ═══════════════════════════════════════════
# These values predate the 16:9 canvas and are NOT what the engine or the
# render gate enforce. Rule 15 (element containment) is enforced by
# mbb_ppt/qa.py against the actual slide bounds (SAFE_RIGHT = SW,
# SAFE_BOTTOM = SH). Rule 18 (page-number lock) is enforced by
# core.add_page_number() at PAGE_NUM_X (12.2") / 7.1". Do not use the
# constants below in new code; they survive only so that any external
# script importing them does not break.

CONTENT_LEFT   = Inches(0.5)
CONTENT_TOP_BOUND   = Inches(1.1)
CONTENT_RIGHT  = Inches(9.5)
CONTENT_BOTTOM = Inches(6.9)

PAGE_NUM_LEFT   = Inches(9.3)
PAGE_NUM_TOP    = Inches(7.05)
PAGE_NUM_WIDTH  = Inches(0.5)
PAGE_NUM_HEIGHT = Inches(0.25)

# ═══════════════════════════════════════════
# TYPOGRAPHY
# ═══════════════════════════════════════════

COVER_TITLE_SIZE    = Pt(44)
SECTION_TITLE_SIZE  = Pt(28)
COVER_SUBTITLE_SIZE = Pt(24)
ACTION_TITLE_SIZE   = Pt(22)
SUB_HEADER_SIZE     = Pt(18)
EMPHASIS_SIZE       = Pt(16)
BODY_SIZE           = Pt(14)
SMALL_SIZE          = Pt(12)
FOOTNOTE_SIZE       = Pt(9)

# Heading and big-text font.
#   Preferred: DM Sans (free, SIL OFL — https://fonts.google.com/specimen/DM+Sans)
#   Equivalent: Inter (also free)
#   Fallback:   Calibri (universal on Windows/macOS)
# PowerPoint uses the explicit fallback chain when DM Sans is not installed.
HEADING_FONT  = "DM Sans"

# Body text. Universal availability across Windows, macOS, and Office.
BODY_FONT     = "Arial"

# Source / footnote text.
SOURCE_FONT   = "Arial"

# ── Backwards-compatible aliases ──────────────────────────────────────
# Engine code imports these older names; they now resolve to the new
# typography. Update call sites at leisure.
FONT_HEADER   = HEADING_FONT
FONT_BODY     = BODY_FONT
# FONT_EA: this skill is English-only. CJK rendering is no longer
# supported. The constant is kept so set_ea_font(run, FONT_EA) calls in
# core.py do not crash; the value points at a Latin font that PowerPoint
# will treat as a no-op for Latin text runs.
FONT_EA       = "Arial"

# ═══════════════════════════════════════════
# GUARD-RAIL CONSTANTS (Rules 11, 13, 14, 16, 17)
# ═══════════════════════════════════════════

# Rule 11: minimum text-box height multiplier (line-height factor).
TEXTBOX_LINE_HEIGHT_FACTOR = 1.4

# Rule 13: minimum font size when auto_size shrinkage is enabled.
AUTO_SIZE_FONT_FLOOR = Pt(9)

# Rule 14: maximum action-title length in characters before truncation.
ACTION_TITLE_MAX_CHARS = 120

# Rule 16: minimum vertical gap between adjacent content elements.
INTER_ELEMENT_GAP_MIN = Inches(0.1)

# Rule 17: minimum height for an insight bar or footnote area.
INSIGHT_BAR_HEIGHT_MIN = Inches(0.4)
