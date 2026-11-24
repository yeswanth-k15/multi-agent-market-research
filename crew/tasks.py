
from crewai import Task


def create_research_task(query: str) -> Task:
    """Create the market research task."""

    return Task(
        description=(
            f"Research the following market topic: {query}\n\n"
            "Find relevant companies, market trends, recent developments, "
            "financial performance, and competitor information.\n"
            "Use reliable sources and include source URLs.\n"
            "Clearly distinguish verified facts from estimates."
        ),
        expected_output=(
            "A structured market research summary containing key findings, "
            "company information, financial data, market trends, "
            "competitor insights, and source URLs."
        ),
    )


def create_analysis_task(query: str, research_task: Task) -> Task:
    """Create the financial analysis task."""

    return Task(
        context=[research_task],
        description=(
            f"Analyze financial information related to: {query}\n\n"
            "Use the Financial Data Analyzer tool to analyze "
            "data/sample_financial_data.csv when relevant.\n"
            "Calculate mean, standard deviation, minimum, and maximum "
            "for numeric columns.\n"
            "Verify numerical consistency and explain important findings."
        ),
        expected_output=(
            "A financial analysis containing available metrics, "
            "statistical summaries, numerical validation, "
            "and key financial insights."
        ),
    )


def create_writing_task(
    query: str,
    research_task: Task,
    analysis_task: Task,
) -> Task:
    """Create the final market research report task."""

    return Task(
        context=[research_task, analysis_task],
        description=(
            f"Prepare a professional market research report about: {query}\n\n"
            "Organize the report into an executive summary, market overview, "
            "company analysis, financial analysis, competitive landscape, "
            "key findings, risks, and conclusion.\n"
            "Use information provided by the research and analysis tasks.\n"
            "Do not invent financial figures or unsupported claims."
        ),
        expected_output=(
            "A complete, professional market research report in Markdown "
            "with clear headings, factual findings, financial tables "
            "where available, and source references."
        ),
    )
