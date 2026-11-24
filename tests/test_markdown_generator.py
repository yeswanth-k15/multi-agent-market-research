
from services.markdown_generator import MarkdownReportGenerator


def test_markdown_report_generation(tmp_path):
    """Verify Markdown report creation and content."""

    output_path = tmp_path / "market_report.md"

    generator = MarkdownReportGenerator(
        output_path=str(output_path)
    )

    content = """
## Executive Summary

The technology market is growing.

## Financial Analysis

Revenue increased by 15%.
"""

    result = generator.generate(
        query="Technology Market Analysis",
        content=content,
    )

    assert result.exists()

    report = result.read_text(encoding="utf-8")

    assert "# Market Research Report" in report
    assert "Technology Market Analysis" in report
    assert "Executive Summary" in report
    assert "Financial Analysis" in report
    assert "Revenue increased by 15%" in report
