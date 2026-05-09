"""Gate-script tests — verify gate_check_content.py and gate_check_render.py
correctly classify pass/fail on representative inputs."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path


def _run_content_gate(project_root: Path, content_path: Path,
                      project_dir: Path) -> dict:
    script = project_root / "plugins" / "mbb-ppt-generator" / "skills" / "mbb-ppt-generator" / "references" / "scripts" / "gate_check_content.py"
    result = subprocess.run(
        [sys.executable, str(script), str(content_path), str(project_dir)],
        capture_output=True, text=True,
    )
    out = project_dir / "gate_content.json"
    return json.loads(out.read_text())


def _run_render_gate(project_root: Path, pptx_path: Path,
                     project_dir: Path) -> dict:
    script = project_root / "plugins" / "mbb-ppt-generator" / "skills" / "mbb-ppt-generator" / "references" / "scripts" / "gate_check_render.py"
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


def test_content_gate_catches_long_oval_label_in_process_chevron(project_root: Path,
                                                                   tmp_project_dir: Path):
    """A process_chevron step with a long label fails the label_too_long check."""
    content = {
        "slides": [
            {
                "idx": 1,
                "layout": "process_chevron",
                "title": "Founder-led sales prove unit economics before scaling",
                "steps": [
                    ["Operations hub", "Phase 1", "Direct sales to known accounts"],   # bad: long label
                    ["Local-first",    "Phase 2", "Referral outreach in same city"],   # bad: long label
                    ["Mobile app",     "Phase 3", "Sales hire + playbook"],            # bad: long label
                ],
                "source": "Source: test",
            },
        ],
    }
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))

    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    assert result["passed"] is False, "Long oval labels should fail the gate"
    categories = {item["check"] for item in result["fail_items"]}
    assert "label_too_long" in categories


def test_content_gate_passes_short_oval_label_in_process_chevron(project_root: Path,
                                                                   tmp_project_dir: Path):
    """Short labels (numbers, codes) pass."""
    content = {
        "slides": [
            {
                "idx": 1,
                "layout": "process_chevron",
                "title": "Founder-led sales prove unit economics before scaling",
                "steps": [
                    ["1", "Phase 1", "Direct sales to known accounts"],
                    ["2", "Phase 2", "Referral outreach in same city"],
                    ["3", "Phase 3", "Sales hire + playbook"],
                ],
                "source": "Source: test",
            },
        ],
    }
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))
    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    cats = {item["check"] for item in result["fail_items"]}
    assert "label_too_long" not in cats


def test_content_gate_catches_long_oval_label_in_four_column(project_root: Path,
                                                               tmp_project_dir: Path):
    """four_column items[0] is the oval label too."""
    content = {
        "slides": [
            {
                "idx": 1,
                "layout": "four_column",
                "title": "Four reasons the recommendation holds together",
                "items": [
                    ["Admin", "Title", "Description"],   # bad: 5 chars
                    ["1",     "Title", "Description"],
                    ["2",     "Title", "Description"],
                    ["3",     "Title", "Description"],
                ],
                "source": "Source: test",
            },
        ],
    }
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))
    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    cats = {item["check"] for item in result["fail_items"]}
    assert "label_too_long" in cats


def test_content_gate_catches_long_oval_label_in_executive_summary(project_root: Path,
                                                                     tmp_project_dir: Path):
    """executive_summary items[0] is the oval label."""
    content = {
        "slides": [
            {
                "idx": 1,
                "layout": "executive_summary",
                "title": "Three actions return revenue to growth quickly",
                "headline": "Concentrated in two channels and one tier",
                "items": [
                    ["First!", "Action title", "Why"],   # bad: 6 chars
                    ["2",      "Action title", "Why"],
                    ["3",      "Action title", "Why"],
                ],
                "source": "Source: test",
            },
        ],
    }
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))
    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    cats = {item["check"] for item in result["fail_items"]}
    assert "label_too_long" in cats


def test_content_gate_value_chain_passes_with_long_stage_title(project_root: Path,
                                                                tmp_project_dir: Path):
    """value_chain stages[i][0] is the stage title, not the oval label.

    Regression for v0.5.0 Bug A: the gate previously enforced the 3-char oval
    rule on the user's stage_title, but the engine renders ``str(i + 1)`` in
    the oval. Long stage titles must pass.
    """
    content = {
        "slides": [
            {
                "idx": 1,
                "layout": "value_chain",
                "title": "Five-stage delivery model spans diagnose to scale",
                "stages": [
                    ["Diagnose",   "Baseline current state",       "#0F4C3A"],
                    ["Design",     "Target operating model",       "#0F4C3A"],
                    ["Build",      "Capabilities and tooling",     "#0F4C3A"],
                    ["Run",        "Steady-state operations",      "#0F4C3A"],
                    ["Scale",      "Replicate across markets",     "#0F4C3A"],
                ],
                "source": "Source: test",
            },
        ],
    }
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))
    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    cats = {item["check"] for item in result["fail_items"]}
    assert "label_too_long" not in cats, \
        "value_chain stage_title is not the oval label; should not trigger oval-budget"


def test_content_gate_numbered_list_panel_passes_with_long_item_title(project_root: Path,
                                                                       tmp_project_dir: Path):
    """numbered_list_panel items[i][0] is the item title, not the oval label.

    Regression for v0.5.0 Bug B.
    """
    content = {
        "slides": [
            {
                "idx": 1,
                "layout": "numbered_list_panel",
                "title": "Four pillars structure the operating-model rebuild",
                "items": [
                    ["Operating model",     "Redesign decision rights and forums."],
                    ["Talent and roles",    "Resize team to align with the new model."],
                    ["Systems and data",    "Consolidate two ERPs into one source of truth."],
                    ["Performance metrics", "Replace activity KPIs with outcome KPIs."],
                ],
                "source": "Source: test",
            },
        ],
    }
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))
    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    cats = {item["check"] for item in result["fail_items"]}
    assert "label_too_long" not in cats, \
        "numbered_list_panel item_title is not the oval label; should not trigger oval-budget"


def _make_slide(idx: int, layout: str) -> dict:
    """Minimal valid slide for the structural checks; used by global-cap tests."""
    return {
        "idx": idx,
        "layout": layout,
        "title": "A perfectly conclusion-led action title for testing purposes",
        "items": [["1", "T", "D"], ["2", "T", "D"], ["3", "T", "D"]],
        "headers": ["A", "B"], "rows": [["x", "y"]],
        "insights": ["Insight."],
        "source": "Source: test",
    }


def test_executive_summary_cap_fails_at_5_of_30(project_root: Path,
                                                 tmp_project_dir: Path):
    """30 content slides + 5 executive_summary → fails (>15%)."""
    slides = [_make_slide(i + 1, "executive_summary") for i in range(5)]
    # 25 visual slides — each grouped_bar with valid data — to keep density gate happy
    for i in range(5, 30):
        slides.append({
            "idx": i + 1,
            "layout": "grouped_bar",
            "title": "Action title here, long enough to pass the title check",
            "categories": ["Q1", "Q2"],
            "series": [["A", "#0F4C3A"]],
            "data": [[10], [20]],
            "source": "Source: test",
        })
    content = {"slides": slides}
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))
    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    cats = {item["check"] for item in result["fail_items"]}
    assert "executive_summary_cap" in cats, \
        "5 / 30 executive_summary should fail the 15% cap"


def test_executive_summary_cap_passes_at_4_of_30(project_root: Path,
                                                  tmp_project_dir: Path):
    """30 content slides + 4 executive_summary → passes (13.3%)."""
    slides = [_make_slide(i + 1, "executive_summary") for i in range(4)]
    for i in range(4, 30):
        slides.append({
            "idx": i + 1,
            "layout": "grouped_bar",
            "title": "Action title here, long enough to pass the title check",
            "categories": ["Q1", "Q2"],
            "series": [["A", "#0F4C3A"]],
            "data": [[10], [20]],
            "source": "Source: test",
        })
    content = {"slides": slides}
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))
    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    cats = {item["check"] for item in result["fail_items"]}
    assert "executive_summary_cap" not in cats, \
        f"4 / 30 executive_summary (13.3%) should pass the 15% cap; fails: {result['fail_items']}"


def test_visual_density_floor_scales_with_deck_size(project_root: Path,
                                                     tmp_project_dir: Path):
    """30 content slides require max(2, 30 // 4) = 7 visual layouts."""
    # 30 content slides, 6 visual → must fail (7 required)
    slides = []
    for i in range(6):
        slides.append({
            "idx": i + 1,
            "layout": "grouped_bar",
            "title": "Action title here, long enough to pass the title check",
            "categories": ["Q1"], "series": [["A", "#0F4C3A"]], "data": [[10]],
            "source": "Source: test",
        })
    for i in range(6, 30):
        slides.append({
            "idx": i + 1,
            "layout": "table_insight",
            "title": "Action title here, long enough to pass the title check",
            "headers": ["A", "B"], "rows": [["x", "y"]],
            "insights": ["Insight."],
            "source": "Source: test",
        })
    content = {"slides": slides}
    content_path = tmp_project_dir / "content.json"
    content_path.write_text(json.dumps(content))
    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    cats = {item["check"] for item in result["fail_items"]}
    assert "visual_density" in cats, \
        "30 content slides with only 6 visual layouts should fail the scaled floor"

    # Same deck, 7 visual → passes
    slides[6] = {
        "idx": 7,
        "layout": "grouped_bar",
        "title": "Action title here, long enough to pass the title check",
        "categories": ["Q1"], "series": [["A", "#0F4C3A"]], "data": [[10]],
        "source": "Source: test",
    }
    content_path.write_text(json.dumps({"slides": slides}))
    result = _run_content_gate(project_root, content_path, tmp_project_dir)
    cats = {item["check"] for item in result["fail_items"]}
    assert "visual_density" not in cats, \
        f"30 content slides with 7 visual layouts should pass; fails: {result['fail_items']}"


def test_render_gate_passes_4_option_harvey_ball_table(project_root: Path,
                                                        tmp_project_dir: Path):
    """4-option harvey_ball_table fits within content width.

    Regression for v0.5.0 Bug C: hardcoded ``c1w + 4*colw = 12.8"`` overflowed
    the 11.733" content width on every render. Now scales to fit.
    """
    from mbb_ppt import MbbEngine

    eng = MbbEngine(total_slides=2)
    eng.cover(title="Harvey ball width regression")
    eng.harvey_ball_table(
        title="Four-option vendor evaluation prefers option B",
        criteria=["Cost", "Reliability", "Scalability", "Time-to-market"],
        options=["Option A", "Option B", "Option C", "Option D"],
        scores=[
            [3, 4, 2, 1],
            [2, 4, 3, 2],
            [3, 3, 4, 2],
            [4, 3, 2, 3],
        ],
        legend_text=["○ Low", "◔ Some", "◑ Medium", "◕ High", "● Full"],
        source="Source: test",
    )

    out = tmp_project_dir / "deck.pptx"
    eng.save(str(out))

    result = _run_render_gate(project_root, out, tmp_project_dir)
    overflow_items = [
        item for item in result.get("fail_items", [])
        if "overflow" in str(item.get("check", "")).lower()
    ]
    assert not overflow_items, \
        f"4-option harvey_ball_table should not overflow; got: {overflow_items}"


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
