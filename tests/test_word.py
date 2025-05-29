import os
import unittest

# import mongomock
from pymongo.collection import InsertOneResult

from mongodb_connect import MongoHandler
from word import Word, WordError
from word import WORD

# working example
WORD_EXAMPLE = "word_example01.json"
# wrong language
WORD_EXAMPLE2 = "word_example02.json"
# wrong part of speech
WORD_EXAMPLE3 = "word_example03.json"


class TestWord(unittest.TestCase):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    def setUp(self) -> None:
        self.clear_jsons()

    def tearDown(self) -> None:
        self.clear_jsons()

    def clear_jsons(self):
        for file in os.listdir(self.dir_path):
            if file.endswith(".json") and not file.startswith("word_example"):
                os.remove(os.path.join(self.dir_path, file))
                # print(os.path.join(self.dir_path, file))

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
        w.to_json(self.dir_path)
        expected_path = os.path.join(self.dir_path, w.word + ".json")
        self.assertTrue(os.path.isfile(expected_path))

        # explicit file name
        w.to_json(self.dir_path, "stabbolgfnock")
        expected_path = os.path.join(self.dir_path, "stabbolgfnock.json")
        self.assertTrue(os.path.isfile(expected_path))

    def test_insert(self):
        mh = MongoHandler()
        w = Word(WORD_EXAMPLE)
        mh.word_coll.delete_one({WORD: w.word})
        ret = w.insert(mh)
        self.assertIsInstance(ret, InsertOneResult)
