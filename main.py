
import argparse
import sys

from services.mock_workflow import generate_mock_report
from crew.crew import create_market_research_crew
from services.benchmark import BenchmarkTracker
from services.markdown_generator import MarkdownReportGenerator
from services.report_generator import MarketReportGenerator
from config.settings import OUTPUT_DIR, BASE_DIR



def parse_arguments():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Multi-Agent Market Research and Report Generator"
    )

    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Market research topic to investigate.",
    )

    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run with simulated agent responses without calling an LLM.",
    )

    return parser.parse_args()



def main():
    """Execute the complete market research workflow."""

    args = parse_arguments()
    query = args.query.strip()

    if not query:
        print("Error: Research query cannot be empty.")
        sys.exit(1)

    benchmark = BenchmarkTracker(
        str(BASE_DIR / "benchmarks.json")
    )

    print("\n" + "=" * 60)
    print("MULTI-AGENT MARKET RESEARCH SYSTEM")
    print("=" * 60)
    print(f"Research Topic: {query}")
    print("=" * 60 + "\n")

    benchmark.start()

    try:
        if args.mock:
            print("Starting MOCK research workflow...\n")

            report_content = generate_mock_report(query)

            benchmark.record_task(
                task_name="Simulated market research",
                agent_name="Mock Lead Researcher",
            )

            benchmark.record_task(
                task_name="Simulated financial analysis",
                agent_name="Mock Financial Analyst",
            )

            benchmark.record_task(
                task_name="Simulated report writing",
                agent_name="Mock Technical Writer",
            )

        else:
            print("Starting hierarchical research workflow...\n")

            crew = create_market_research_crew(
                query=query,
                benchmark=benchmark,
            )

            result = crew.kickoff()
            report_content = str(result)

        # Generate reports in BOTH mock and real modes.
        markdown_generator = MarkdownReportGenerator(
            str(OUTPUT_DIR / "market_report.md")
        )

        pdf_generator = MarketReportGenerator(
            str(OUTPUT_DIR / "market_report.pdf")
        )

        markdown_path = markdown_generator.generate(
            query,
            report_content,
        )

        pdf_path = pdf_generator.generate(
            query,
            report_content,
        )

        print("\nMARKET RESEARCH COMPLETED")
        print("-" * 60)
        print(f"Markdown Report: {markdown_path}")
        print(f"PDF Report: {pdf_path}")

    except Exception as exc:
        print(f"\nError during market research: {exc}")
        sys.exit(1)

    finally:
        benchmark.stop()
        benchmark.save(query)

        print(
            f"\nExecution Time: "
            f"{benchmark.execution_time} seconds"
        )
        print(
            f"Benchmark File: {benchmark.output_path}"
        )


if __name__ == "__main__":
    main()
