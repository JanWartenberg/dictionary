import requests
import xml.etree.ElementTree as ET
from bson import json_util

HOST = "https://de.wiktionary.org/"
# wikt = "https://de.wiktionary.org/wiki/Spezial:Exportieren"
# filler = "/"

# defs
API_ACTION_QUERY = "w/api.php?action=query"  # Fetch data from and about MediaWiki.
# https://www.mediawiki.org/w/api.php?action=help&modules=main

# API Param Keys
APK_LIST = "list"  # https://www.mediawiki.org/w/api.php?action=help&modules=query
#   see also
#   https://www.mediawiki.org/wiki/API:Categorymembers
APK_CMTYPE = "cmtype"  # categorymembers
APK_CMTITLE = "cmtitle"
APK_CMPAGEID = "cmpageid"
APK_CMLIMIT = "cmlimit"
APK_CMCONTINUE = "cmcontinue"

APK_FORMAT = "format"

# subcategories
CMTYPE_SUBCAT = "subcat"
RESP_QUERY = "query"
RESP_CONT = "continue"
RESP_CMCONT = "cmcontinue"
CAT_MEMBERS = "categorymembers"

# API defaults
DEFAULT_LIMIT = 20
JSON = "json"


class WiktionaryApi(object):
    def __init__(self, host=HOST):
        self.host = host

    def get_page_content(self, pagename):
        url = self.host + "wiki/" + "Special:Export/" + pagename
        resp = requests.get(url=url)
        cont = ""
        # print(resp.status_code)
        # tree = ET.parse('country_data.xml')
        # root = tree.getroot()
        if resp.status_code == 200:
            root = ET.fromstring(resp.text)
            print(root.tag)
            print(root.attrib)

            parent_map = {c: p for p in root.iter() for c in p}

            # search for mediawiki.page.revision.text
            # for child in root.findall('mediawiki'):
            for child in root.iter():
                if child.tag == 'text':
                    # print(child.attrib)
                    # print(child.text)
                    cont = child.text
        return cont

    # TODO
    #  get content of normal page
    #   The Revisions API can be used to retrieve the content of a page as wikitext.
    #   This can be done by specifying the title of the page in the titles parameter
    #   and setting the rvprop parameter to content. For more options, see API:Revisions.
    #   api.php?action=query&prop=revisions&titles=Pet_door&rvslots=*&rvprop=content&formatversion=2

    #  get members of cat
    def get_api_request(self, cmtitle=None, cmpageid=None, **kwargs):
        # if cmtitle is None:
        #     cmtitle = "Kategorie:Deutsch"

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
        params[APK_CMLIMIT] = DEFAULT_LIMIT

        params[APK_FORMAT] = JSON

        resp = requests.get(url=self.host + API_ACTION_QUERY, params=params)
        # print(resp.status_code)
        return resp

    def get_all_subcats(self, cat):
        ret_val = []
        params = {APK_CMTITLE: cat, APK_CMTYPE: CMTYPE_SUBCAT}
        resp = self.get_api_request(**params)
        resp_dict = json_util.loads(resp.text)
        ret_val.extend(resp_dict.get(RESP_QUERY).get(CAT_MEMBERS))
        # "The next [n] subcategories can be continued using the cmcontinue parameter from the response above.
        cm_cont = resp_dict.get(RESP_CONT).get(RESP_CMCONT)

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

        return ret_val
