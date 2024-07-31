import fugashi
import json
import urllib.parse
import pprint

import os

tagger = fugashi.Tagger('-Owakati')

def parseText(text, fields):
    if fields is None:
        fields = ['pos1', 'pos2', 'pos3', 'pos4', 'lemma', 'orthBase', 'kanaBase', 'cType', 'cForm', 'type']

    results = []
    for node in tagger.parseToNodeList(text):
        # @see 列名については https://clrd.ninjal.ac.jp/unidic/faq.html#col_name
        token = {
            'text': str(node),
        }
        for field in fields:
            token[field] = getattr(node.feature, field, None)

        results.append(token)
    return results

def errorResponse(start_response, message):
    headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(message))),
    ]
    start_response(message, headers)
    return [message.encode('utf-8')]

def application(environ, start_response):
    if environ['PATH_INFO'] == '/healthz':
        start_response('200 OK', [
            ('Content-Type', 'text/plain'),
            ('Content-Length', '0'),
        ])
        return []

    # 404 Not Found except for root access.
    if environ['PATH_INFO'] != '/':
        return errorResponse(start_response, '404 Not Found')

    query = urllib.parse.parse_qs(environ['QUERY_STRING'])
    env_secret = os.environ.get('SECRET')

    # Check SECRET env if present.
    if env_secret is not None:
        query_secret = query.get('secret', [None])[-1]
        if env_secret != query_secret:
            return errorResponse(start_response, '400 Bad Request')

    # 400 Bad Request if no text parameter.
    if query.get('text') is None:
        return errorResponse(start_response, '400 Bad Request')

    text = query.get('text')[-1]
    fields = None
    if query.get('fields') is not None:
        fields = query.get('fields')[-1].split(',')

    output = json.dumps(parseText(text, fields), ensure_ascii=False)
    start_response('200 OK', [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(output.encode('utf-8')))),
    ])
    return [output.encode('utf-8')]
