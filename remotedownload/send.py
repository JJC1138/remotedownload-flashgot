#!/usr/bin/env python3

import argparse
import json
import sys

from . import *

def send():
    # [--comment COMMENT][--referer REFERER][--folder FOLDER][--fname FNAME][--headers HEADERS][--post POST][--ufile UFILE][--cfile CFILE][--ua UA]

    if len(sys.argv) == 1:
        sys.argv.append('-h')

    arg_parser = argparse.ArgumentParser()

    # - not using:
    # url: replicated in ufile in more complete format (supporting multiple files at once)
    # cookie: replicated in cfile in a more complete format
    # ulist: replicated in ufile in a more manageable format
    # rawpost: is a combination of headers and post
    # userpass: are included in the URL
    for i in fields.__dict__.values():
        arg_parser.add_argument('--%s' % i)

    args = vars(arg_parser.parse_args())

    # remove None and empty values:
    args = { k: v for k, v in args.items() if v }

    for i in ['cfile', 'ufile']:
        arg = args.get(i)
        if arg is None: continue
        with open(arg, 'rt', encoding='utf-8') as f:
            args[i] = f.read()

    args['ufile'] = args['ufile'].split()

    with open('/Users/Jon/Downloads/dllog', 'wt', encoding=encoding) as f:
        f.write(json.dumps(args))
