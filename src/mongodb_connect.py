import datetime

import pymongo
from bson import ObjectId
from bson import json_util
from pymongo.errors import DuplicateKeyError
from pymongo.results import _WriteResult

from src.word import Word, WORD, LANGUAGE

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
DB_NAME = "word_db"
COL_NAME = "words"


class MongoHandler(object):
    def __init__(self):
        self.mc = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        db = self.mc.get_database(DB_NAME)
        # print(db.list_collection_names())

        self.word_coll = db.get_collection(COL_NAME)
        # Create compound unique index on word + language
        self.word_coll.create_index(
            [(WORD, pymongo.ASCENDING), (LANGUAGE, pymongo.ASCENDING)],
            unique=True
        )

    def close(self):
        self.mc.close()

    def insert_word(self, word):
        try:
            return self.word_coll.insert_one(word)
        except DuplicateKeyError:
            # DuplicateKeyError is thrown for duplicate word+language combination
            print(f"Skipping duplicate word: {word.get(WORD)} ({word.get(LANGUAGE)})")
            return PseudoResult(False)

    def find_recent_words(self, limit=10):
        return [
            Word(w)
            for w in self.word_coll.find().sort("_id", pymongo.DESCENDING).limit(limit)
        ]

    def find_words_from_n_minutes_ago(self, minutes_ago, limit=10):
        few_minutes_ago = datetime.datetime.now(datetime.UTC) - datetime.timedelta(
            minutes=minutes_ago
        )
        oid = ObjectId.from_datetime(few_minutes_ago)
        gt_this_oid = {"_id": {"$gt": oid}}
        return [
            Word(w)
            for w in self.word_coll.find(gt_this_oid)
            .sort("_id", pymongo.DESCENDING)
            .limit(limit)
        ]

    def clear_words(self, all_words=False, timedelta=None):
        """Delete words from the database

        mh.clear_words(True)    -> clear all words
        mh.clear_words(timedelta=datetime.timedelta(minutes=30))) -> clear all words of last 30 mins
        :param all_words: boolean, if True, rest is ignored!
        :param timedelta: takes a datetime.timedelta object
        :return:
        """
        if all_words is True:
            return self.word_coll.delete_many({})
        if timedelta:
            some_time_ago = datetime.datetime.now(datetime.UTC) - timedelta
            gt_this_oid = {"_id": {"$gt": ObjectId.from_datetime(some_time_ago)}}
            return self.word_coll.delete_many(gt_this_oid)
        else:
            return PseudoResult(False)

    def dump(self, json_out_path):
        data = list(self.word_coll.find())
        with open(json_out_path, "w", encoding="utf-8") as f:
            f.write(json_util.dumps(data, indent=4))

    def get_db_stats(self):
        """Get database statistics including size."""
        return self.mc.get_database(DB_NAME).command("dbStats")

    def print_db_stats(self):
        """Print database statistics in a readable format."""
        stats = self.get_db_stats()
        print(f"Database: {DB_NAME}")
        print(f"Collections: {stats['collections']}")
        print(f"Documents: {stats['objects']}")
        print(f"Total size: {stats['dataSize'] / 1024 / 1024:.2f} MB")
        print(f"Storage size: {stats['storageSize'] / 1024 / 1024:.2f} MB")
        print(f"Indexes: {stats['indexes']}")
        print(f"Index size: {stats['indexSize'] / 1024 / 1024:.2f} MB")

    def rebuild_index(self):
        """Rebuild the compound unique index on word + language."""
        print("Dropping all indexes...")
        self.word_coll.drop_indexes()
        print("Creating new compound index on word + language...")
        self.word_coll.create_index(
            [(WORD, pymongo.ASCENDING), (LANGUAGE, pymongo.ASCENDING)],
            unique=True
        )
        print("Index rebuilt successfully.")


class PseudoResult(_WriteResult):
    """Class that can be used where a WriteResult is expected, although
    no proper one is ready. (E.g. if exception occurred during write attempt)."""

    __slots__ = ("__inserted_id", "__acknowledged")

    def __init__(self, acknowledged, oid=None):
        super().__init__(acknowledged)
        self.__inserted_id = oid

    @property
    def inserted_id(self):
        """The inserted document's _id."""
        return self.__inserted_id
