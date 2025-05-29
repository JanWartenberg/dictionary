# from io import StringIO
import os
import shutil
import tempfile
import unittest

from dictparser import TextParser

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
