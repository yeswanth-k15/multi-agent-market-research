
import pandas as pd
import pytest

from tools.financial_data_tool import FinancialDataTool


def test_financial_data_analysis(tmp_path):
    """Verify financial statistics calculated from a CSV."""

    csv_file = tmp_path / "financial_data.csv"

    df = pd.DataFrame({
        "Company": ["A", "B", "C"],
        "Revenue": [100, 200, 300],
        "Profit": [20, 40, 60],
    })

    df.to_csv(csv_file, index=False)

    tool = FinancialDataTool()
    result = tool._run(csv_path=str(csv_file))

    assert "Financial Data Summary" in result
    assert "Revenue" in result
    assert "Profit" in result
    assert "mean" in result
    assert "max" in result


def test_missing_csv_file():
    """Verify missing CSV files raise an error."""

    tool = FinancialDataTool()

    with pytest.raises(FileNotFoundError):
        tool._run(csv_path="missing_file.csv")


def test_csv_without_numeric_columns(tmp_path):
    """Verify CSV files without numeric columns are rejected."""

    csv_file = tmp_path / "text_data.csv"

    df = pd.DataFrame({
        "Company": ["A", "B", "C"],
        "Sector": ["IT", "Finance", "Healthcare"],
    })

    df.to_csv(csv_file, index=False)

    tool = FinancialDataTool()

    with pytest.raises(ValueError):
        tool._run(csv_path=str(csv_file))
