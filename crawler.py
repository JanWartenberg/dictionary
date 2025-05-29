import json
import requests
import xml.etree.ElementTree as ET
from bson import json_util

# API Param Keys
APK_LIST = "list"
APK_CMCONTINUE = "cmcontinue"
APK_CMLIMIT = "cmlimit"
APK_CMPAGEID = "cmpageid"
APK_CMTITLE = "cmtitle"
APK_CMTYPE = "cmtype"  # categorymembers

APK_FORMAT = "format"
APK_TITLE = "title"

# subcategories
CAT_MEMBERS = "categorymembers"
CMTYPE_PAGE = "page"
CMTYPE_SUBCAT = "subcat"
RESP_CONT = "continue"
RESP_QUERY = "query"
RESP_CMCONT = "cmcontinue"

# API defaults
DEFAULT_LIMIT = 20
JSON = "json"

# proj defaults
DEFAULT_PROJECT = "wiktionary"
DEFAULT_LANG = "de"
API_ACTION_QUERY = "w/api.php?action=query"


class Crawler(object):
    """Collect methods to crawl data from a Wikimedia project."""

    def __init__(self, lang=None, proj=None):
        if lang is None:
            self.lang = DEFAULT_LANG
        else:
            self.lang = lang
        if proj is None:
            self.proj = DEFAULT_PROJECT
        else:
            self.proj = proj
        self.host = f"https://{self.lang}.{self.proj}.org/"

    def get_page_content(self, lemma):
        """
        Get the content (= unparsed wikitext) of a single page
        :param self:
        :param lemma: title/lemma of the page
        :return:
        """
        r = self._get_contents_parse_api(lemma)
        page = json.loads(r.text)
        try:
            ret = page["parse"]["wikitext"]
        except KeyError:
            ret = ""
        return ret

    def _get_contents_parse_api(self, lemma):
        """
        https://www.mediawiki.org/wiki/API:Get_the_contents_of_a_page
        Method 2: Use the Parse API
        :param lemma: title/lemma of the page
        :return: server's HTTP Response
        """
        url = (
            f"{self.host}/w/api.php?action=parse"
            f"&page={lemma}&prop=wikitext&formatversion=2&format=json"
            f"&redirects=1"
        )
        return requests.get(url)

    def get_interwiki_links(self, lemma):
        # Note prop=iwlinks
        #  only shows de-links..
        url = (
            f"{self.host}/w/api.php?action=parse"
            f"&page={lemma}&prop=langlinks&formatversion=2&format=json"
            f"&redirects=1"
        )
        res = requests.get(url)
        page = json.loads(res.text)
        try:
            ret = page["parse"]["langlinks"]
        except KeyError:
            ret = []
        return ret

    def get_api_request(self, cmtitle=None, cmpageid=None, **kwargs):
        """Return generic API Response
         (api.php?action=query + parameters)
        :param cmtitle: Which category to enumerate (required).
            Must include the Category: prefix.
            Cannot be used together with cmpageid.
        :param cmpageid: Page ID of the category to enumerate.
            Cannot be used together with cmtitle.
            Type: integer
        :param kwargs:
            kwargs dictionary with generic parameters:
            https://www.mediawiki.org/wiki/API:Categorymembers
        :return:
        """

        if kwargs is not None:
            params = kwargs
        else:
            params = {}

        # if pages within a category are queried
        params[APK_LIST] = CAT_MEMBERS

        if cmpageid is None:
            # Which category to enumerate (required).
            params[APK_CMTITLE] = cmtitle
        else:
            # cmpageid
            #   Page ID of the category to enumerate. Cannot be used together with cmtitle.
            #   Type: integer
            params[APK_CMPAGEID] = cmpageid

        # The maximum number of pages to return. [1, 500]
        if params.get(APK_CMLIMIT) is None:
            params[APK_CMLIMIT] = DEFAULT_LIMIT

        params[APK_FORMAT] = JSON

        resp = requests.get(url=self.host + API_ACTION_QUERY, params=params)
        # print(resp.status_code)
        return resp

    def get_pages_in_cat(self, cat):
        """
        Return list of lemmata which are in given category.
        :param cat: string of cat-lemma  (including prefix 'Kategorie:')
        :return: list of strings, i.e. of the lemmata
        """
        cm_cont = None
        lemmata = []
        params = {APK_CMTITLE: cat, APK_CMTYPE: CMTYPE_PAGE, APK_CMLIMIT: 500}

        while True:
            if len(lemmata) != 0:
                params[APK_CMCONTINUE] = cm_cont

            resp = self.get_api_request(**params)
            resp_dict = json_util.loads(resp.text)
            ls = resp_dict.get(RESP_QUERY).get(CAT_MEMBERS)
            lemmata.extend([c[APK_TITLE] for c in ls])

            try:
                cm_cont = resp_dict.get(RESP_CONT).get(RESP_CMCONT)
            except AttributeError:
                return lemmata
            if cm_cont is None:
                return lemmata

    def get_all_subcats(self, cat):
        """
        Return list of sub-categories which are in given category.
        :param cat: string of cat-lemma  (including prefix 'Kategorie:')
        :return: list of strings, i.e. of the categories
        """
        ret_val = []
        cat_lemmata = []
        params = {APK_CMTITLE: cat, APK_CMTYPE: CMTYPE_SUBCAT}
        resp = self.get_api_request(**params)
        resp_dict = json_util.loads(resp.text)
        ret_val.extend(resp_dict.get(RESP_QUERY).get(CAT_MEMBERS))
        # The next [n] subcategories can be continued using the
        # cmcontinue parameter from the response above.
        try:
            cm_cont = resp_dict.get(RESP_CONT).get(RESP_CMCONT)
        except AttributeError:
            return ret_val

        while True:
            params[APK_CMCONTINUE] = cm_cont
            resp = self.get_api_request(**params)
            resp_dict = json_util.loads(resp.text)
            ret_val.extend(resp_dict.get(RESP_QUERY).get(CAT_MEMBERS))
            try:
                cm_cont = resp_dict.get(RESP_CONT).get(RESP_CMCONT)
            except AttributeError:
                break
            if cm_cont is None:
                break

        # ret_val: contains resp_dict, but maybe only lemmata relevant
        cat_lemmata = [c[APK_TITLE] for c in ret_val]
        return cat_lemmata

    def get_pages_in_cat_with_sub(self, cat):
        """Get pages in a category, including subcats."""
        subcats = self.get_all_subcats(cat)
        try:
            subcats = [s[APK_TITLE] for s in subcats]
        except TypeError:
            pass
        res = []
        for subcat in subcats:
            res.extend(self.get_pages_in_cat_with_sub(subcat))
        res.extend(self.get_pages_in_cat(cat))
        return res
