import re
import unittest

from bson import json_util
from requests import Response

from src.crawler import APK_LIST, CAT_MEMBERS, RESP_QUERY, Crawler
from tests.base import all_instance_of


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = Crawler("de", "wiktionary")

    def test_get_api_request(self):
        cat = "Kategorie:Deutsch"
        "Get the ten articles most recently added to a category"
        "api.php?action=query&list=categorymembers&cmtitle=Category:Physics&cmsort=timestamp&cmdir=desc"
        kwargs = {APK_LIST: CAT_MEMBERS, "cmsort": "timestamp", "cmdir": "desc"}

        resp = self.crawler.get_api_request(cmtitle=cat, **kwargs)

        self.assertTrue(isinstance(resp, Response))
        resp_dict = json_util.loads(resp.text)
        self.assertTrue(len(resp_dict[RESP_QUERY][CAT_MEMBERS]) == 20)

    def test_get_pages_in_cat(self):
        cat = "Kategorie:Präposition (Deutsch)"
        res = self.crawler.get_pages_in_cat(cat)

        self.assertTrue(len(res) > 100)

    def test_get_all_subcats(self):
        cat = "Kategorie:Präposition"
        res = self.crawler.get_all_subcats(cat)

        # checking from live system
        #  48: last value I saw
        self.assertTrue(len(res) > 48)
        self.assertTrue(all_instance_of(res, str))

    def test_get_page_content(self):
        ex_lemma = "hinsichtlich"

        content = self.crawler.get_page_content(ex_lemma)

        # patt = fr'== {ex_lemma}\W*\(\{\{Sprache|Deutsch\}\}\)\W*=='
        # patt = fr'== {ex_lemma}\W*\('
        patt = rf"{ex_lemma} {{{{Sprache|Deutsch}}}}"
        re_search = re.search(re.compile(patt), content)
        self.assertIsInstance(content, str)
        self.assertTrue(len(content) > 500)
        self.assertTrue(re_search)
