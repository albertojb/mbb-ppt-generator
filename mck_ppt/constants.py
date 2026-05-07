# Copyright 2024-2026 Kaku Li (https://github.com/likaku)
# Licensed under the Apache License, Version 2.0 — see LICENSE and NOTICE.
# Originally part of "Mck-ppt-design-skill" (McKinsey PPT Design Framework).
# NOTICE: This file must be retained in all copies or substantial portions.
#
# Adapted 2026 by albertojb for "MBB PPT Generator":
#   - Heading font changed from Georgia (transitional serif) to DM Sans (modern
#     neutral sans-serif), with a Calibri fallback for systems without DM Sans.
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

NAVY       = RGBColor(0x05, 0x1C, 0x2C)
BLACK      = RGBColor(0x00, 0x00, 0x00)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)

DARK_GRAY  = RGBColor(0x33, 0x33, 0x33)
MED_GRAY   = RGBColor(0x66, 0x66, 0x66)
LINE_GRAY  = RGBColor(0xCC, 0xCC, 0xCC)
BG_GRAY    = RGBColor(0xF2, 0xF2, 0xF2)

# ═══════════════════════════════════════════
# COLOR PALETTE — accent (≥3 parallel items)
# ═══════════════════════════════════════════

ACCENT_BLUE   = RGBColor(0x00, 0x6B, 0xA6)
ACCENT_GREEN  = RGBColor(0x00, 0x7A, 0x53)
ACCENT_ORANGE = RGBColor(0xD4, 0x6A, 0x00)
ACCENT_RED    = RGBColor(0xC6, 0x28, 0x28)

LIGHT_BLUE    = RGBColor(0xE3, 0xF2, 0xFD)
LIGHT_GREEN   = RGBColor(0xE8, 0xF5, 0xE9)
LIGHT_ORANGE  = RGBColor(0xFF, 0xF3, 0xE0)
LIGHT_RED     = RGBColor(0xFF, 0xEB, 0xEE)

ACCENT_PAIRS = [
    (ACCENT_BLUE,   LIGHT_BLUE),
    (ACCENT_GREEN,  LIGHT_GREEN),
    (ACCENT_ORANGE, LIGHT_ORANGE),
    (ACCENT_RED,    LIGHT_RED),
]

# ═══════════════════════════════════════════
# COLOR PALETTE — additions (v2.0)
# ═══════════════════════════════════════════

# HEADING_ACCENT is an alias of NAVY, named for cover titles and large
# display text where the semantic role is "heading emphasis".
HEADING_ACCENT = RGBColor(0x05, 0x1C, 0x2C)

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
# CONTENT AREA BOUNDARY (Rule 15, v2.0)
# ═══════════════════════════════════════════
# Hard bounding box for all shapes, text boxes, and charts on a content
# slide. The render gate validates placement against these limits.
#
# These are tighter than the legacy LM/RM values; the render-gate
# enforces them but engine layouts using LM/CW continue to work because
# Rule 15 governs the *outer* envelope, not internal column widths.

CONTENT_LEFT   = Inches(0.5)
CONTENT_TOP_BOUND   = Inches(1.1)
CONTENT_RIGHT  = Inches(9.5)
CONTENT_BOTTOM = Inches(6.9)

# ═══════════════════════════════════════════
# PAGE-NUMBER PLACEMENT LOCK (Rule 18, v2.0)
# ═══════════════════════════════════════════
# Page numbers must be placed at this exact position on every slide.
# Never compute dynamically.

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
# GUARD-RAIL CONSTANTS (v2.0 — Rules 11, 13, 14, 16, 17)
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
