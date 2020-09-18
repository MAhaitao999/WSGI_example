"""
Created by HenryMa on 2020/9/4
"""

__author__ = 'HenryMa'

import time
from abc import ABC
from builtins import *

import multiprocessing

import gunicorn.app.base
from cgi import parse_qs, escape
import time


def number_of_workers():
    return 1
    # return (multiprocessing.cpu_count() * 2) + 1


def application(environ, start_response):
    # Sorting and stringifying the environment key, value pairs
    # response_body = [bytes(("%s: %s" % (key, value))) for key, value in sorted(environ.items())]
    # response_body = bytes(("%s: %s" % ('111', '222')).encode('utf-8'))
    input_data = environ['wsgi.input']
    print('wsgi.input is: ', environ['wsgi.input'])
    print('REQUEST_METHOD is: ', environ['REQUEST_METHOD'])
    print('QUERY_STRING is: ', environ['QUERY_STRING'])

    # d = parse_qs(environ['QUERY_STRING'])

    # In this idiom you must issue a list containing a default value.
    # age = d.get('age', [''])[0]  # Returns the first name value.
    # hobbies = d.get('hobbies', [])[0]  # Returns a list of hobbies.
    # print("age is: ", age)
    # print("hobbies is: ", hobbies)

    body = b''
    try:
        length = int(environ.get('CONTENT_LENGTH', '0'))
    except ValueError:
        length = 0
    if length != 0:
        t1 = time.time()
        body = environ['wsgi.input']
        # body = body.reader.read(length)
        body = body.read(length)
        print('==========', len(body))
        t2 = time.time()

    # print('resolve input data cost time is {} ms'.format((t2 - t1) * 1000))

    # print(body)

    response_body = b''
    for key, value in sorted(environ.items()):
        response_body += bytes(("%s: %s" % (key, value)).encode('utf-8')) + b'\n'
    # print(response_body)

    response_body = response_body[0:-1]
    response_body = b'Hello world'

    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]


class StandaloneApplication(gunicorn.app.base.BaseApplication, ABC):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    print(number_of_workers())
    myoptions = {
        'bind': '%s:%s' % ('127.0.0.1', '8080'),
        'workers': number_of_workers(),
    }

    StandaloneApplication(application, myoptions).run()

