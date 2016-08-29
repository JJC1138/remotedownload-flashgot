import cgi
import email.parser
import http.cookiejar
import json
import os
import os.path
import posixpath
import sys
import tempfile
import urllib.parse

import requests

from . import *

def get():
    # - Unused parameters:
    # comment
    # folder
    with open(sys.argv[1], 'rt', encoding=encoding) as f: data = json.load(f)

    session = requests.Session()
    session.headers.update({
        'Referer': data[fields.referer],
        'User-Agent': data[fields.user_agent],
    })

    cookies_txt = data.get(fields.cookies_txt)
    if cookies_txt:
        cookies_file = tempfile.NamedTemporaryFile('wt', encoding='utf-8', delete=False)
        cookies_file.write(http.cookiejar.MozillaCookieJar.header)
        cookies_file.write(cookies_txt)
        cookies_file.close()

        cookie_jar = http.cookiejar.MozillaCookieJar()
        cookie_jar.load(cookies_file.name)

        os.remove(cookies_file.name)

        session.cookies = cookie_jar

    session.stream = True

    headers_string = data.get(fields.headers)
    if headers_string:
        headers = email.parser.Parser().parsestr(headers_string)
        session.headers.update(headers)

    for url in data[fields.urls]:
        post = data.get(fields.post)
        if post:
            response = session.post(url, data=post, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        else:
            response = session.get(url)

        response.raise_for_status()

        out_file = tempfile.NamedTemporaryFile('wb', suffix='.remotedownload', dir=os.getcwd(), delete=False)
        for chunk in response.iter_content(4096):
            out_file.write(chunk)
        out_file.close()

        filename = cgi.parse_header(response.headers.get('Content-Disposition', ''))[1].get('filename')
        if filename:
            filename = os.path.basename(filename)
        else:
            # Guess it from the URL
            filename = posixpath.basename(urllib.parse.unquote(urllib.parse.urlparse(response.url).path))

        if not filename:
            if len(data[fields.urls]) == 1:
                filename = os.path.basename(data.get(fields.filename, ''))

        if filename:
            final_filename = filename
            duplicate_number = 2
            while True:
                # Make sure the file doesn't exist already
                try:
                    final_file = open(final_filename, 'xb')
                    final_file.close()
                    break
                except:
                    root, ext = os.path.splitext(filename)
                    final_filename = '%s %d%s' % (root, duplicate_number, ext)
                    duplicate_number += 1

            if sys.platform.startswith('win32'):
                # Windows will fail if the file exists so:
                os.remove(final_filename)

            os.rename(out_file.name, final_filename)

            final_filename = os.path.abspath(final_filename)
        else:
            final_filename = out_file.name

        log(final_filename)
