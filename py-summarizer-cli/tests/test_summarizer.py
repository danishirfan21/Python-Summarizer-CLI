import unittest
from src.cli_tool.summarizer import split_sentences, tokenize, summarize_and_insights

class TestSummarizer(unittest.TestCase):
    def test_split_sentences(self):
        text = "Hello world. This is a test! Are you there? Yes."
        sents = split_sentences(text)
        self.assertGreaterEqual(len(sents), 4)

    def test_tokenize(self):
        text = "Hello, world! Python-3.11 isn't bad."
        toks = tokenize(text)
        self.assertIn("python", toks)
        self.assertIn("3", toks)
        self.assertTrue(any("isn" in t or "isn't" in t for t in toks))

    def test_summarize_and_insights(self):
        text = "A. B. C. D. E. F. G."
        result = summarize_and_insights(text, max_sentences=3, insights_n=3)
        self.assertIn("summary", result)
        self.assertIn("key_insights", result)
        self.assertEqual(len(result["key_insights"]), 3)
