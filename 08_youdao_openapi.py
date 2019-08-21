#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: 08_youdao.py
@time: 2019/7/24 9:25
@desc:
'''
import time
import uuid
import hashlib
import requests
import json


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def encrypt(signStr):  # sha256加密
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def compose_data(line_data):
    APP_SECRET = '8z6MGtGsyVoervF5Fk3yET4xsNOqgjet'
    APP_KEY = '2ba19d7e3ed057cf'
    data = {}
    data['from'] = 'zh'
    data['to'] = 'en'
    data['signType'] = 'v3'
    data['appKey'] = APP_KEY

    salt = str(uuid.uuid1())
    curtime = str(int(time.time()))
    signStr = APP_KEY + truncate(line_data) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['curtime'] = curtime
    data['sign'] = sign
    data['salt'] = salt
    data['q'] = line_data
    return data


if __name__ == '__main__':
    YOUDAO_URL = 'http://openapi.youdao.com/api'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    with open('./data/segaa', mode='r', encoding='utf-8') as f:
        count = 1
        for line in f:
            line_data = line.replace("\n", "")
            data = compose_data(line_data)
            result = requests.post(YOUDAO_URL, data=data, headers=headers).text
            print(count, line.replace("\n", ""), "===", json.loads(result)["translation"][0])
            count += 1
