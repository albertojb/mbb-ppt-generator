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


def test_content_gate_catches_visual_density_floor(project_root: Path,
                                                     tmp_project_dir: Path):
    """A 7-content-slide deck with no chart/diagram/image layouts fails."""
    def text_slide(idx: int) -> dict:
        return {
            "idx": idx,
            "layout": "executive_summary",
            "title": f"Action title {idx} reasonably long for the gate",
            "headline": f"Headline phrase for slide {idx}",
            "items": [["1", "A", "Description"], ["2", "B", "Description"], ["3", "C", "Description"]],
            "source": "Source: test",
        }

    content = {
        "slides": [
            {"idx": 1, "layout": "cover", "title": "Cover"},
            *(text_slide(i) for i in range(2, 9)),  # 7 text-only content slides
            {"idx": 9, "layout": "closing", "title": "Done"},
        ]
    }
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))

    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    assert result["passed"] is False, \
        "Text-only deck of 7 content slides should fail the visual-density gate"
    categories = {item["check"] for item in result["fail_items"]}
    assert "visual_density" in categories


def test_content_gate_visual_density_passes_with_charts(project_root: Path,
                                                          tmp_project_dir: Path):
    """A 7-content-slide deck with two visual layouts passes the density gate."""
    content = {
        "slides": [
            {"idx": 1, "layout": "cover", "title": "Cover"},
            {"idx": 2, "layout": "executive_summary",
             "title": "Three actions return revenue to growth quickly",
             "headline": "Growth concentrated in two channels",
             "items": [["1", "A", "Desc"], ["2", "B", "Desc"], ["3", "C", "Desc"]],
             "source": "Source: test"},
            {"idx": 3, "layout": "horizontal_bar",
             "title": "Premium products lead the rankings clearly here",
             "items": [["A", 80], ["B", 70], ["C", 60]],
             "source": "Source: test"},
            {"idx": 4, "layout": "matrix_2x2",
             "title": "Two priorities dominate the decision space here",
             "quadrants": [["High/High", "#FFE0E0", "fast"], ["Low/High", "#E0FFE0", "wait"],
                           ["High/Low", "#FFFFE0", "cheap"], ["Low/Low", "#E0E0FF", "skip"]],
             "source": "Source: test"},
            {"idx": 5, "layout": "side_by_side",
             "title": "Two options balance speed and margin tradeoff",
             "options": [["A", "Description"], ["B", "Description"]],
             "source": "Source: test"},
            {"idx": 6, "layout": "vertical_steps",
             "title": "Three sequential steps deliver the plan",
             "steps": [["1", "A", "Description"], ["2", "B", "Description"], ["3", "C", "Description"]],
             "source": "Source: test"},
            {"idx": 7, "layout": "executive_summary",
             "title": "Bring it all together with three actions",
             "headline": "Headline phrase",
             "items": [["1", "A", "Desc"], ["2", "B", "Desc"], ["3", "C", "Desc"]],
             "source": "Source: test"},
            {"idx": 8, "layout": "four_column",
             "title": "Phased rollout in four stages over time",
             "items": [["1", "A", "Desc"], ["2", "B", "Desc"], ["3", "C", "Desc"], ["4", "D", "Desc"]],
             "source": "Source: test"},
            {"idx": 9, "layout": "closing", "title": "Done"},
        ]
    }
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))

    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    categories = {item["check"] for item in result["fail_items"]}
    assert "visual_density" not in categories, \
        f"Deck with horizontal_bar + matrix_2x2 should pass density gate; failed with: {result['fail_items']}"


def test_content_gate_visual_density_skipped_for_short_decks(project_root: Path,
                                                                tmp_project_dir: Path):
    """A 5-content-slide text-only deck does not trigger the density gate."""
    def text_slide(idx: int) -> dict:
        return {
            "idx": idx,
            "layout": "executive_summary",
            "title": f"Action title {idx} reasonably long for the gate",
            "headline": f"Headline phrase for slide {idx}",
            "items": [["1", "A", "Description"], ["2", "B", "Description"], ["3", "C", "Description"]],
            "source": "Source: test",
        }

    content = {
        "slides": [
            {"idx": 1, "layout": "cover", "title": "Cover"},
            *(text_slide(i) for i in range(2, 7)),  # only 5 content slides
            {"idx": 7, "layout": "closing", "title": "Done"},
        ]
    }
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))

    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    categories = {item["check"] for item in result["fail_items"]}
    assert "visual_density" not in categories, \
        "Deck under 6 content slides should not trigger the density gate"


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
