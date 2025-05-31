import os
import unittest

# import mongomock
from pymongo.collection import InsertOneResult

from src.mongodb_connect import MongoHandler
from src.word import Word, WordError
from src.word import WORD


def abs_test_path(filename: str) -> str:
    """Returns absolute path for a test resource file."""
    return os.path.join(os.path.dirname(__file__), filename)


# working example
WORD_EXAMPLE = abs_test_path("word_example01.json")
# wrong language
WORD_EXAMPLE2 = abs_test_path("word_example02.json")
# wrong part of speech
WORD_EXAMPLE3 = abs_test_path("word_example03.json")


class TestWord(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the base test directory path"""
        cls.dir_path = os.path.dirname(os.path.realpath(__file__))
        cls.tmp_path = os.path.join(cls.dir_path, "tmp")

    def setUp(self):
        """Create temporary directory for each test"""
        os.makedirs(self.tmp_path, exist_ok=True)

    def tearDown(self):
        """Clean up after each test"""
        self.clear_jsons()
        try:
            os.rmdir(self.tmp_path)
        except (FileNotFoundError, OSError):
            # OSError can happen if directory is not empty
            pass

    def clear_jsons(self):
        """Remove JSON files from temporary directory"""
        if not os.path.exists(self.tmp_path):
            return

        for file in os.listdir(self.tmp_path):
            if file.endswith(".json") and not file.startswith("word_example"):
                file_path = os.path.join(self.tmp_path, file)
                try:
                    os.remove(file_path)
                except (FileNotFoundError, OSError):
                    pass

    # ----
    def test_data_setter(self):
        with self.assertRaises(WordError) as cm:
            # wrong language
            w = Word(WORD_EXAMPLE2)
        self.assertIn("Not in allowed languages: ", str(cm.exception))

    def test_data_setter2(self):
        with self.assertRaises(WordError) as cm:
            # wrong part of speech
            w = Word(WORD_EXAMPLE3)
        self.assertIn("Not in allowed part of speeches: ", str(cm.exception))

    def test_to_dict(self):
        w = Word(WORD_EXAMPLE)
        ret = w.to_dict()
        self.assertIsInstance(ret, dict)

    def test_to_json(self):
        w = Word(WORD_EXAMPLE)

        # implicit file name
        w.to_json(self.tmp_path)
        expected_path = os.path.join(self.tmp_path, w.word + ".json")
        self.assertTrue(os.path.isfile(expected_path))

        # explicit file name
        w.to_json(self.tmp_path, "stabbolgfnock")
        expected_path = os.path.join(self.tmp_path, "stabbolgfnock.json")
        self.assertTrue(os.path.isfile(expected_path))

    def test_insert(self):
        mh = MongoHandler()
        w = Word(WORD_EXAMPLE)
        mh.word_coll.delete_one({WORD: w.word})
        ret = w.insert(mh)
        self.assertIsInstance(ret, InsertOneResult)
        mh.close()
