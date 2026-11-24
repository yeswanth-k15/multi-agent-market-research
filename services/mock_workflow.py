
from datetime import datetime


def generate_mock_report(query: str) -> str:
    """
    Simulate the output of the three market research agents.

    This mode does not call OpenAI or execute CrewAI agents.
    All findings are illustrative and must not be treated as
    verified market research.
    """

    generated_at = datetime.now().strftime(
        "%d %B %Y, %H:%M"
    )

    return f"""# MOCK MODE - SIMULATED MARKET RESEARCH

> **Important:** This report was generated using mock responses.
> It does not contain verified live market research or financial findings.

## Executive Summary

This simulated report demonstrates how the multi-agent
market research system organizes information about:

**Research Topic:** {query}

The simulated research workflow contains three stages:

1. Lead Researcher: Identifies relevant market research areas.
2. Financial Analyst: Demonstrates financial data interpretation.
3. Technical Writer: Organizes the findings into a report.

## Market Overview

The following topics are included as illustrative research areas:

- Market size and growth trends
- Major technology companies
- Emerging technologies
- Industry developments
- Competitive landscape

No live market claims have been verified in this mock execution.

## Company Analysis

The simulated research identifies the following companies
as examples for a technology-sector analysis:

| Company | Research Area |
|---|---|
| Microsoft | Cloud computing and AI |
| Alphabet | Digital advertising and AI |
| Amazon | Cloud infrastructure and e-commerce |
| NVIDIA | AI chips and accelerated computing |

These are illustrative research targets, not findings
from a completed live research process.

## Financial Analysis

The Financial Analyst demonstrates the statistical
analysis workflow using the project's sample CSV dataset.

| Metric | Revenue | Profit | Expenses |
|---|---:|---:|---:|
| Mean | 180000 | 52000 | 128000 |
| Minimum | 120000 | 30000 | 90000 |
| Maximum | 250000 | 75000 | 175000 |

**Note:** These values come from the sample dataset.
They do not represent the actual financial results of
the companies mentioned in this report.

## Competitive Landscape

The simulated analysis considers these comparison dimensions:

- Revenue and profitability
- Product innovation
- Cloud and AI capabilities
- Market positioning
- Business risks

Actual competitor rankings have not been calculated.

## Key Findings

1. The report structure can organize company and market information.
2. Pandas can calculate financial summary statistics from CSV data.
3. The PDF and Markdown generators can format the final report.
4. Live research and LLM-generated analysis require real API execution.

## Risks and Limitations

- No OpenAI LLM calls were made.
- No live market research was performed.
- Sample financial data is illustrative.
- No investment recommendations should be inferred.

## Conclusion

The mock execution demonstrates the report-generation
pipeline for the research topic: **{query}**.

**Generation Time:** {generated_at}

**Execution Mode:** MOCK - NOT LIVE RESEARCH
"""
