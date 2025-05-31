"""main module for crawler/dictionary lib
-> probably rather playground since it could be a sort of generic library
   and not a single script/programm"""

import datetime
from pathlib import Path
import time

from crawler import Crawler

from dictparser import (
    DeWiktParser,
)
from dumpparser import MediaWikiPageExtractor, MediaWikiTitleExtractor
from mongodb_connect import MongoHandler
from word import TOPICS, Word, to_words

CAT_GERMAN = "Kategorie:Deutsch"
TEMPLATE_GERMAN = "{{Sprache|Deutsch}}"
EX_CAT = "Kategorie:Präposition (Deutsch)"
EX_LEMMA = "hinsichtlich"


def search_db():
    mh = MongoHandler()
    res = mh.word_coll.aggregate(
        [{"$match": {TOPICS: "Culture Ship Name"}}, {"$sample": {"size": 1}}]
    )
    res = to_words(list(res))
    [print(w) for w in res]


def dump():
    mh = MongoHandler()
    mh.dump(Path(__file__).parent / "dump.json")


def parse_wikt_dump():
    """Parse the German Wiktionary dump and store all words in MongoDB.
    Only processes articles (namespace="0") and stores them by language."""
    # parse de.wikt; only articles
    dump_file_path = (
        r"D:\Docs\Sonstiges\dewiktionary-20220521-pages-articles-multistream_crop.xml"
    )

    mh = MongoHandler()
    processed = 0
    stored = 0

    try:
        with open(dump_file_path, "rb") as in_xml:
            for record in MediaWikiPageExtractor(in_xml, namespace="0"):
                processed += 1
                if processed % 1000 == 0:
                    print(f"Processed {processed} articles, stored {stored} words")

                try:
                    dwp = DeWiktParser(record)
                    word = dwp.parse()
                    if word and word.word and word.language:  # Only store if we have valid word data
                        word.insert(mh)
                        stored += 1
                except Exception as e:
                    print(f"Error processing record: {e}")
                    continue
    finally:
        print(f"Finished processing {processed} articles")
        print(f"Successfully stored {stored} words in MongoDB")
        mh.close()


def query_words(language=None, part_of_speech=None, limit=10):
    """Query words from MongoDB by language and/or part of speech."""
    mh = MongoHandler()
    try:
        query = {}
        if language:
            query[LANGUAGE] = language
        if part_of_speech:
            query[PART_OF_SPEECH] = part_of_speech

        results = mh.word_coll.find(query).limit(limit)
        words = to_words(list(results))
        return words
    finally:
        mh.close()


if __name__ == "__main__":
    # parse_wikt_dump()
    mh = MongoHandler()

    # Uncomment the next line to rebuild the index if needed
    mh.rebuild_index()

    mh.print_db_stats()
    mh.close()
