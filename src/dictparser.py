"""
Module to collect parsers,
which parse some input into Word() class.
"""

import re

from src.word import Word
from src.word import (
    LANGUAGE,
    PART_OF_SPEECH,
    TOPICS,
    WORD,
    HYPHENATION,
    SOURCE,
    DERIVED_LANGUAGE,
    REMARK,
)

# Mapping from German Wiktionary terms to MongoDB field names
DE_WIKT_TO_MONGO = {
    # Basic fields
    "Wort": WORD,
    "Sprache": LANGUAGE,
    "Wortart": PART_OF_SPEECH,
    "Silbentrennung": HYPHENATION,
    "Thema": TOPICS,
    "Quelle": SOURCE,
    "Herkunftssprache": DERIVED_LANGUAGE,
    "Anmerkung": REMARK,
    # Parts of speech mappings
    "Substantiv": "noun",
    "Eigenname": "name",
    "Verb": "verb",
    "Adjektiv": "adjective",
    "Adverb": "adverb",
    "Pronomen": "pronoun",
    "Präposition": "preposition",
    "Konjunktion": "conjunction",
    "Interjektion": "interjection",
    "Numerale": "numeral",
    "Artikel": "article",
    # Language mappings
    "Deutsch": "German",
    "Englisch": "English",
    "Altgriechisch": "Ancient Greek",
    "Latein": "Latin",
}


class DeWiktParser(object):
    """Parser for German Wiktionary entries"""

    def __init__(self, content):
        self.content = content

    def _get_header_sections(self):
        """
        Parse header sections from wikitext content.
        Extracts sections in the format: == <page title> ({{Sprache|language}}) ==
        Returns a list of tuples (title, language, section_content)
        """
        # Pattern to match header sections
        # == title ({{Sprache|lang}}) ==
        header_pattern = r"==\s*([^=\n(]+?)\s*\({{Sprache\|([^}]+)}}\)\s*=="

        # Split content into sections by headers
        sections = re.split(header_pattern, self.content)

        # First element is content before any headers
        pre_header = sections[0]

        # Process remaining sections
        parsed_sections = []
        for i in range(
            1, len(sections), 3
        ):  # Step by 3 because we have title, lang, and content groups
            if i + 2 < len(sections):
                title = sections[i].strip()
                language = DE_WIKT_TO_MONGO.get(
                    sections[i + 1].strip(), sections[i + 1].strip()
                )  # Map language if possible
                content = sections[i + 2].strip()
                parsed_sections.append((title, language, content))

        return pre_header, parsed_sections

    def parse(self):
        """Parse the wikitext content into a Word object."""
        pre_header, sections = self._get_header_sections()

        # Initialize word dictionary
        word_dict = {}

        # If we have any sections, use the first one as the main entry
        if sections:
            title, language, content = sections[0]
            word_dict[WORD] = title
            word_dict[LANGUAGE] = language

            # TODO: Extract additional information from content:
            # - Part of speech
            # - Hyphenation
            # - Topics

        return Word(word_dict)


class TextParser(object):
    """Parse a single txt file.

    Syntax:

    ## comment (to be ignored)
    Actual word
    Actual word2
        source of word

    """

    def __init__(self, filepath, default_dict=None):
        """
        Args:
            filepath: path to input file
            default_dict: dict to set default values (e.g. language)
        """
        if default_dict is None:
            default_dict = {}
        self.filepath = filepath
        self.def_dict = default_dict

    def parse(self):
        """Do the actual parsing."""
        with open(self.filepath, encoding="utf-8") as f:
            words = []
            for line in f:
                line = line.strip("\n")

                if len(line) == 0:
                    continue
                if re.match(r"^##", line):
                    continue
                elif re.match(r"\S", line):
                    word_dict = {WORD: line}
                    word_dict.update(self.def_dict)
                    words.append(Word(word_dict))
                else:
                    line = line.strip(" ")
                    last_word = words[-1]
                    last_word.source = line
        return words


class FunnyParser(TextParser):
    """funny_in_general
    word / source"""

    def __init__(self, filepath=r"name_examples\funny_in_general.txt"):
        super().__init__(filepath)
        self.def_dict = {PART_OF_SPEECH: "name", LANGUAGE: "English"}


class FunnyParserDe(TextParser):
    """funny_in_general
    word / source"""

    def __init__(self, filepath=r"name_examples\funny_in_general_de.txt"):
        super().__init__(filepath)
        self.def_dict = {PART_OF_SPEECH: "name", LANGUAGE: "German"}


class RobotParser(TextParser):
    """problem: what to do with generic names? lang->English"""

    def __init__(self):
        super().__init__(filepath=r"name_examples\Namen_Roboter.txt")
        self.def_dict = {
            PART_OF_SPEECH: "name",
            LANGUAGE: "English",
            TOPICS: ["Robot name"],
        }


class CultureShipParser(TextParser):
    """"""

    def __init__(self, filepath=r"name_examples\culture_shipnames.txt"):
        super().__init__(filepath=filepath)
        self.def_dict = {
            PART_OF_SPEECH: "name",
            LANGUAGE: "English",
            TOPICS: ["Culture Ship Name"],
        }
