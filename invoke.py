#! /usr/bin/env python3

"The command line argument parser to invoke specific action."

import sys


def lookup_single_word(word):
    import core
    result = core.lookup_word(word, "en")
    show = ""
    for super_entry in result:
        show += super_entry.show_no_style()
    if show == "":
        show = "No response"
    return show


def cli_interface():
    # TODO: Implement CLI

    print("This is the CLI interface of vocabtool")

    while(True):
        word = input("Please input the word to lookup[English]:")
        print(lookup_single_word(word))


def check_dict(argv):
    args = list(argv)
    result = []
    for item in ['-d', '--dict', '--dictionary']:
        while item in args:
            result.append(args[args.index(item)+1])
            args.remove(result[-1])
            args.remove(item)
    return result


def get_param(argv, keys, default):
    args = list(reversed(argv))
    result = default
    lastOccur = len(args)
    for item in keys:
        if item in args:
            if lastOccur > args.index(item):
                lastOccur = args.index(item)
                result = args[lastOccur - 1]
            args.remove(args[args.index(item) - 1])
            args.remove(item)
    return result


def check_format(args):
    keys = ['-f', '--format']
    default = 'text'
    return get_param(args, keys, default)


def check_output(args):
    keys = ['-o', '--output']
    default = 'stdout'
    return get_param(args, keys, default)


def parse_args(args):
    result = {}
    if len(args) == 0 or args[0] == '-i':
        result['action'] = 'cli'  # Enter text-interactive mode
    elif args[0] in ['-h', '--help', '-?']:
        result['action'] = 'help'  # Print help message
    elif args[0] in ['-l', '--list']:
        result['action'] = 'dict'  # Print all dictionaries
    else:
        result['action'] = 'look'
        result['dict'] = check_dict(args)  # Specify Dictionary
        result['format'] = check_format(args)  # Specify Format
        result['output'] = check_output(args)
        result['word'] = args[-1]  # The word to look up
    return result


def print_help():
    print('VocabTool\n\nusage:\t' +
          sys.argv[0] +
          ' [-h | -i | -l]\n\t' +
          sys.argv[0] +
          ' [-d Dictionary] [-f Format] [-o Output] word\n\n' +
          '\td: Specify which dictionary to use. Use multiple times\n' +
          '\t   to specify multiple dictionaries. Default: all.\n' +
          '\tf: Specify which format the output should be. Available\n' +
          '\t   choices: text, rtf, pdf. Default: text.\n' +
          '\th: Print this help message.\n' +
          '\ti: Invoke interactive text interface.\n' +
          '\tl: List all of the available dictionaries.\n' +
          '\to: Specify the output file. Default: standard output.')


def print_dict():
    import json
    config_filename = "config.json"
    with open(config_filename, "rb") as handle:
        content = handle.read().decode("utf-8")
        config = json.loads(content)
    for dictionary in config:
        if dictionary["enable"]:
            print(dictionary["id"])


def main(args):
    result = parse_args(args)
    if result['action'] == 'help':
        print_help()
    elif result['action'] == 'cli':
        cli_interface()
    elif result['action'] == 'dict':
        print_dict()
    else:
        # TODO: Invoke core here.
        print(lookup_single_word(result['word']))

if __name__ == '__main__':
    main(sys.argv[1:])
