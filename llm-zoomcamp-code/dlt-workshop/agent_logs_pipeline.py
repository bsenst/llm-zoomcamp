import json
import os
from typing import Iterator

import dlt
import requests


BASE_URL = "https://test-agent-traces-api-xt2e7ottma-ew.a.run.app"


def normalize_log_entry(payload: dict) -> dict:
    message = payload.get("message") or {}
    content = message.get("content") or []
    text_parts = []

    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text = item.get("text")
                if isinstance(text, str):
                    text_parts.append(text)
    elif isinstance(content, str):
        text_parts.append(content)

    usage = payload.get("usage") or {}
    return {
        "index": payload.get("index"),
        "uuid": payload.get("uuid"),
        "parent_uuid": payload.get("parentUuid"),
        "session_id": payload.get("sessionId"),
        "type": payload.get("type"),
        "timestamp": payload.get("timestamp"),
        "cwd": payload.get("cwd"),
        "git_branch": payload.get("gitBranch"),
        "version": payload.get("version"),
        "message_role": message.get("role"),
        "message_text": "\n".join(text_parts),
        "model": (message.get("model") or payload.get("model")),
        "stop_reason": payload.get("stop_reason"),
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "raw_payload": json.dumps(payload, sort_keys=True),
    }


@dlt.resource(table_name="agent_logs", max_table_nesting=0)
def agent_logs(limit: int = 1000, offset: int = 0) -> Iterator[dict]:
    page_size = min(limit, 1000)
    current_offset = offset
    total_fetched = 0

    while total_fetched < limit:
        url = f"{BASE_URL}/logs?offset={current_offset}&limit={page_size}"
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        payload = response.json()

        logs = payload.get("logs") or []
        if not logs:
            break

        for item in logs:
            yield normalize_log_entry(item)
            total_fetched += 1
            if total_fetched >= limit:
                break

        if payload.get("next_offset") is None:
            break
        current_offset = payload["next_offset"]


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="agent_logs_pipeline",
        dataset_name="agent_logs",
        destination="duckdb",
    )
    limit = int(os.getenv("AGENT_LOGS_LIMIT", "20000"))
    info = pipeline.run(agent_logs(limit=limit))
    print(info)
