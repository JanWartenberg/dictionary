"""
Module to collect parsers,
which parse some input into Word() class.
"""
import re

from word import Word
from word import LANGUAGE, PART_OF_SPEECH, TOPICS, WORD


class DeWiktParser(object):
    """de-wikt"""

    def __init__(self, content):
        self.content = content

    def _get_header_sections(self):
        # TODO
        #  get everything before == HEADER ==, and all Header Sections
        #  when I finally get how the shit works
        # res = re.findall("={2}[^=][.]+={2}", self.content)
        # res = re.findall("={2}.+={2}", self.content, re.MULTILINE)
        # perhaps like this
        # res = re.findall("(.*?)(==[^\n]*)(.*?)", self.content, re.DOTALL)
        # H2_pattern = "[^=]={2}(?:[^=]).*[^=]={2}(?:[^=])"

        res = re.findall("(.*?)[^=]={2}[^=].*?[^=]={2}[^=]", self.content, re.DOTALL)
        pre_header = res[0]
        rest = res[1]
        # TODO split by header sections

        print(res)

    def parse(self):
        """"""
        # TODO implement actual regexing
        tmp_dict = {}
        # TODO: WORD
        # tmp_dict[WORD] = ???
        self._get_header_sections()
        # TODO: LANGUAGE
        # TODO: PART_OF_SPEECH
        # TODO: HYPHENATION
        # TODO: TOPICS

        return Word(tmp_dict)


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
