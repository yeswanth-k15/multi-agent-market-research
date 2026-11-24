
from crewai import Crew, LLM, Process
from httpx2 import query

from config.settings import MODEL_NAME, MANAGER_MODEL
from crew.agents import (
    create_researcher_agent,
    create_analyst_agent,
    create_writer_agent,
)
from crew.tasks import (
    create_research_task,
    create_analysis_task,
    create_writing_task,
)
from services.benchmark import BenchmarkTracker


def create_market_research_crew(
    query: str,
    benchmark: BenchmarkTracker | None = None,
) -> Crew:
    """Create a hierarchical market research crew."""

    researcher = create_researcher_agent()
    analyst = create_analyst_agent()
    writer = create_writer_agent()

    manager_llm = LLM(
        model=f"openai/{MANAGER_MODEL}",
        temperature=0.2,
    )

    research_task = create_research_task(query)
    analysis_task = create_analysis_task(query, research_task)
    writing_task = create_writing_task(query, research_task, analysis_task)

    def task_callback(task_output):
        """Record completed task information."""

        if benchmark is None:
            return

        agent_name = getattr(
            task_output,
            "agent",
            None,
        )

        task_description = getattr(
            task_output,
            "description",
            "Completed task",
        )

        benchmark.record_task(
            task_name=str(task_description)[:100],
            agent_name=str(agent_name or "Unknown"),
            status="completed",
        )

    crew = Crew(
        name="Market Research Crew",
        agents=[
            researcher,
            analyst,
            writer,
        ],
        tasks=[
            research_task,
            analysis_task,
            writing_task,
        ],
        process=Process.hierarchical,
        manager_llm=manager_llm,
        verbose=True,
        max_rpm=10,
        task_callback=task_callback,
    )

    return crew
