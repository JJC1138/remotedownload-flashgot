#!/usr/bin/env python3

import argparse
import json

from . import *

def serialize(argv):
    # [--comment COMMENT][--referer REFERER][--folder FOLDER][--fname FNAME][--headers HEADERS][--post POST][--ufile UFILE][--cfile CFILE][--ua UA]
    arg_parser = argparse.ArgumentParser(allow_abbrev=False)

    # - not using:
    # url: replicated in ufile in more complete format (supporting multiple files at once)
    # cookie: replicated in cfile in a more complete format
    # ulist: replicated in ufile in a more manageable format
    # rawpost: is a combination of headers and post
    # userpass: are included in the URL
    for i in fields.__dict__.values():
        arg_parser.add_argument('--%s' % i)

    args = vars(arg_parser.parse_known_args(argv)[0])

    # remove None and empty values:
    args = { k: v for k, v in args.items() if v }

    for i in ['cfile', 'ufile']:
        arg = args.get(i)
        if arg is None: continue
        with open(arg, 'rt', encoding='utf-8') as f:
            args[i] = f.read()

    args['ufile'] = args['ufile'].split()

    return json.dumps(args)

def main():
    import sys

    arg_parser = argparse.ArgumentParser(allow_abbrev=False)
    arg_parser.add_argument('--output-file', '-o')
    args, unparsed_args = arg_parser.parse_known_args(sys.argv)

    if args.output_file:
        out = open(args.output_file, 'wt', encoding=encoding)
    else:
        out = sys.stdout

    out.write(serialize(unparsed_args))