import unittest
from docsum import split_docs, extract_text, _split_docs_with_separator

class TestSplitDocs(unittest.TestCase):

    def test_split_docs_length_simple(self):
        """
        Test that split_docs correctly splits a simple string into chunks of the specified length.

        The input text is "AAAAABBBBBCCCCC" and the chunk size is 5.
        The expected output is three chunks: ["AAAAA", "BBBBB", "CCCCC"].
        """
        text = "A" * 5 + "B" * 5 + "C" * 5
        chunks = split_docs(text, 5)
        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0], "AAAAA")
        self.assertEqual(chunks[1], "BBBBB")
        self.assertEqual(chunks[2], "CCCCC")

    def test_split_docs_length_hamlet(self):
        """
        Test that split_docs returns a string of the same length as the input when applied to the text of Hamlet.

        The input text is the content of "docs/hamlet.txt" and the chunk size is 20000.
        The test checks if the length of the joined chunks is the same as the original text.
        """
        hamlet = extract_text("docs/hamlet.txt")
        hamlet_chunks = split_docs(hamlet, 20000)
        joined_result = ''.join(hamlet_chunks)
        self.assertEqual(len(joined_result), len(hamlet))

    def test_split_docs_length_hamlet_min_length(self):
        """
        Test that split_docs on Hamlet does not result in any chunks smaller than 100 characters.

        The input text is the content of "docs/hamlet.txt" and the chunk size is 20000.
        The test checks that each chunk is greater than 100 characters in length.
        """
        hamlet = extract_text("docs/hamlet.txt")
        hamlet_chunks = split_docs(hamlet, 20000)
        for chunk in hamlet_chunks:
            self.assertGreater(len(chunk), 100)
    
    def test_split_docs_length_declaration(self):
        """
        Test that split_docs returns a string of the same length as the input when applied to the Declaration of Independence.

        The input text is the content of "docs/declaration" and the chunk size is 20000.
        The test checks if the length of the joined chunks is the same as the original text.
        """
        declaration = extract_text("docs/declaration")
        declaration_chunks = split_docs(declaration, 20000)
        joined_result = ''.join(declaration_chunks)
        self.assertEqual(len(joined_result), len(declaration))
    
    def test_split_docs_with_separator(self):
        """
        Test that _split_docs_with_separator correctly splits text using a given separator.

        The input text is "AAAAAAA. BBBBBBB. CCCCCCC. DDDDDDD" and the separator is ". ".
        The expected output is four chunks: ["AAAAAAA. ", "BBBBBBB. ", "CCCCCCC. ", "DDDDDDD"].
        """
        text = "A" * 7 + ". " + "B" * 7 + ". " + "C" * 7 + ". " + "D" * 7
        separator = ". "
        expected_chunks = ["A" * 7 + ". ", "B" * 7 + ". ", "C" * 7 + ". ", "D" * 7]
        result = _split_docs_with_separator(text, separator)
        self.assertEqual(result, expected_chunks)

    def test_split_docs_with_separator_no_separator(self):
        """
        Test that _split_docs_with_separator correctly splits text into individual characters when no separator is provided.

        The input text is "AAAAAAABBBBBBBCCCCCCCDDDDDDD" and the separator is an empty string.
        The expected output is a list of individual characters.
        """
        text = "A" * 7 + "B" * 7 + "C" * 7 + "D" * 7
        separator = ""
        expected_chunks = list(text)
        result = _split_docs_with_separator(text, separator)
        self.assertEqual(result, expected_chunks)

    def test_split_docs_with_separator_empty_text(self):
        """
        Test that _split_docs_with_separator returns an empty list when the input text is empty.

        The input text is an empty string and the separator is ". ".
        The expected output is a list containing an empty string.
        """
        text = ""
        separator = ". "
        expected_chunks = [""]
        result = _split_docs_with_separator(text, separator)
        self.assertEqual(result, expected_chunks)

    def test_split_docs_with_separator_multiple_separators(self):
        """
        Test that _split_docs_with_separator correctly splits text using a space as the separator.

        The input text is "AAAAAAA BBBBBBB CCCCCCC DDDDDDD" and the separator is a space.
        The expected output is four chunks: ["AAAAAAA ", "BBBBBBB ", "CCCCCCC ", "DDDDDDD"].
        """
        text = "A" * 7 + " " + "B" * 7 + " " + "C" * 7 + " " + "D" * 7
        separator = " "
        expected_chunks = ["A" * 7 + " ", "B" * 7 + " ", "C" * 7 + " ", "D" * 7]
        result = _split_docs_with_separator(text, separator)
        self.assertEqual(result, expected_chunks)

    def test_split_docs_with_separator_edge_case(self):
        """
        Test that _split_docs_with_separator correctly handles edge cases with unusual separators.

        The input text is "AAAAAAA..BBBBBBB" and the separator is "..".
        The expected output is two chunks: ["AAAAAAA..", "BBBBBBB"].
        """
        text = "A" * 7 + ".." + "B" * 7
        separator = ".."
        expected_chunks = ["A" * 7 + "..", "B" * 7]
        result = _split_docs_with_separator(text, separator)
        self.assertEqual(result, expected_chunks)

if __name__ == '__main__':
    unittest.main()