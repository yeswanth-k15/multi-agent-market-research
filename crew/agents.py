from crewai import Agent

from config.settings import MODEL_NAME
from tools.web_search_tool import TavilySearchTool
from tools.financial_data_tool import FinancialDataTool


def create_researcher_agent() -> Agent:
    """Create the Lead Researcher Agent."""

    return Agent(
        role="Market Research Specialist",
        goal=(
            "Research companies, financial performance, industry trends, "
            "competitors, and market developments using reliable sources."
        ),
        backstory=(
            "You are an experienced market research specialist. "
            "You collect relevant information from credible sources, "
            "verify dates and figures, and provide source URLs."
        ),
        tools=[TavilySearchTool()],
        llm=MODEL_NAME,
        verbose=True,
        allow_delegation=False,
    )


def create_analyst_agent() -> Agent:
    """Create the Financial Data Analyst Agent."""

    return Agent(
        role="Financial Data Analyst",
        goal=(
            "Analyze financial datasets, calculate statistical metrics, "
            "identify trends, and verify numerical consistency."
        ),
        backstory=(
            "You are a detail-oriented financial data analyst skilled "
            "in Pandas, statistical analysis, financial interpretation, "
            "and data validation."
        ),
        tools=[FinancialDataTool()],
        llm=MODEL_NAME,
        verbose=True,
        allow_delegation=False,
    )


def create_writer_agent() -> Agent:
    """Create the Technical Reports Writer Agent."""

    return Agent(
        role="Technical Reports Writer",
        goal=(
            "Transform verified research and financial analysis into "
            "a professional, structured market research report."
        ),
        backstory=(
            "You are an experienced technical report writer. "
            "You communicate complex market and financial information "
            "clearly, objectively, and professionally."
        ),
        llm=MODEL_NAME,
        verbose=True,
        allow_delegation=False,
    )