import argparse
import json
import logging
import os
from pathlib import Path
from typing import Iterator

import dlt

logger = logging.getLogger(__name__)


@dlt.resource(table_name="claude_logs", max_table_nesting=0)
def claude_log_records(source_dir: str) -> Iterator[dict]:
    root = Path(source_dir)
    if not root.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")

    files_processed = 0
    records_emitted = 0

    for path in sorted(root.glob("**/*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".jsonl", ".log"}:
            continue

        files_processed += 1
        logger.info("Processing %s", path)

        try:
            with path.open("r", encoding="utf-8") as handle:
                for line_number, raw_line in enumerate(handle, start=1):
                    line = raw_line.strip()
                    if not line:
                        continue

                    try:
                        payload = json.loads(line)
                    except json.JSONDecodeError as exc:
                        logger.warning("Skipping invalid JSON in %s:%d: %s", path, line_number, exc)
                        continue

                    records_emitted += 1
                    yield {
                        "source_file": str(path),
                        "line_number": line_number,
                        "raw_json": line,
                        "parsed_json": payload,
                    }
        except (OSError, UnicodeDecodeError) as exc:
            logger.warning("Skipping unreadable file %s: %s", path, exc)

    logger.info("Finished scanning %d files; emitted %d records", files_processed, records_emitted)


def iter_claude_log_records(source_dir: str) -> list[dict]:
    return list(claude_log_records(source_dir))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="Load local Claude JSON/JSONL/log files into DuckDB")
    parser.add_argument(
        "source_dir",
        nargs="?",
        default=os.getenv("CLAUDE_LOGS_DIR", "/home/codespace/.gemini/tmp/llm-zoomcamp/chats"),
        help="Directory containing Claude log files",
    )
    args = parser.parse_args()

    pipeline = dlt.pipeline(
        pipeline_name="claude_logs_pipeline",
        dataset_name="claude_logs",
        destination="duckdb",
    )

    info = pipeline.run(claude_log_records(args.source_dir))
    print(info)
