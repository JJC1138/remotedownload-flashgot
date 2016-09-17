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
    arg_names = StringAttributes([
        'comment',
        'referer',
        'folder',
        'fname',
        'headers',
        'post',
        'ufile',
        'cfile',
        'ua',
    ])

    for i in arg_names:
        arg_parser.add_argument('--%s' % i)

    args = vars(arg_parser.parse_known_args(argv)[0])

    # remove None and empty values:
    args = { k: v for k, v in args.items() if v }

    for i in [arg_names.cfile, arg_names.ufile]:
        arg = args.get(i)
        if arg is None: continue
        with open(arg, 'rt', encoding='utf-8') as f:
            args[i] = f.read()

    args[arg_names.ufile] = args[arg_names.ufile].split()

    arg_names_to_data_key_names = {
        arg_names.comment: field_keys.label,
        arg_names.referer: field_keys.referer,
        arg_names.folder: field_keys.folder,
        arg_names.headers: field_keys.headers,
        arg_names.post: field_keys.post_data,
        arg_names.cfile: field_keys.cookies,
        arg_names.ua: field_keys.user_agent,
    }

    data = { arg_names_to_data_key_names[k]: v for k, v in args.items() if k in arg_names_to_data_key_names.keys() }
    data[field_keys.items] = [{ item_keys.url: url } for url in args[arg_names.ufile]]

    if len(data[field_keys.items]) == 1:
        # The filename is only meaningful if we have only one item to download.
        fname = args.get(arg_names.fname)
        if fname:
            data[field_keys.items][0][item_keys.filename] = fname

    return json.dumps(data).encode(encoding)

def main():
    import sys

    arg_parser = argparse.ArgumentParser(allow_abbrev=False)
    arg_parser.add_argument('--output-file', '-o')
    args, unparsed_args = arg_parser.parse_known_args(sys.argv)

    if args.output_file:
        out = open(args.output_file, 'wb')
    else:
        out = sys.stdout.buffer

    out.write(serialize(unparsed_args))
