import datetime

from wikt_api import WiktionaryApi
from mongodb_connect import MongoHandler
from word import Word


def main():
    wa = WiktionaryApi()
    mh = MongoHandler()
    cat_german = "Kategorie:Deutsch"
    # content = wa.get_page_content(cat_german)
    # print(content)
    # res = wa.get_all_subcats(cat_german)
    # print(res)

    # w = Word("word_template.json")
    # w.word = "Hans"
    # ret = w.insert(mh)
    # word_list = mh.find_recent_words()
    # for el in word_list:
    #     print(el.data['_id'].generation_time, el)

    word_list = mh.find_words_from_n_minutes_ago(65)
    for el in word_list:
        print(el.data['_id'].generation_time, el)


if __name__ == "__main__":
    main()
