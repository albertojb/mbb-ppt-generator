"""Layout tests — exercise a representative sample of layouts from each
family to confirm they render without error."""
from __future__ import annotations
from pathlib import Path


def test_structure_layouts(tmp_project_dir: Path):
    """cover, toc, section_divider, closing, appendix_title."""
    from mck_ppt import MckEngine

    eng = MckEngine(total_slides=5)
    eng.cover(title="Structure test")
    eng.toc(items=[
        ("1", "Section one", "First topic preview"),
        ("2", "Section two", "Second topic preview"),
    ])
    eng.section_divider(section_label="01", title="A new section",
                        subtitle="What this section covers")
    eng.appendix_title(title="Appendix", subtitle="Supporting analysis")
    eng.closing(title="Done", message="Structure test complete")

    out = tmp_project_dir / "structure.pptx"
    eng.save(str(out))
    assert out.stat().st_size > 5_000


def test_data_layouts(tmp_project_dir: Path):
    """big_number, two_stat, three_stat, data_table, metric_cards, table_insight."""
    from mck_ppt import MckEngine
    from mck_ppt.constants import NAVY, ACCENT_BLUE, ACCENT_GREEN

    eng = MckEngine(total_slides=7)
    eng.cover(title="Data layouts test")

    eng.big_number(
        title="Big number test slide",
        number="+12%",
        unit="growth",
        description="Headline statistic",
        source="Source: test",
    )

    eng.two_stat(
        title="Two stat test",
        stats=[("+18%", "Growth", True), ("-2pp", "Margin", False)],
        source="Source: test",
    )

    eng.three_stat(
        title="Three stat test",
        stats=[
            ("+12%", "Revenue", True),
            ("31%",  "Margin",  False),
            ("+8",   "NPS",     True),
        ],
        source="Source: test",
    )

    eng.data_table(
        title="Data table test",
        headers=["Item", "Value", "Note"],
        rows=[
            ["Row A", "100", "First"],
            ["Row B", "200", "Second"],
        ],
        source="Source: test",
    )

    eng.metric_cards(
        title="Metric cards test",
        cards=[
            ("1", "Card one", "First card description"),
            ("2", "Card two", "Second card description"),
            ("3", "Card three", "Third card description"),
        ],
        source="Source: test",
    )

    eng.table_insight(
        title="Table insight test",
        headers=["Action", "Mechanism", "Impact"],
        rows=[
            ["Action A", "Mechanism A", "+12%"],
            ["Action B", "Mechanism B", "+8%"],
        ],
        insights=[
            "First insight statement.",
            "Second insight statement.",
        ],
        source="Source: test",
    )

    eng.closing(title="Done")

    out = tmp_project_dir / "data.pptx"
    eng.save(str(out))
    assert out.stat().st_size > 10_000


def test_chart_layouts(tmp_project_dir: Path):
    """donut, grouped_bar, horizontal_bar."""
    from mck_ppt import MckEngine
    from mck_ppt.constants import NAVY, ACCENT_BLUE, ACCENT_GREEN, MED_GRAY

    eng = MckEngine(total_slides=4)
    eng.cover(title="Chart layouts test")

    eng.donut(
        title="Donut test",
        segments=[
            (0.42, NAVY,         "Premium"),
            (0.31, ACCENT_BLUE,  "Standard"),
            (0.27, ACCENT_GREEN, "Entry"),
        ],
        center_label="42%",
        source="Source: test",
    )

    eng.grouped_bar(
        title="Grouped bar test",
        categories=["Q1", "Q2", "Q3", "Q4"],
        series=[("A", NAVY), ("B", ACCENT_BLUE)],
        data=[[100, 80], [120, 95], [140, 110], [160, 125]],
        source="Source: test",
    )

    eng.horizontal_bar(
        title="Horizontal bar test",
        items=[
            ("Top item", 80, NAVY),
            ("Mid item", 50, ACCENT_BLUE),
            ("Low item", 30, MED_GRAY),
        ],
        source="Source: test",
    )

    out = tmp_project_dir / "charts.pptx"
    eng.save(str(out))
    assert out.stat().st_size > 5_000


def test_storyline_builds(tmp_project_dir: Path):
    """The bundled 12-slide storyline builds end-to-end via DeckBuilder."""
    from mck_ppt.deck_builder import DeckBuilder
    from mck_ppt.storylines import ai_enterprise

    out = tmp_project_dir / "storyline.pptx"
    DeckBuilder.build(ai_enterprise.STORYLINE, str(out))

    assert out.exists()
    assert out.stat().st_size > 30_000, \
        "12-slide storyline should be larger than 30KB"
    assert len(ai_enterprise.STORYLINE) == 12, \
        "Storyline should have exactly 12 slides"


def test_retired_layouts_still_callable(tmp_project_dir: Path):
    """venn, cycle, funnel, pie, gauge — retired but back-compat callable."""
    from mck_ppt import MckEngine
    from mck_ppt.constants import NAVY, ACCENT_BLUE, ACCENT_GREEN

    # Just verify the methods exist on the class — don't render them
    # (they're deprecated and not promoted in new decks).
    eng = MckEngine(total_slides=1)
    assert hasattr(eng, "venn")
    assert hasattr(eng, "cycle")
    assert hasattr(eng, "funnel")
    assert hasattr(eng, "pie")
    assert hasattr(eng, "gauge")
