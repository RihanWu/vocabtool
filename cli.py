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
import pprint


# Create the parser
parser = argparse.ArgumentParser(description="Vocab Tool")

# Top level options
parser.add_argument("-v", "--version",
                    action="store_true",
                    dest="show_version")
subparsers = parser.add_subparsers(dest="subcmd")

# Lookup argument group
parser_lookup = subparsers.add_parser("lookup", aliases=["-"])
parser_lookup.add_argument("word",
                           help="The word you want to look up.")
parser_lookup.add_argument("-l", "--language",
                           default="en",
                           help="Specify the language of the word.")
parser_lookup.add_argument("-s", "--source",
                           nargs="+",
                           help="Specify the source to use")

# Config argument group
parser_config = subparsers.add_parser("config")
parser_config.add_argument("-r", "--read",
                           dest="read_arg")
parser_config.add_argument("-w", "--write",
                           nargs=2,
                           dest='write_arg')
parser_config.add_argument("-e", "--enable",
                           nargs="+",
                           dest="enable_list",
                           help="Enable one or more dictionary sources by IDs")
parser_config.add_argument("-d", "--disable",
                           nargs="+",
                           dest="disable_list",
                           help="Disable one or more dictionary sources by IDs")

if __name__ == "__main__":
    args = parser.parse_args()

    # Config pprint
    pp = pprint.PrettyPrinter()

    # Initialize core
    vt = core.VocabTool()

    if args.subcmd in ["lookup", "-"]:
        result = vt.look_up_word(args.word, args.language, args.source)
        show = ""
        for super_entry in result:
            show = show + super_entry.show_no_style()
        if show == "":
            show = "No reponse"
        print(show)
    elif args.subcmd == "config":
        if args.read_arg or args.write_arg:
            # Read and write should not be excuting together
            if args.read_arg:
                pp.pprint(vt.read_config(args.read_arg))
            elif args.write_arg:
                vt.write_config(*args.write_arg)
        elif args.enable_list or args.disable_list:
            # Enable and disable can be excuting together
            if args.enable_list:
                for item in args.enable_list:
                    vt.write_config(".".join(["dictionaries", item, "enable"]),
                                    True)
            if args.disable_list:
                for item in args.disable_list:
                    vt.write_config(".".join(["dictionaries", item, "enable"]),
                                    False)
    elif args.show_version:
        print("Version:" + core.__version__)
