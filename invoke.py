#! /usr/bin/env python3

"The command line argument parser to invoke specific action."

import sys

def cliInterface():
    # TODO: Implement CLI
    # Import core component
    import core

    print("This is the CLI interface of  vocabtool")

    while(True):
        word = input("Please input the word to lookup[English]:")
        result = core.lookup_word(word, "en")
        show = ""
        for super_entry in result:
            show = show + super_entry.show_no_style()
        if show == "":
            show = "No reponse"
        print(show)

def checkDict(argv):
    args=list(argv)
    result = []
    for item in ['-d','--dict','--dictionary']:
        while item in args:
            result.append(args[args.index(item)+1])
            args.remove(result[-1])
            args.remove(item)
    return result

def getParam(argv,keys,default):
    args = list(reversed(argv))
    result = default
    lastOccur = len(args)
    for item in keys:
        while item in args:
            if lastOccur > args.index(item):
                lastOccur = args.index(item)
                result = args[lastOccur -1]
            args.remove(args[args.index(item)-1])
            args.remove(item)
    return result

def checkFormat(args):
    keys = ['-f','--format']
    default = 'text'
    return getParam(args,keys,default)

def checkOutput(args):
    keys = ['-o','--output']
    default = 'stdout'
    return getParam(args,keys,default)

def parseArgs(args):
    result = {}
    if len(args) == 0 or args[0] == '-i':
        result['action']='cli' # Enter text-interactive mode
    elif args[0] in ['-h','--help','-?']:
        result['action']='help' # Print help message
    elif args[0] in ['-l','--list']:
        result['action']='dict' # Print all available dictionaries
    else:
        result['action']='look'
        result['dict']=checkDict(args) # Specify Dictionary - Return a list
        result['format']=checkFormat(args) # Specify Format
        result['output']=checkOutput(args)
        result['word']=args[-1] # The word to look up is always at the end.
    return result

def printHelp():
    print('VocabTool\n\nusage:\t'+sys.argv[0]+' [-h | -i | -l]\n\t'+sys.argv[0]+' [-d Dictionary] [-f Format] [-o Output] word\n')
    print('\td: Specify which dictionary to use. Use multiple times\n\t   to specify multiple dictionaries. Default: all.')
    print('\tf: Specify which format the output should be. Available\n\t   choices: text, rtf, pdf. Default: text.')
    print('\th: Print this help message.')
    print('\ti: Invoke interactive text interface.')
    print('\tl: List all of the available dictionaries.')
    print('\to: Specify the output file. Default: standard output.')

def main(args):
    result = parseArgs(args)
    if result['action']=='help':
        printHelp()
    elif result['action']=='cli':
        cliInterface()
    else:
        # TODO: Invoke core here.
        print(result)

if __name__ == '__main__':
    main(sys.argv[1:])