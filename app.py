import fugashi
import json
import urllib.parse
import pprint

import os

def parseText(text):
    tagger = fugashi.Tagger('-Owakati')
    results = []
    for node in tagger.parseToNodeList(text):
        # @see 列名については https://clrd.ninjal.ac.jp/unidic/faq.html#col_name
        results.append({
            'text': str(node),
            'pos1': node.feature.pos1,         # 品詞大分類
            'pos2': node.feature.pos2,         # 品詞中分類
            'pos3': node.feature.pos3,         # 品詞小分類
            'pos4': node.feature.pos4,         # 品詞細分類
            'lemma': node.feature.lemma,       # 語彙素 (＋語彙素細分類)
            'orthBase': node.feature.orthBase, # 書字形基本形
            'kanaBase': node.feature.kanaBase  # 仮名形基本形
        })
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

    output = json.dumps(parseText(text), ensure_ascii=False)
    start_response('200 OK', [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(output.encode('utf-8')))),
    ])
    return [output.encode('utf-8')]
