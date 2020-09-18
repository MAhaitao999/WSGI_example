"""
Created by HenryMa on 2020/9/16
"""

__author__ = 'HenryMa'


import sys
import json
import os
import time
import base64
from builtins import *
import cv2

import numpy as np
import http.client


if __name__ == '__main__':
    conn = http.client.HTTPConnection('127.0.0.1', 8080)
    header = {'Content-type': 'application/octet-stream', 'Connection': 'keep-alive'}

    img = cv2.imread('mug.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (1080, 720))
    img_string = img.tostring()
    img_shape = [1080, 720, 3]

    d = {'client_id': '1234', 'shape_of_images': [img_shape, img_shape, img_shape]}
    json_d = json.dumps(d)
    bytes_d = bytes(json_d, encoding='utf-8')

    offset = len(bytes_d) + 4
    # print(offset)
    offset_bytes = offset.to_bytes(4, byteorder='little', signed=True)

    # print(offset_bytes)

    send_bytes = offset_bytes + bytes_d + img_string + img_string + img_string

    # print(send_bytes)

    start_time = time.time()
    # conn.request('POST', '/', bytes(1024 * 1024 * 10 * 'a', encoding='utf-8'), header)
    conn.request('POST', '/', send_bytes, header)
    response = conn.getresponse()
    end_time = time.time()
    print('cost time is {} ms'.format((end_time - start_time) * 1000))
    res = response.read()
    print("****** 返回结果 ******")
    print(res.decode())

