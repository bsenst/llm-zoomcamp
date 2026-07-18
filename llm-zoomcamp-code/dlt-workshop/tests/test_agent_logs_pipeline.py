import unittest

from agent_logs_pipeline import normalize_log_entry


class AgentLogsPipelineTest(unittest.TestCase):
    def test_normalize_log_entry_extracts_message_and_usage_fields(self) -> None:
        payload = {
            "index": 7,
            "sessionId": "abc",
            "type": "assistant",
            "timestamp": "2026-01-01T00:00:00+00:00",
            "message": {
                "role": "assistant",
                "content": [{"type": "text", "text": "Let me inspect the code"}],
            },
            "usage": {"input_tokens": 12, "output_tokens": 3},
            "model": "claude-opus-4-8",
        }

        normalized = normalize_log_entry(payload)

        self.assertEqual(normalized["index"], 7)
        self.assertEqual(normalized["session_id"], "abc")
        self.assertEqual(normalized["type"], "assistant")
        self.assertEqual(normalized["message_role"], "assistant")
        self.assertEqual(normalized["message_text"], "Let me inspect the code")
        self.assertEqual(normalized["model"], "claude-opus-4-8")
        self.assertEqual(normalized["input_tokens"], 12)
        self.assertEqual(normalized["output_tokens"], 3)


if __name__ == "__main__":
    unittest.main()
