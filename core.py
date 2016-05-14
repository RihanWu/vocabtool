# -*- coding: utf-8 -*-
"""VocabTool core module

This is the core module of 'VocabTool'.
It connects the other modules with each other.
"""
# Standard module
import json

# Local modules
import database
import generate


# Read config from external config file
config_filename = "config.json"
with open(config_filename, "rb") as handle:
    content = handle.read().decode("utf-8")
    config = json.loads(content)

# Load enabled dictionary
loaded_dict = list()  # (module, dictionary configuration)
for dictionary in config:
    if dictionary["enable"]:
        loaded_dict.append((__import__("dict."+dictionary["id"],
                                       fromlist=["*"]),
                           dictionary))

# Current word object
current_word = list()


def lookup_word(word_text, search_language, source_list=None):
    """Look up word in sources as configed."""

    # Reset current word
    current_word = list()

    # Lookup in loaded dictionaries
    for source in loaded_dict:
        if source[1]["lang"] == search_language:
            if source_list:
                if source[1]["id"] in source_list:
                    current_word.append(source[0].lookup(source[1], word_text))
            else:
                current_word.append(source[0].lookup(source[1], word_text))

    # Return to GUI
    return current_word


def add_to_database():
    """Add the current word to database."""

    response = database.add(current_word)


def generate_pdf():
    """Generate pdf that meets the requirement."""

    response = generate.generate_pdf()
