"""Command-line interface for dictionary operations."""
import os
from pathlib import Path
from dotenv import load_dotenv

from src.crawler import Crawler
from src.dictparser import (
    DeWiktParser,
)
from src.dumpparser import MediaWikiPageExtractor, MediaWikiTitleExtractor
from src.mongodb_connect import MongoHandler
from src.word import TOPICS, PART_OF_SPEECH, LANGUAGE, Word, to_words
from src.dump_processor import DumpProcessor

load_dotenv()

CAT_GERMAN = "Kategorie:Deutsch"
TEMPLATE_GERMAN = "{{Sprache|Deutsch}}"
EX_CAT = "Kategorie:Präposition (Deutsch)"
EX_LEMMA = "hinsichtlich"


def search_db(topic: str = "Culture Ship Name"):
    """Search for a random word with the specified topic.
    
    Args:
        topic: Topic to search for (default: "Culture Ship Name")
    """
    mh = MongoHandler()
    try:
        res = mh.word_coll.aggregate(
            [{"$match": {TOPICS: topic}}, {"$sample": {"size": 1}}]
        )
        res = to_words(list(res))
        [print(w) for w in res]
    finally:
        mh.close()


def dump():
    """Dump the MongoDB collection to a JSON file."""
    mh = MongoHandler()
    try:
        mh.dump(Path(__file__).parent / "dump.json")
    finally:
        mh.close()


def parse_wikt_dump(dump_file_path: str = None):
    """Parse the German Wiktionary dump and store all words in MongoDB.
    
    Args:
        dump_file_path: Optional path to dump file. If None, uses default path.
    """
    if dump_file_path is None:
        dump_file_path = os.getenv("XML_DUMP_INPUT")

    processor = DumpProcessor()
    processed, stored = processor.process_dump(dump_file_path)
    
    print(f"Finished processing {processed} articles")
    print(f"Successfully stored {stored} words in MongoDB")


def query_words(language=None, part_of_speech=None, limit=10):
    """Query words from MongoDB by language and/or part of speech.
    
    Args:
        language: Optional language to filter by
        part_of_speech: Optional part of speech to filter by
        limit: Maximum number of results to return (default 10)
        
    Returns:
        List of Word objects matching the query
    """
    mh = MongoHandler()
    try:
        query = {}
        if language:
            query[LANGUAGE] = language
        if part_of_speech:
            query[PART_OF_SPEECH] = part_of_speech

        results = mh.word_coll.find(query).limit(limit)
        return to_words(list(results))
    finally:
        mh.close()


if __name__ == "__main__":
    # Initialize MongoDB connection
    mh = MongoHandler()
    try:
        # Rebuild index if needed
        mh.rebuild_index()
        # Print database statistics
        mh.print_db_stats()
    finally:
        mh.close()
