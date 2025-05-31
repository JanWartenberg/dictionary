# TODO
## general

- mal sortieren
- was habe ich schon?
- was will ich noch?
- **was sind die nächsten Schritte?**
- evtl.:
  - Methode, alle Lemmata einer Kategorie ziehen
  - darauf Ähnlichkeitsmethode ziehen
    (Beispiel: alle Wörter, die "Bilch" ähneln)

## word class
Clarify: what about "names"? (special case of noun?)
either "part of speech"->"name"
either "part of speech"->"noun"  + further attribute

## special: Greek / Latin
https://en.wikipedia.org/wiki/List_of_Greek_and_Latin_roots_in_English/A
    -> parsen
(von A-Z) ..

## parse Wikt
consider how/if de-Wikt can be parsed
- within parser class

## Generator class
- name generator  (i.e. criteria: category, ...)
- backronym generator  (params:  backronym, categories, language, ...)

## Parse out of XML
Try to parse of XML: easy? quick?
https://stackoverflow.com/questions/16533153/parse-xml-dump-of-a-mediawiki-wiki
-> looks a bit nasty, but I have a method to get the page content
-> and way quicker than using the REST API (1)
-> any WikiText-Parsing can be built upon that

(1) crawl everything from Kategorie:Deutsch
    (just the lemma names - not the content!)
    456 s  = nearly 8 min.
        703350 entries
    -> and that is just Kategorie:Deutsch...
