import pandas as pd
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class FinancialDataInput(BaseModel):
    """Input schema for financial CSV analysis."""

    csv_path: str = Field(
        ...,
        description="Path to the financial CSV file."
    )


class FinancialDataTool(BaseTool):
    """Analyze financial data from CSV files using Pandas."""

    name: str = "Financial Data Analyzer"

    description: str = (
        "Reads a financial CSV file and calculates mean, "
        "standard deviation, minimum, and maximum for numeric columns. "
        "Returns the results as a Markdown table."
    )

    args_schema: type[BaseModel] = FinancialDataInput

    def _run(self, csv_path: str) -> str:
        file_path = Path(csv_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"CSV file not found: {file_path}"
            )

        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError("The CSV file is empty.")

        numeric_df = df.select_dtypes(include="number")

        if numeric_df.empty:
            raise ValueError("No numeric columns found.")

        summary = numeric_df.describe().loc[
            ["mean", "std", "min", "max"]
        ]

        markdown_table = summary.round(2).to_markdown()

        return (
            f"## Financial Data Summary\n\n"
            f"**Rows analyzed:** {len(df)}\n\n"
            f"**Numeric columns:** "
            f"{', '.join(numeric_df.columns)}\n\n"
            f"{markdown_table}"
        )