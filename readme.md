# German Wiktionary Parser and Dictionary Tool

⚠️ **Work in Progress** ⚠️

This project is in early development stages. While functional, it's actively evolving and may undergo significant changes. Feel free to explore and provide feedback, but please note that APIs and functionality may change without notice.

## Overview

A Python-based tool for parsing German Wiktionary dumps and storing entries in MongoDB. The main goals are to:
- Parse data from Wiktionary (primarily de.wiktionary.org)
- Store parsed data efficiently
- Enable easy queries for analysis, acronym generation, etc.

### Word Structure
Each word entry contains:
- Word text (e.g., "Affe")
- Language (e.g., "German")
- Part of speech ("Wortart", e.g., "Substantiv")
- Additional attributes (where available):
  - Hyphenation
  - Topics/categories
  - Source URLs

## Features

- Parse German Wiktionary XML dumps
- Store entries in MongoDB with language and part of speech information
- Query words by:
  ```python
  # Get German adjectives
  words = query_words(language="German", part_of_speech="Adjektiv", limit=10)
  
  # Get random word with specific topic
  search_db(topic="Culture Ship Name")
  ```
- Memory-efficient processing using generators
- Proper error handling and resource management

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure MongoDB is running locally (default: localhost:27017)

## Usage

1. Parse a Wiktionary dump:
   ```python
   from plg import parse_wikt_dump
   parse_wikt_dump("path/to/your/dump.xml")
   ```

2. Query the database:
   ```python
   from plg import query_words
   
   # Get German nouns
   words = query_words(language="German", part_of_speech="Substantiv", limit=10)
   for word in words:
       print(word)
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- German Wiktionary community


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

