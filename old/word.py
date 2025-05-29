""" module to cover the class Word
 (at least to add documentation to the word_template.json)
"""
import os
from bson import json_util
from json.decoder import JSONDecodeError

TEMPLATE_FILEPATH = "word_template.json"

WORD = "word"
LANGUAGE = "language"
PART_OF_SPEECH = "part_of_speech"
HYPHENATION = "hyphenation"
TOPIC = "topic"
SOURCE = "source"
DERIVED_LANGUAGE = "derived_language"
WORD_KEYS = [WORD, LANGUAGE, PART_OF_SPEECH, HYPHENATION, TOPIC, SOURCE, DERIVED_LANGUAGE]

MIDDLE_DOT = "‧"  # U+00B7 Middle Dot (Mittelpunkt) - as in German Wiktionary
# REMARK: English Wiktionary uses the following:
HYPHENATION_POINT = "‧"  # U+2027 Hyphenation Point (Trennpunkt)


class Word(object):
    def __init__(self, inputw=None):
        if isinstance(inputw, dict):
            self.data = inputw
        elif isinstance(inputw, str):
            if os.path.isfile(inputw):
                with open(inputw) as f:
                    self.data = json_util.loads(f.read())
            else:
                try:
                    json_util.loads(inputw)
                except JSONDecodeError:
                    self.data = {}
        else:
            self.data = {}

    def __repr__(self):
        repre = "%s (%s)" % (self.word, self.language)
        if self.part_of_speech is not None:
            repre += repre + ", %s" % self.part_of_speech
        if self.topic is not None:
            repre += repre + ", topic: %s" % self.topic
        if self.source is not None:
            repre += repre + ", source: %s" % self.source
        return repre

    @property
    def word(self):
        """ actual word/name <mandatory> """
        return self.data.get(WORD)

    @word.setter
    def word(self, new_word):
        self.data[WORD] = new_word

    @property
    def language(self):
        """ language of the word <mandatory> """
        return self.data.get(LANGUAGE)

    @language.setter
    def language(self, new_language):
        # TODO: make check for allowed languages
        self.data[LANGUAGE] = new_language

    @property
    def part_of_speech(self):
        """ part of speech of the word (noun, verb, ...)  <optional> """
        return self.data.get(PART_OF_SPEECH)

    @part_of_speech.setter
    def part_of_speech(self, new_pospeech):
        # TODO: make check for allowed part_of_speeches
        # TODO: how/where to distinguish names from other words?
        self.data[PART_OF_SPEECH] = new_pospeech

    @property
    def hyphenation(self):
        """ hyphenation (noun, verb, ...) <optional>
        Hyphenation describes how a word is broken across line breaks.
        It is a question of typography, of formatting printed or screen display of a word for aesthetic reasons."""
        return self.data.get(HYPHENATION)

    @hyphenation.setter
    def hyphenation(self, new_hyph):
        # TODO
        #  check new_hyph contains MIDDLE_DOT
        self.data[HYPHENATION] = new_hyph

    @property
    def topic(self):
        """ list of related topics / categorys of the word <optional> """
        return self.data.get(TOPIC)

    @topic.setter
    def topic(self, new_topic):
        self.data[TOPIC] = new_topic

    @property
    def source(self):
        """ source of the word / name <optional>
        especially for Names (e.g. Book/Comic/Movie/Webpage/Podcast/...) """
        return self.data.get(SOURCE)

    @source.setter
    def source(self, new_source):
        self.data[SOURCE] = new_source

    @property
    def derived_language(self):
        """ derived language: i.e. which language the word is 'classically' derived from <optional>
        e.g. anthropozentrisch -> greek (no intermediate languages)"""
        return self.data.get(SOURCE)

    @derived_language.setter
    def derived_language(self, new_der_lang):
        # TODO: make check for allowed languages
        self.data[SOURCE] = new_der_lang

    def insert(self, mh):
        return mh.insert_word(self.data)

    # TODO
    #  other links for mongohandler update? delete? ...
