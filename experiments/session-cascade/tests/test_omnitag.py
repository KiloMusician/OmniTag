import unittest
from omnitag import SessionState, parse_tags, replay

class TestSessionCascade(unittest.TestCase):
    def test_deterministic_replay(self):
        events = [{"role": "user", "content": "ΞΨΩ", "tags": {"Ctx": "Review"}},
                  {"role": "assistant", "content": "done", "tags": {"Ctx": "Verified"}}]
        self.assertEqual(replay("demo", events).footer(), replay("demo", events).footer())

    def test_atomic_rejection(self):
        s = SessionState("demo")
        with self.assertRaises(ValueError):
            s.ingest("user", "hello", {"Valid": "yes", "invalid name": "no"})
        self.assertEqual(s.message_count, 0)
        self.assertEqual(s.tags, {})

    def test_unknown_tags(self):
        self.assertEqual(parse_tags("hi [New⛛{Ψ}] [Msg⛛{42}]"),
                         [("New", "Ψ"), ("Msg", "42")])

    def test_strict_rejects_prose(self):
        with self.assertRaises(ValueError):
            parse_tags("prose [Msg⛛{42}]", strict=True)

    def test_no_plaintext_retained(self):
        s = SessionState("demo")
        s.ingest("user", "private sentence")
        self.assertNotIn("private sentence", str(s.snapshot()))

    def test_last_write_wins(self):
        s = SessionState("demo")
        s.ingest("user", "first", {"Ctx": "One"})
        s.ingest("user", "second", {"Ctx": "Two"})
        self.assertEqual(s.tags["Ctx"], "Two")

    def test_unicode_footer(self):
        s = SessionState("demo")
        s.ingest("user", "Ξ", {"QM": "Ψ"})
        self.assertIn("Ψ", s.footer())

if __name__ == "__main__":
    unittest.main()
