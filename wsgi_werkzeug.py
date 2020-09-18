"""
Created by HenryMa on 2020/9/16
"""

__author__ = 'HenryMa'

import sys
import time
from builtins import *
from cgi import parse_qs

from werkzeug.serving import run_simple


def application(environ, start_response):
    # Sorting and stringifying the environment key, value pairs
    # response_body = [bytes(("%s: %s" % (key, value))) for key, value in sorted(environ.items())]
    # response_body = bytes(("%s: %s" % ('111', '222')).encode('utf-8'))
    # environ['wsgi.input'] = sys.stdin.buffer
    input_data = environ['wsgi.input']

    t1 = time.time()
    body = b''
    try:
        length = int(environ.get('CONTENT_LENGTH', '0'))
    except ValueError:
        length = 0
    if length != 0:
        body = environ['wsgi.input'].read(length)

    t2 = time.time()

    print('resolve input data cost time is {} ms'.format((t2 - t1) * 1000))

    # print(body)
    print('wsgi.input is: ', environ['wsgi.input'])
    print('REQUEST_METHOD is: ', environ['REQUEST_METHOD'])
    print('QUERY_STRING is: ', environ['QUERY_STRING'])

    # d = parse_qs(environ['QUERY_STRING'])
    #
    # # In this idiom you must issue a list containing a default value.
    # age = d.get('age', [''])[0]  # Returns the first name value.
    # hobbies = d.get('hobbies', [])[0]  # Returns a list of hobbies.
    # print("age is: ", age)
    # print("hobbies is: ", hobbies)
    response_body = b''
    for key, value in sorted(environ.items()):
        response_body += bytes(("%s: %s" % (key, value)).encode('utf-8')) + b'\n'
    # print(response_body)

    response_body = response_body[0:-1]

    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]


if __name__ == '__main__':
    run_simple('127.0.0.1', 8080, application)
