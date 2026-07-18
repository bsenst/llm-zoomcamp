import tempfile
import unittest
from pathlib import Path

from claude_logs_pipeline import iter_claude_log_records


class ClaudeLogsPipelineTest(unittest.TestCase):
    def test_iter_claude_log_records_reads_jsonl_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source_dir = Path(tmpdir)
            sample_file = source_dir / "session.jsonl"
            sample_file.write_text(
                '{"kind": "main", "messages": []}\n'
                '{"kind": "tool", "messages": [{"text": "hi"}]}\n',
                encoding="utf-8",
            )

            rows = list(iter_claude_log_records(str(source_dir)))

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["source_file"], str(sample_file))
            self.assertEqual(rows[0]["line_number"], 1)
            self.assertEqual(rows[0]["raw_json"], '{"kind": "main", "messages": []}')


if __name__ == "__main__":
    unittest.main()
