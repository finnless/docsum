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


if __name__ == '__main__':
    unittest.main()

