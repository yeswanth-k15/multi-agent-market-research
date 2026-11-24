
import json
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter


class BenchmarkTracker:
    """Track workflow execution time and task routing history."""

    def __init__(self, output_path: str = "benchmarks.json"):
        self.output_path = Path(output_path)
        self.start_time = None
        self.task_history = []
        self.execution_time = 0.0

    def start(self):
        """Start measuring workflow execution time."""
        self.start_time = perf_counter()

    def record_task(
        self,
        task_name: str,
        agent_name: str,
        status: str = "completed",
    ):
        """Record task execution and agent routing."""

        self.task_history.append(
            {
                "task": task_name,
                "assigned_agent": agent_name,
                "status": status,
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
            }
        )

    def stop(self):
        """Stop the execution timer."""

        if self.start_time is not None:
            self.execution_time = round(
                perf_counter() - self.start_time,
                2,
            )

    def save(self, query: str):
        """Save benchmark information as JSON."""

        benchmark_data = {
            "query": query,
            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "execution_time_seconds": self.execution_time,
            "total_tasks": len(self.task_history),
            "task_routing_history": self.task_history,
        }

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.output_path.write_text(
            json.dumps(
                benchmark_data,
                indent=4,
            ),
            encoding="utf-8",
        )

        return self.output_path
