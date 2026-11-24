
from xml.sax.saxutils import escape
from datetime import datetime
from pathlib import Path

from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


class MarketReportGenerator:
    """Generate professional PDF market research reports."""

    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.styles = getSampleStyleSheet()

        self.styles.add(
            ParagraphStyle(
                name="ReportTitle",
                parent=self.styles["Title"],
                fontSize=22,
                leading=28,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#17365D"),
                spaceAfter=12,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="SectionHeading",
                parent=self.styles["Heading2"],
                fontSize=14,
                leading=18,
                textColor=colors.HexColor("#17365D"),
                spaceBefore=14,
                spaceAfter=8,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="ReportBody",
                parent=self.styles["BodyText"],
                fontSize=9,
                leading=14,
                spaceAfter=8,
            )
        )

    def _header_footer(self, canvas, document):
        """Draw the report header and footer."""

        canvas.saveState()

        width, height = A4

        canvas.setFillColor(colors.HexColor("#17365D"))
        canvas.rect(
            0,
            height - 8 * mm,
            width,
            8 * mm,
            fill=1,
            stroke=0,
        )

        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)

        canvas.drawString(
            20 * mm,
            12 * mm,
            "Confidential | Market Research Report",
        )

        canvas.drawRightString(
            width - 20 * mm,
            12 * mm,
            f"Page {canvas.getPageNumber()} of {self.page_count}",
        )

        canvas.restoreState()

    def _build_markdown_table(self, rows):
        """Convert Markdown table rows into a ReportLab table."""

        parsed_rows = []

        for row in rows:
            cells = [
                cell.strip()
                for cell in row.strip().strip("|").split("|")
            ]

            # Skip Markdown separator rows
            if all(
                cell
                and set(cell.replace(":", "").strip()) <= {"-"}
                for cell in cells
            ):
                continue

            parsed_rows.append(cells)

        if not parsed_rows:
            return None

        # Normalize column counts
        column_count = max(len(row) for row in parsed_rows)

        normalized_rows = [
            row + [""] * (column_count - len(row))
            for row in parsed_rows
        ]

        table_data = []

        for row_index, row in enumerate(normalized_rows):
            formatted_row = []

            for cell in row:
                safe_text = escape(cell)

                if row_index == 0:
                    safe_text = f"<b>{safe_text}</b>"

                formatted_row.append(
                    Paragraph(
                        safe_text,
                        self.styles["ReportBody"],
                    )
                )

            table_data.append(formatted_row)

        table = Table(
            table_data,
            repeatRows=1,
            hAlign="LEFT",
        )

        table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#17365D"),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ])
        )

        return table

    def generate(self, query: str, markdown_content: str) -> Path:
        """Generate a PDF report with accurate page numbering."""

        document = SimpleDocTemplate(
            str(self.output_path),
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=22 * mm,
            bottomMargin=22 * mm,
            title=f"Market Research Report - {query}",
            author="Multi-Agent Market Research System",
        )

        story = []

        story.append(
            Paragraph(
                "MARKET RESEARCH REPORT",
                self.styles["ReportTitle"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Research Topic:</b> {escape(query)}",
                self.styles["ReportBody"],
            )
        )

        story.append(
            Paragraph(
                f"<b>Generated:</b> "
                f"{datetime.now().strftime('%d %B %Y, %H:%M')}",
                self.styles["ReportBody"],
            )
        )

        story.append(Spacer(1, 10))

        lines = markdown_content.splitlines()
        index = 0

        while index < len(lines):
            line = lines[index].strip()

            if not line:
                story.append(Spacer(1, 5))
                index += 1
                continue

            # Markdown table handling
            if line.startswith("|"):
                table_rows = []

                while (
                    index < len(lines)
                    and lines[index].strip().startswith("|")
                ):
                    table_rows.append(lines[index].strip())
                    index += 1

                table = self._build_markdown_table(table_rows)

                if table:
                    story.append(Spacer(1, 6))
                    story.append(table)
                    story.append(Spacer(1, 8))

                continue

            if line.startswith("# "):
                story.append(
                    Paragraph(
                        escape(line[2:]),
                        self.styles["Heading1"],
                    )
                )

            elif line.startswith("## "):
                story.append(
                    Paragraph(
                        escape(line[3:]),
                        self.styles["SectionHeading"],
                    )
                )

            elif line.startswith("### "):
                story.append(
                    Paragraph(
                        escape(line[4:]),
                        self.styles["Heading3"],
                    )
                )

            elif line.startswith(("- ", "* ")):
                story.append(
                    Paragraph(
                        f"&bull; {escape(line[2:])}",
                        self.styles["ReportBody"],
                    )
                )

            else:
                story.append(
                    Paragraph(
                        escape(line),
                        self.styles["ReportBody"],
                    )
                )

            index += 1

        class NumberedCanvas(pdf_canvas.Canvas):
            """Canvas that adds total page count."""

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.saved_page_states = []

            def showPage(self):
                """Save the current page state before moving to the next page."""

                self.saved_page_states.append(
                    dict(self.__dict__)
                )

                self._startPage()

            def save(self):
                """Draw page numbers after calculating the total page count."""

                total_pages = len(self.saved_page_states)

                for state in self.saved_page_states:
                    self.__dict__.update(state)

                    self._header_footer(total_pages)

                    pdf_canvas.Canvas.showPage(self)

                pdf_canvas.Canvas.save(self)

            def _header_footer(self, total_pages):
                """Draw the report header and footer."""

                self.saveState()

                width, height = A4

                # Header banner
                self.setFillColor(
                    colors.HexColor("#17365D")
                )

                self.rect(
                    0,
                    height - 8 * mm,
                    width,
                    8 * mm,
                    fill=1,
                    stroke=0,
                )

                # Footer
                self.setFont("Helvetica", 8)
                self.setFillColor(colors.grey)

                self.drawString(
                    20 * mm,
                    12 * mm,
                    "Confidential | Market Research Report",
                )

                self.drawRightString(
                    width - 20 * mm,
                    12 * mm,
                    f"Page {self.getPageNumber()} of {total_pages}",
                )

                self.restoreState()

        document.build(
            story,
            canvasmaker=NumberedCanvas,
        )

        return self.output_path
