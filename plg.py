""" main module for crawler/dictionary lib
-> probably rather playground since it could be a sort of generic library
   and not a single script/programm """

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
    # parse de.wikt; only articles
    dump_file_path = (
        r"D:\Docs\Sonstiges\dewiktionary-20220521-pages-articles-multistream_crop.xml"
    )

    # with open(dump_file_path, "rb") as in_xml:
    #     for record in MediaWikiPageExtractor(in_xml, namespace="0"):
    #         dwp = DeWiktParser(record)
    #         word = dwp.parse()
    with open(
        r"tests\example_wikitxt.txt",
        "r",
        encoding="utf-8",
    ) as wiki_example:
        content = wiki_example.read()
        dwp = DeWiktParser(content)
        word = dwp.parse()
        print(word)


if __name__ == "__main__":
    parse_wikt_dump()
