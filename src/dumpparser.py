"""Parse/Analyse/Whatever the XML dump of a Mediawiki.

orig:
https://stackoverflow.com/questions/16533153/parse-xml-dump-of-a-mediawiki-wiki
 -> does not work for large files
https://stackoverflow.com/a/55147982

"""

from lxml import etree
import os
from dotenv import load_dotenv

TITLE = "title"
TEXT = "text"
NAMESPACE = "xmlns"

XPATH_TO_TEXT = f"./{NAMESPACE}:revision/{NAMESPACE}:{TEXT}/{TEXT}( )"
XPATH_TO_TITLE = f"./{NAMESPACE}:title/text( )"
XPATH_TO_NAMESPACE = f"./{NAMESPACE}:ns/text( )"

load_dotenv()
dump_file_path = os.getenv("XML_DUMP_INPUT")

"""
entity = {}
# Assign the 'elem.namespace' to the 'xpath'
#   Article text is child of revision,
#   namespace needed..
#   text twice: xmlns:text is the XML element called 'text'
#   text( ) is the actual content
entity["revision"] = elem.xpath(
    self.xpath,
    namespaces={NAMESPACE: etree.QName(elem).namespace},
)

# REMARK: example for without namespace..
# entity["revision"] = elem.xpath("./revision/text/text( )")
# entity["revision"] = elem.xpath("./title/text( )")
"""


def get_xpath_content(elem, xpath):
    return elem.xpath(
        xpath,
        namespaces={NAMESPACE: etree.QName(elem).namespace},
    )


class MediaWikiPageExtractor:
    """Extract all pages contents."""

    def __init__(self, fh, tag="page", xpath=XPATH_TO_TEXT, namespace=None):
        """
        Initialize 'iterparse' to only generate 'end' events on tag '<entity>'

        :param fh: File Handle from the XML File to parse
        :param tag: The tag to process
        """
        # Prepend the default Namespace {*} to get anything.
        self.context = etree.iterparse(fh, events=("end",), tag=["{*}" + tag])
        self.xpath = xpath
        self.namespace = namespace

    def _parse(self):
        """
        Parse the XML File for all '<tag>...</tag>' Elements
        Clear/Delete the Element Tree after processing

        :return: Yield the current 'Event, Element Tree'
        """
        for event, elem in self.context:
            yield event, elem

            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

    def __iter__(self):
        """
        Iterate all '<tag>...</tag>' Element Trees yielded from self._parse()

        :return: str: content
        """
        for event, elem in self._parse():
            if self.namespace:
                if get_xpath_content(elem, XPATH_TO_NAMESPACE)[0] != self.namespace:
                    continue

            res = get_xpath_content(elem, self.xpath)
            if not res:
                # empty page
                continue
            yield res[0]


class MediaWikiEmptyPageExtractor(MediaWikiPageExtractor):
    def __iter__(self):
        for event, elem in self._parse():
            if self.namespace:
                if get_xpath_content(elem, XPATH_TO_NAMESPACE)[0] != self.namespace:
                    continue

            res = get_xpath_content(elem, self.xpath)
            if not res:
                # empty page -> yield title
                yield get_xpath_content(elem, XPATH_TO_TITLE)


class MediaWikiTitleExtractor(MediaWikiPageExtractor):
    """Only extract titles"""

    def __init__(
        self, fh, tag="page", xpath=XPATH_TO_TEXT, namespace=None, cat_filter=None
    ):
        """
        Initialize 'iterparse' to only generate 'end' events on tag '<entity>'

        :param fh: File Handle from the XML File to parse
        :param tag: The tag to process
        """
        super().__init__(fh, tag, xpath, namespace)
        self.cat_filter = cat_filter

    def __iter__(self):
        """
        Iterate all '<tag>...</tag>' Element Trees yielded from self._parse()

        :return: str: content
        """
        for event, elem in self._parse():
            if self.namespace:
                if get_xpath_content(elem, XPATH_TO_NAMESPACE)[0] != self.namespace:
                    continue

            res = get_xpath_content(elem, self.xpath)
            if not res:
                # empty page
                continue
            # TODO
            #  check if in category -> cant do that.. can only parse for template
            if self.cat_filter:
                if self.cat_filter not in res[0]:
                    continue

            # yield title
            yield get_xpath_content(elem, XPATH_TO_TITLE)[0]


if __name__ == "__main__":
    # all page contents
    # with open(dump_file_path, "rb") as in_xml:
    #    for record in MediaWikiPageExtractor(in_xml):
    #         print(record)

    # number of pages
    with open(dump_file_path, "rb") as in_xml:
        a = list(MediaWikiPageExtractor(in_xml))
        print(len(a))

    # empty pages
    # with open(dump_file_path, "rb") as in_xml:
    #     for record in MediaWikiEmptyPageExtractor(in_xml):
    #         print(record)
