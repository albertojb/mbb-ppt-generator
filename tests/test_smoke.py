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

    assert __version__ == "0.5.1"
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


def test_schema_covers_every_active_layout(project_root: Path):
    """references/api-schemas.yaml must list every public engine method.

    Regression for v0.5.1 — drift between the engine and the schema
    silently breaks the S3 gate's structural validation and the generated
    cheatsheet. Catch it at test time.
    """
    import inspect
    import yaml as _yaml
    from mbb_ppt import MbbEngine

    schema_path = (project_root /
                   "plugins/mbb-ppt-generator/skills/mbb-ppt-generator/"
                   "references/api-schemas.yaml")
    schema = _yaml.safe_load(schema_path.read_text())
    schema_layouts = set((schema.get("layouts") or {}).keys())

    engine_methods = {
        n for n, _ in inspect.getmembers(MbbEngine, predicate=inspect.isfunction)
        if not n.startswith("_") and n != "save"
    }

    missing = engine_methods - schema_layouts
    extra = schema_layouts - engine_methods
    assert not missing, f"Engine methods missing from api-schemas.yaml: {sorted(missing)}"
    assert not extra,   f"Schema entries with no engine method: {sorted(extra)}"

    # Every active layout should declare a family. (Retired ones may omit it.)
    families_missing = [
        name for name, lay in (schema.get("layouts") or {}).items()
        if lay.get("status", "active") == "active" and not lay.get("family")
    ]
    assert not families_missing, \
        f"Active schema entries without `family`: {families_missing}"


def test_cheatsheet_regenerates_clean(project_root: Path, tmp_path: Path):
    """`generate_cheatsheet.py` must produce a non-empty file from the current schema.

    Catches regressions where the generator can't parse the schema (bad sort
    keys, missing required fields, etc.).
    """
    import subprocess, sys
    script = (project_root /
              "plugins/mbb-ppt-generator/skills/mbb-ppt-generator/"
              "references/scripts/generate_cheatsheet.py")
    out = tmp_path / "cheatsheet.md"
    res = subprocess.run([sys.executable, str(script), str(out)],
                         capture_output=True, text=True)
    assert res.returncode == 0, f"generator failed: {res.stderr}"
    text = out.read_text()
    assert "ExecEngine — API Cheatsheet" in text
    # Sanity-check that several known active layouts appear.
    for layout in ("cover", "executive_summary", "harvey_ball_table",
                   "value_chain", "numbered_list_panel"):
        assert f"`{layout}`" in text, f"Cheatsheet missing entry for {layout}"


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
