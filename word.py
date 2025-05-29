""" module to cover the class Word
 (at least to add documentation to the word_template.json)
"""
import os
from bson import json_util
from json.decoder import JSONDecodeError

TEMPLATE_FILEPATH = "word_template.json"

WORD = "word"
LANGUAGE = "language"
PART_OF_SPEECH = "part of speech"
HYPHENATION = "hyphenation"
TOPICS = "topic"
SOURCE = "source"
DERIVED_LANGUAGE = "derived language"
REMARK = "remark"
WORD_KEYS = [
    WORD,
    LANGUAGE,
    PART_OF_SPEECH,
    HYPHENATION,
    TOPICS,
    SOURCE,
    DERIVED_LANGUAGE,
    REMARK,
]

MIDDLE_DOT = "‧"  # U+00B7 Middle Dot (Mittelpunkt) - as in German Wiktionary
# REMARK: English Wiktionary uses the following:
HYPHENATION_POINT = "‧"  # U+2027 Hyphenation Point (Trennpunkt)

ALLOWED_LANGS = ["English", "German", "Ancient Greek", "Latin"]
ALLOWED_POS = [
    "noun",
    "name",
    "verb",
    "adjective",
    "adverb",
    "pronoun",
    "preposition",
    "conjunction",
    "interjection",
    "numeral",
    "article",
]


def to_words(words):
    return [Word(word) for word in words]


class WordError(Exception):
    """Exception if input to Word() does not following expectations."""

    pass


class Word(object):
    """A word object, which can be read from JSON and stored in Mongo DB."""

    def __init__(self, inputw=None):
        if isinstance(inputw, dict):
            self.data = inputw
        elif isinstance(inputw, str):
            if os.path.isfile(inputw):
                with open(inputw, encoding="utf-8") as f:
                    self.data = json_util.loads(f.read())
            else:
                try:
                    json_util.loads(inputw)
                except JSONDecodeError:
                    self.data = {}
        else:
            self.data = {}

    def __repr__(self):
        repre = f"{self.word} ({self.language})"
        if self.part_of_speech is not None:
            repre = f"{repre}, {self.part_of_speech}"
        if self.topics is not None:
            repre = f"{repre}, topic: {self.topics}"
        if self.source is not None:
            repre = f"{repre}, source: {self.source}"
        return repre

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        if (
            new_data.get(LANGUAGE) not in ALLOWED_LANGS
            and new_data.get(LANGUAGE) is not None
        ):
            raise WordError(f"Not in allowed languages: " f"{new_data.get(LANGUAGE)}")
        if (
            new_data.get(DERIVED_LANGUAGE) not in ALLOWED_LANGS
            and new_data.get(DERIVED_LANGUAGE) is not None
        ):
            raise WordError(
                f"Not in allowed derived languages: "
                f"{new_data.get(DERIVED_LANGUAGE)}"
            )
        if (
            new_data.get(PART_OF_SPEECH) not in ALLOWED_POS
            and new_data.get(PART_OF_SPEECH) is not None
        ):
            raise WordError(
                f"Not in allowed part of speeches: " f"{new_data.get(PART_OF_SPEECH)}"
            )
        self._data = new_data

    @property
    def word(self):
        """actual word/name <mandatory>"""
        return self._data.get(WORD)

    @word.setter
    def word(self, new_word):
        self._data[WORD] = new_word

    @property
    def language(self):
        """language of the word <mandatory>"""
        return self._data.get(LANGUAGE)

    @language.setter
    def language(self, new_language):
        if new_language in ALLOWED_LANGS:
            self._data[LANGUAGE] = new_language
        else:
            raise WordError

    @property
    def part_of_speech(self):
        """part of speech of the word (noun, verb, ...)  <optional>"""
        return self._data.get(PART_OF_SPEECH)

    @part_of_speech.setter
    def part_of_speech(self, new_pospeech):
        # TODO: how/where to distinguish names from other words?
        if new_pospeech in PART_OF_SPEECH:
            self._data[PART_OF_SPEECH] = new_pospeech
        else:
            raise WordError

    @property
    def hyphenation(self):
        """hyphenation (noun, verb, ...) <optional>
        Hyphenation describes how a word is broken across line breaks.
        It is a question of typography, of formatting printed or screen display
        of a word for aesthetic reasons."""
        return self._data.get(HYPHENATION)

    @hyphenation.setter
    def hyphenation(self, new_hyph):
        if HYPHENATION_POINT in new_hyph:
            new_hyph.replace(HYPHENATION_POINT, MIDDLE_DOT)
        self._data[HYPHENATION] = new_hyph

    @property
    def topics(self):
        """list of related topics / categorys of the word <optional>"""
        return self._data.get(TOPICS)

    @topics.setter
    def topics(self, new_topics):
        self._data[TOPICS] = new_topics

    @property
    def source(self):
        """source of the word / name <optional>
        especially for Names (e.g. Book/Comic/Movie/Webpage/Podcast/...)"""
        return self._data.get(SOURCE)

    @source.setter
    def source(self, new_source):
        self._data[SOURCE] = new_source

    @property
    def derived_language(self):
        """derived language: i.e. which language the word is 'classically'
        derived from <optional>
        e.g. anthropozentrisch -> greek (no intermediate languages)"""
        return self._data.get(SOURCE)

    @derived_language.setter
    def derived_language(self, new_der_lang):
        if new_der_lang in ALLOWED_LANGS:
            self._data[SOURCE] = new_der_lang
        else:
            raise WordError

    @property
    def remark(self):
        """remark <optional>
        general comment to a word, which does not fit into other categories"""
        return self._data.get(REMARK)

    @remark.setter
    def remark(self, new_remark):
        self._data[REMARK] = new_remark

    # ---
    def insert(self, mh):
        return mh.insert_word(self.data)

    # TODO
    #  other links for mongohandler update? delete? ...

    def to_dict(self):
        return self.data

    def to_json(self, output_dir, filename=None):
        if filename is None:
            filename = self.word
        if not filename.endswith(".json"):
            filename += ".json"

        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_util.dumps(self.data))
