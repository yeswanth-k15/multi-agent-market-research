
from datetime import datetime
from pathlib import Path


class MarkdownReportGenerator:
    """Generate Markdown market research reports."""

    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def generate(self, query: str, content: str) -> Path:
        """Create a Markdown report."""

        report = f"""# Market Research Report

**Research Topic:** {query}

**Generated:** {datetime.now().strftime("%d %B %Y, %H:%M")}

**Prepared By:** Multi-Agent Market Research System

---

{content}

---

*This report was generated using a multi-agent market research workflow.*
"""

        self.output_path.write_text(
            report,
            encoding="utf-8",
        )

        return self.output_path
