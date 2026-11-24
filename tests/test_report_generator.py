
from pathlib import Path

from pypdf import PdfReader

from services.report_generator import MarketReportGenerator


def test_pdf_report_generation(tmp_path):
    """Verify that a valid PDF report is generated."""

    pdf_path = tmp_path / "test_report.pdf"

    generator = MarketReportGenerator(
        output_path=str(pdf_path)
    )

    content = """
# Executive Summary

This is a sample market research report.

## Market Overview

The technology sector is growing.

## Key Findings

- Revenue growth
- Market expansion
- Competitive developments
"""

    result = generator.generate(
        query="Technology Market Analysis",
        markdown_content=content,
    )

    assert result.exists()
    assert result.stat().st_size > 0

    reader = PdfReader(str(result))

    assert len(reader.pages) >= 1

    extracted_text = "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )

    assert "MARKET RESEARCH REPORT" in extracted_text
    assert "Executive Summary" in extracted_text
    assert "Market Overview" in extracted_text

def test_pdf_includes_markdown_table(tmp_path):
    """Verify Markdown table content appears in the PDF."""

    pdf_path = tmp_path / "financial_report.pdf"

    generator = MarketReportGenerator(
        output_path=str(pdf_path)
    )

    content = """
## Financial Summary

| Metric | Revenue | Profit |
|---|---:|---:|
| Mean | 180000 | 52000 |
| Minimum | 120000 | 30000 |
| Maximum | 250000 | 75000 |
"""

    result = generator.generate(
        query="Technology Financial Analysis",
        markdown_content=content,
    )

    reader = PdfReader(str(result))

    extracted_text = "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )

    assert "Financial Summary" in extracted_text
    assert "Revenue" in extracted_text
    assert "180000" in extracted_text
    assert "52000" in extracted_text
