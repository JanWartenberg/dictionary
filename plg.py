""" main module for crawler/dictionary lib
-> probably rather playground since it could be a sort of generic library
   and not a single script/programm """

import datetime
from pathlib import Path
import time

from crawler import Crawler

# from crawler import APK_CMTITLE, APK_CMTYPE, CAT_MEMBERS
from dictparser import (
    FunnyParser,
    FunnyParserDe,
    RobotParser,
    DeWiktParser,
    CultureShipParser,
)
from dumpparser import MediaWikiPageExtractor, MediaWikiTitleExtractor
from mongodb_connect import MongoHandler
from word import TOPICS, Word, to_words

CAT_GERMAN = "Kategorie:Deutsch"
TEMPLATE_GERMAN = "{{Sprache|Deutsch}}"
EX_CAT = "Kategorie:Präposition (Deutsch)"
EX_LEMMA = "hinsichtlich"


def bilch_similar():
    # crawl German pages
    # cr = Crawler()
    # cats = cr.get_pages_in_cat(CAT_GERMAN)

    dump_file_path = (
        r"D:\Docs\Sonstiges\dewiktionary-20220521-pages-articles-multistream_crop.xml"
    )
    with open(dump_file_path, "rb") as in_xml:
        a = list(
            MediaWikiTitleExtractor(in_xml, namespace="0", cat_filter=TEMPLATE_GERMAN)
        )

    # list all lemmas
    print(len(a))
    print(a)

    # compare for similarity
    # C:\Users\janwa\Dropbox\wichtiges\Code\win_motd\util.py
    pass


def search_db():
    mh = MongoHandler()
    res = mh.word_coll.aggregate(
        [{"$match": {TOPICS: "Culture Ship Name"}}, {"$sample": {"size": 1}}]
    )
    # for el in res:
    #     print(Word(el))
    res = to_words(list(res))
    [print(w) for w in res]


def dump():
    mh = MongoHandler()
    mh.dump(Path(__file__).parent / "dump.json")


def play_around():
    # ts = time.time()
    # cr = Crawler(lang="de", proj="wikipedia")
    # res = cr.get_pages_in_cat('Kategorie:Deutsch')
    # res = cr.get_pages_in_cat_with_sub('Kategorie:Vögel')
    # print(time.time() - ts)
    # print(len(res))
    # print([el for el in res if el.startswith("Q")])

    # microparser for name examples
    # mh = MongoHandler()
    # mh.clear_words(True)
    # mh.clear_words(timedelta=datetime.timedelta(hours=1))
    # fp = FunnyParser()
    # words = fp.parse()
    # fpde = FunnyParserDe()
    # words.extend(fpde.parse())
    # rp = RobotParser()
    # words.extend(rp.parse())

    # csn = CultureShipParser()
    # words = csn.parse()
    # for word in words:
    #     word.source = "Culture Books"
    # csn = CultureShipParser(r"name_examples\culture_shipnames_twitter.txt")
    # words_twitter = csn.parse()
    # for word in words_twitter:
    #     word.remark = word.source
    #     word.source = "Twitter @cultureshipname"
    # words.extend(words_twitter)
    #
    # for word in words:
    #     word.insert(mh)

    # parse de.wikt; only articles
    dump_file_path = (
        r"D:\Docs\Sonstiges\dewiktionary-20220521-pages-articles-multistream_crop.xml"
    )

    # with open(dump_file_path, "rb") as in_xml:
    #     for record in MediaWikiPageExtractor(in_xml, namespace="0"):
    #         dwp = DeWiktParser(record)
    #         word = dwp.parse()
    with open(
        r"C:\Users\janwa\Dropbox\wichtiges\Code\dictionary\tests\example_wikitxt.txt",
        "r",
        encoding="utf-8",
    ) as wiki_example:
        content = wiki_example.read()
        dwp = DeWiktParser(content)
        word = dwp.parse()


def play_around2():
    cat = "Kategorie:Affen"
    cr = Crawler(lang="de", proj="wikipedia")
    pages = cr.get_pages_in_cat(cat)
    print(len(pages))
    print(pages)
    pages = cr.get_pages_in_cat_with_sub(cat)
    print(len(pages))
    print(pages)
    # res = cr.get_page_content(EX_LEMMA)
    # names = [page for page in pages if "ett" in page]
    # print(names)


def translate_sightings():
    from pandas_ods_reader import read_ods
    with open(r"D:\Docs\tmp\update2.txt", "r", encoding="utf-8") as s_file:
        sichtungen = s_file.read().splitlines()
    sichtungen = set(sichtungen)
    # sichtungen.remove("")
    sichtungen = list(sichtungen)
    ods = read_ods(r"D:\Docs\Birding\Svensson_Artenliste.ods")

    for sichtung in sichtungen:
        try:
            en = ods[ods["Deutsch"] == sichtung]["Englisch"].item()
        except ValueError:
            en = None
        try:
            la = ods[ods["Deutsch"] == sichtung]["Wissenschaftlich"].item()
        except ValueError:
            la = None
        with open(r"D:\Docs\tmp\de_en", "a+", encoding="utf-8") as out_file_en:
            out_file_en.write(f"{sichtung}\t{en}\n")
        with open(r"D:\Docs\tmp\de_la", "a+", encoding="utf-8") as out_file_la:
            out_file_la.write(f"{sichtung}\t{la}\n")
        print(f"{sichtung}, {en}")


if __name__ == "__main__":
    # translate_sightings()
    # bilch_similar()
    # main()
    # for _ in range(10):
    #     search_db()
    # dump()
    play_around()