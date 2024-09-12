import unittest
from docsum import split_docs, extract_text, _split_docs_with_separator

class TestSplitDocs(unittest.TestCase):


    def test_split_docs_length_simple(self):
        text = "A" * 5 + "B" * 5 + "C" * 5
        chunks = split_docs(text, 5)
        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0], "AAAAA")
        self.assertEqual(chunks[1], "BBBBB")
        self.assertEqual(chunks[2], "CCCCC")

    # Test that split_docs returns a string of same length as input
    def test_split_docs_length_hamlet(self):
        hamlet = extract_text("docs/hamlet.txt")
        hamlet_chunks = split_docs(hamlet, 20000)
        # Join the chunks back together
        joined_result = ''.join(hamlet_chunks)
        # Check if the length of the joined result is the same as the input text
        self.assertEqual(len(joined_result), len(hamlet))

    # test that split_docs on hamlet doesnt result in any chunks smaller than 100 characters
    def test_split_docs_length_hamlet_min_length(self):
        hamlet = extract_text("docs/hamlet.txt")
        hamlet_chunks = split_docs(hamlet, 20000)
        for chunk in hamlet_chunks:
            self.assertGreater(len(chunk), 100)
    
    def test_split_docs_length_declaration(self):
        declaration = extract_text("docs/declaration")
        declaration_chunks = split_docs(declaration, 20000)
        joined_result = ''.join(declaration_chunks)
        self.assertEqual(len(joined_result), len(declaration))
    
    def test_split_docs_with_separator(self):
        text = "A" * 7 + ". " + "B" * 7 + ". " + "C" * 7 + ". " + "D" * 7
        separator = ". "
        expected_chunks = ["A" * 7 + ". ", "B" * 7 + ". ", "C" * 7 + ". ", "D" * 7]
        result = _split_docs_with_separator(text, separator)
        self.assertEqual(result, expected_chunks)

    def test_split_docs_with_separator_no_separator(self):
        text = "A" * 7 + "B" * 7 + "C" * 7 + "D" * 7
        separator = ""
        expected_chunks = list(text)
        result = _split_docs_with_separator(text, separator)
        self.assertEqual(result, expected_chunks)

    def test_split_docs_with_separator_empty_text(self):
        text = ""
        separator = ". "
        expected_chunks = [""]
        result = _split_docs_with_separator(text, separator)
        self.assertEqual(result, expected_chunks)

    def test_split_docs_with_separator_multiple_separators(self):
        text = "A" * 7 + " " + "B" * 7 + " " + "C" * 7 + " " + "D" * 7
        separator = " "
        expected_chunks = ["A" * 7 + " ", "B" * 7 + " ", "C" * 7 + " ", "D" * 7]
        result = _split_docs_with_separator(text, separator)
        self.assertEqual(result, expected_chunks)

    def test_split_docs_with_separator_edge_case(self):
        text = "A" * 7 + ".." + "B" * 7
        separator = ".."
        expected_chunks = ["A" * 7 + "..", "B" * 7]
        result = _split_docs_with_separator(text, separator)
        self.assertEqual(result, expected_chunks)

if __name__ == '__main__':
    unittest.main()