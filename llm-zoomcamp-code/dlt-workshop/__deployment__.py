"""Deployment manifest — import the pipelines and notebooks you want to deploy and list them in __all__."""

import os
import importlib

import dlt
from dlt._workspace.deployment import pipeline_run
from dlt.hub.run import trigger

from agent_logs_pipeline import agent_logs

agent_traces_dashboard = importlib.import_module("reports.agent_logs_report")


@pipeline_run(
    "agent_logs_pipeline",
    name="agent_logs_pipeline_run",
    trigger=trigger.schedule("0 12 * * *"),
)
def run_pipeline() -> object:
    pipeline = dlt.pipeline(
        pipeline_name="agent_logs_pipeline",
        dataset_name="agent_logs",
        destination="duckdb",
    )
    return pipeline.run(
        agent_logs(limit=int(os.environ.get("AGENT_LOGS_LIMIT", "20000")))
    )


__all__: list[str] = ["run_pipeline", "agent_traces_dashboard"]
