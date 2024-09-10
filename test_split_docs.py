import unittest
from docsum import split_docs, find_split_point


class TestSplitDocs(unittest.TestCase):

    def test_find_split_point(self):
        text = "Line one.\nLine two.\nLine three."
        separators = [r"\n"]
        split_point = find_split_point(text, 15, separators)
        self.assertEqual(split_point, 9)  # The first newline is at index 9

    def test_split_on_newline(self):
        text = "Line one.\nLine two.\nLine three."
        result = split_docs(text, max_length=15)  # Reduce the max_length to force a split
        print(result)  # Debug output to see the chunks
        self.assertEqual(len(result), 2)  # Expecting two chunks
        self.assertTrue(result[0].endswith("Line two."))  # First chunk should end here
        self.assertTrue(result[1].startswith("Line three."))  # Second chunk should start here

    def test_split_on_period(self):
        text = "This is sentence one. This is sentence two. This is sentence three."
        result = split_docs(text, max_length=40)
        self.assertEqual(len(result), 2)
        self.assertTrue(result[0].endswith("sentence two."))
        self.assertTrue(result[1].startswith("This is sentence three."))

    def test_no_split_small_text(self):
        text = "This text is under the limit."
        result = split_docs(text, max_length=100)
        self.assertEqual(len(result), 1)  # No split should occur
        self.assertEqual(result[0], text)  # The text should remain unchanged

    def test_no_separator_found(self):
        text = "This text has no special separators and is very long" * 50
        result = split_docs(text, max_length=100)
        self.assertGreater(len(result), 1)  # The text should be split
        self.assertTrue(all(len(chunk) <= 100 for chunk in result))  # All chunks should be within the max_length


if __name__ == '__main__':
    unittest.main()
