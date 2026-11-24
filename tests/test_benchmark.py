
import json

from services.benchmark import BenchmarkTracker


def test_benchmark_json_generation(tmp_path):
    """Verify benchmark data is saved correctly."""

    output_path = tmp_path / "benchmarks.json"

    tracker = BenchmarkTracker(
        output_path=str(output_path)
    )

    tracker.start()

    tracker.record_task(
        task_name="Market Research",
        agent_name="Market Research Specialist",
        status="completed",
    )

    tracker.record_task(
        task_name="Financial Analysis",
        agent_name="Financial Data Analyst",
        status="completed",
    )

    tracker.stop()

    result = tracker.save(
        query="Technology Market Analysis"
    )

    assert result.exists()

    data = json.loads(
        result.read_text(encoding="utf-8")
    )

    assert data["query"] == "Technology Market Analysis"
    assert data["total_tasks"] == 2
    assert data["execution_time_seconds"] >= 0

    assert len(data["task_routing_history"]) == 2

    assert (
        data["task_routing_history"][0]["assigned_agent"]
        == "Market Research Specialist"
    )
