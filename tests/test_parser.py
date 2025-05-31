import os
import shutil
import tempfile
import unittest

from src.dictparser import TextParser, DeWiktParser


def abs_test_path(filename: str) -> str:
    """Returns absolute path for a test resource file."""
    return os.path.join(os.path.dirname(__file__), filename)


EXAMPLE_NAMES = """Holm Gero Düngler
   Caspar David Niedlich"""


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_parse(self):
        tmp_filepath = os.path.join(self.test_dir, "test.txt")
        with open(tmp_filepath, "w", encoding="utf-8") as f:
            f.write(EXAMPLE_NAMES)

        tp = TextParser(tmp_filepath)
        res = tp.parse()
        print(res)


# TODO: dramatically extend the test cases
class TestDeWiktParser(unittest.TestCase):
    def setUp(self):
        """Load example wiki text for each test"""
        with open(abs_test_path("example_wikitxt.txt"), "r", encoding="utf-8") as f:
            self.wiki_content = f.read()

    def test_parse_single_word(self):
        """Test that the parser correctly extracts the title"""
        parser = DeWiktParser(self.wiki_content)
        word = parser.parse()
        self.assertEqual(
            word.word, "Hallo", "Parser should extract 'Hallo' as the title"
        )
        self.assertEqual(
            word.language, "German", "Parser should extract 'German' as the language"
        )
