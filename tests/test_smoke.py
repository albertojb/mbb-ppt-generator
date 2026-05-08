"""Smoke tests — verify the package imports cleanly and the engine produces
a valid .pptx end-to-end. Run after installation to confirm setup."""
from __future__ import annotations
import os
import zipfile
from pathlib import Path


def test_package_imports():
    """Engine, constants, and gate-supporting class all import without error."""
    from mbb_ppt import MbbEngine, __version__
    from mbb_ppt.constants import (
        HEADING_FONT, BODY_FONT, NAVY, ACCENT_BLUE,
        CONTENT_LEFT, CONTENT_RIGHT, ACTION_TITLE_MAX_CHARS,
    )
    from mbb_ppt.qa import PptQA

    assert __version__ == "0.4.2"
    assert HEADING_FONT == "DM Sans"
    assert BODY_FONT == "Arial"
    assert ACTION_TITLE_MAX_CHARS == 120


def test_engine_renders_minimal_deck(tmp_project_dir: Path):
    """A 3-slide deck saves to a non-empty .pptx file."""
    from mbb_ppt import MbbEngine

    eng = MbbEngine(total_slides=3)
    eng.cover(title="Smoke test", subtitle="Engine import + render")
    eng.executive_summary(
        title="The engine produces a valid .pptx end-to-end",
        headline="Smoke test verifies install + render",
        items=[
            ("1", "Imports work", "All public symbols resolve from mbb_ppt"),
            ("2", "Constants present", "HEADING_FONT and friends are accessible"),
            ("3", "Render succeeds", "save() produces a non-empty .pptx file"),
        ],
        source="Source: smoke test",
    )
    eng.closing(title="Done", message="Smoke test complete")

    out = tmp_project_dir / "deck.pptx"
    eng.save(str(out))

    assert out.exists(), f"Engine did not produce output at {out}"
    assert out.stat().st_size > 5_000, "Output .pptx is suspiciously small"


def test_pptx_is_valid_zip(tmp_project_dir: Path):
    """The saved file is a well-formed OOXML zip with the expected internals."""
    from mbb_ppt import MbbEngine

    eng = MbbEngine(total_slides=2)
    eng.cover(title="Zip integrity test")
    eng.closing(title="Done")

    out = tmp_project_dir / "deck.pptx"
    eng.save(str(out))

    # OOXML / .pptx is a zip file — verify it opens and contains expected parts.
    with zipfile.ZipFile(str(out)) as z:
        names = z.namelist()
        assert "[Content_Types].xml" in names, "Missing OOXML content types"
        assert any(n.startswith("ppt/slides/slide") for n in names), \
            "No slide parts found inside .pptx"
        assert any(n.startswith("ppt/theme/theme") for n in names), \
            "No theme parts found inside .pptx"


def test_full_cleanup_strips_pstyle(tmp_project_dir: Path):
    """eng.save() should remove p:style elements (theme effect leaks)."""
    from mbb_ppt import MbbEngine

    eng = MbbEngine(total_slides=2)
    eng.cover(title="Cleanup test")
    eng.closing(title="Done")

    out = tmp_project_dir / "deck.pptx"
    eng.save(str(out))

    with zipfile.ZipFile(str(out)) as z:
        for name in z.namelist():
            if name.endswith(".xml"):
                content = z.read(name).decode("utf-8", errors="ignore")
                # full_cleanup() strips <p:style> from shapes
                # We check the root-level slide files; theme files may legitimately have <a:style>
                if "ppt/slides/slide" in name:
                    assert "<p:style>" not in content, \
                        f"<p:style> leaked into {name} — full_cleanup() failed"
