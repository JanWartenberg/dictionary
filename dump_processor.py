"""Module for processing Wiktionary XML dumps and storing entries in MongoDB."""

from typing import Optional, Generator, Tuple

from dumpparser import MediaWikiPageExtractor
from dictparser import DeWiktParser
from mongodb_connect import MongoHandler
from word import Word


class DumpProcessor:
    """Handles processing of Wiktionary XML dumps and storing entries in MongoDB."""
    
    def __init__(self, mongo_handler: Optional[MongoHandler] = None):
        """Initialize the processor with an optional MongoDB handler.
        
        Args:
            mongo_handler: Optional MongoDB handler. If None, creates a new one.
        """
        self.mh = mongo_handler or MongoHandler()
        self._processed = 0
        self._stored = 0

    def process_dump(self, dump_file_path: str, namespace: str = "0") -> Tuple[int, int]:
        """Process a Wiktionary XML dump file and store entries in MongoDB.
        
        Args:
            dump_file_path: Path to the XML dump file
            namespace: MediaWiki namespace to process (default "0" for articles)
            
        Returns:
            Tuple of (processed_count, stored_count)
        """
        try:
            with open(dump_file_path, "rb") as in_xml:
                for record in MediaWikiPageExtractor(in_xml, namespace=namespace):
                    self._processed += 1
                    if self._processed % 1000 == 0:
                        print(f"Processed {self._processed} articles, stored {self._stored} words")

                    try:
                        word = self._process_record(record)
                        if word:
                            self._stored += 1
                    except Exception as e:
                        print(f"Error processing record: {e}")
                        continue

            return self._processed, self._stored
        finally:
            # Don't close MongoDB connection if it was passed in
            if self.mh and not isinstance(self.mh, MongoHandler):
                self.mh.close()

    def process_dump_generator(self, dump_file_path: str, namespace: str = "0") -> Generator[Word, None, None]:
        """Process a Wiktionary dump file and yield Word objects without storing them.
        
        Args:
            dump_file_path: Path to the XML dump file
            namespace: MediaWiki namespace to process (default "0" for articles)
            
        Yields:
            Word objects parsed from the dump
        """
        with open(dump_file_path, "rb") as in_xml:
            for record in MediaWikiPageExtractor(in_xml, namespace=namespace):
                try:
                    word = self._process_record(record)
                    if word:
                        yield word
                except Exception as e:
                    print(f"Error processing record: {e}")
                    continue

    def _process_record(self, record) -> Optional[Word]:
        """Process a single MediaWiki record and return a Word object if valid.
        
        Args:
            record: MediaWiki record to process
            
        Returns:
            Word object if successfully parsed, None otherwise
        """
        parser = DeWiktParser(record)
        word = parser.parse()
        
        if word and word.word and word.language:
            if isinstance(self.mh, MongoHandler):
                word.insert(self.mh)
            return word
        return None

    @property
    def processed_count(self) -> int:
        """Number of records processed."""
        return self._processed

    @property
    def stored_count(self) -> int:
        """Number of words stored in MongoDB."""
        return self._stored 