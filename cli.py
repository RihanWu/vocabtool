# -*- coding: utf-8 -*-
"""CLI interface of vocabtool.

Arguments:
    * Lookup
        * Required:
            word
        * Optional:
            * language ``-l, --language``
            * source ``-s, --source``

    * Config(sub-command)
        * enable source ``-e, --enable``
        * disable source ``-d, --disable``
        * set key-value pair ``-s, --set``

    * Help
        * List dictionaries ``--list``
        * Version ``-v, --version``
"""

# Import core component
import core
import argparse


# Create the parser
parser = argparse.ArgumentParser(description="Vocab Tool")

parser.add_argument("word", help="The word you want to look up.")
parser.add_argument("-l", "--language", default="en",
                    help="Specify the language of the word.")
parser.add_argument("-s", "--source", nargs="+",
                    help="Specify the source to use")

if __name__ == "__main__":
    args = parser.parse_args()

    result = core.lookup_word(args.word, args.language, args.source)
    show = ""
    for super_entry in result:
        show = show + super_entry.show_no_style()
    if show == "":
        show = "No reponse"
    print(show)
