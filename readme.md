# About

This is a dictionary playground, the basic idea is:
- provide mechanism to parse data from Wiktionary (preferably de.wiktionary.org)
- stored the parsed data
- make easy queries possible for analysis, for acronym generation, ...

# Contents
## word class

Attributes:
- word: Affe
- language: Deutsch
- part of speech ("Wortart"): Substantiv
- perhaps
  - hyphenation
  - topics (category/context/topic)
  - source (where word comes from, not etymology)
  - ...

### To be clarified
- are there further attributes are needed?
- can those attributes be parsed from Wiktionary?

## crawler class
 API to (de) wiktionary
 get all entries (per language)
 get all entries (per word type)
 ...
 
## parser class
Methods (resp. classes) to parse different input

## database connect class
API to MongoDB

