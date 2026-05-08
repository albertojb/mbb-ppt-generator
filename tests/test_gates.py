"""Gate-script tests — verify gate_check_content.py and gate_check_render.py
correctly classify pass/fail on representative inputs."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path


def _run_content_gate(project_root: Path, content_path: Path,
                      project_dir: Path) -> dict:
    script = project_root / "references" / "scripts" / "gate_check_content.py"
    result = subprocess.run(
        [sys.executable, str(script), str(content_path), str(project_dir)],
        capture_output=True, text=True,
    )
    out = project_dir / "gate_content.json"
    return json.loads(out.read_text())


def _run_render_gate(project_root: Path, pptx_path: Path,
                     project_dir: Path) -> dict:
    script = project_root / "references" / "scripts" / "gate_check_render.py"
    result = subprocess.run(
        [sys.executable, str(script), str(pptx_path), str(project_dir)],
        capture_output=True, text=True,
    )
    out = project_dir / "gate_render.json"
    return json.loads(out.read_text())


def test_content_gate_passes_valid_content(project_root: Path,
                                            tmp_project_dir: Path):
    """A valid content.json passes the S3 content gate."""
    content = {
        "brief": {"audience": "Test", "goal": "Test", "key_messages": ["m"]},
        "slides": [
            {"idx": 1, "layout": "cover", "title": "Test cover"},
            {
                "idx": 2,
                "layout": "table_insight",
                "title": "A perfectly conclusion-led action title for testing",
                "headers": ["A", "B", "C"],
                "rows": [["x", "y", "z"]],
                "insights": ["First insight here."],
                "source": "Source: test",
            },
            {"idx": 3, "layout": "closing", "title": "Done"},
        ],
    }
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))

    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    assert result["passed"] is True, \
        f"Valid content failed: {result['fail_items']}"


def test_content_gate_catches_short_title(project_root: Path,
                                           tmp_project_dir: Path):
    """A too-short action title fails the S3 gate."""
    content = {
        "slides": [
            {
                "idx": 1,
                "layout": "table_insight",
                "title": "Too short",   # < 10 chars triggers title_too_short
                "headers": ["A"],
                "rows": [["x"]],
                "insights": ["x"],
                "source": "Source: test",
            },
        ],
    }
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))

    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    assert result["passed"] is False
    categories = {item["check"] for item in result["fail_items"]}
    assert "title_too_short" in categories


def test_content_gate_catches_missing_source(project_root: Path,
                                              tmp_project_dir: Path):
    """A content slide without a source line fails the S3 gate."""
    content = {
        "slides": [
            {
                "idx": 1,
                "layout": "big_number",
                "title": "Missing source on a content slide test case",
                "number": "42",
                # No 'source' key — should trigger source_missing
            },
        ],
    }
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))

    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    assert result["passed"] is False
    categories = {item["check"] for item in result["fail_items"]}
    assert "source_missing" in categories


def test_content_gate_catches_donut_overcount(project_root: Path,
                                                tmp_project_dir: Path):
    """A donut with > 6 segments fails the S3 gate (chart-limits Experience 001)."""
    content = {
        "slides": [
            {
                "idx": 1,
                "layout": "donut",
                "title": "Too many segments for donut layout test case",
                "segments": [[0.15, "#NAVY", f"L{i}"] for i in range(7)],
                "source": "Source: test",
            },
        ],
    }
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))

    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    assert result["passed"] is False
    categories = {item["check"] for item in result["fail_items"]}
    assert "count" in categories


def test_render_gate_passes_clean_deck(project_root: Path,
                                        tmp_project_dir: Path):
    """A clean rendered deck passes the S4 render gate."""
    from mbb_ppt import MbbEngine

    eng = MbbEngine(total_slides=2)
    eng.cover(title="Render gate test")
    eng.closing(title="Done")

    out = tmp_project_dir / "deck.pptx"
    eng.save(str(out))

    result = _run_render_gate(project_root, out, tmp_project_dir)
    # Clean cover/closing decks always pass — no body content to overflow.
    assert result["passed"] is True
    assert result["checklist"]["user_code_errors"] == 0


def test_render_gate_handles_missing_file(project_root: Path,
                                            tmp_project_dir: Path):
    """A missing .pptx returns passed: False, not a crash."""
    fake = tmp_project_dir / "does-not-exist.pptx"
    result = _run_render_gate(project_root, fake, tmp_project_dir)
    assert result["passed"] is False
    assert "error" in result or result["verdict"].startswith("FAIL")
