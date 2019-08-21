# -*- coding:utf-8 -*-

import http.client
import hashlib
import urllib.request
import random
import json
import time

appid = '20190705000314976'  # 你的appid
secretKey = 'CvA9qvJnLtJsJNKol7BL'  # 你的密钥


class BaiDu(object):
    def __init__(self):
        self.httpClient = None
        self.myurl = '/api/trans/vip/translate'

    def trans(self, q='你好'):
        fromLang = 'zh'
        toLang = 'en'
        salt = random.randint(32768, 65536)
        sign = appid + q + str(salt) + secretKey
        m1 = hashlib.md5()
        b = sign.encode(encoding='utf-8')
        m1.update(b)
        sign = m1.hexdigest()
        self.myurl = self.myurl + '?appid=' + appid + '&q=' + urllib.request.quote(
            q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
        try:
            self.httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            self.httpClient.request('GET', self.myurl)
            # response是HTTPResponse对象
            response = self.httpClient.getresponse()
            w = response.read()
            r = json.loads(w.decode())
            content = r['trans_result']
            # print(content)
            return (content[0]['dst'])
        except Exception as e:
            print(e)
        finally:
            if self.httpClient:
                self.httpClient.close()


if __name__ == '__main__':
    count = 0
    w = BaiDu()
    with open('question.pattern', mode='r', encoding='utf-8') as f:
        for line in f:
            count += 1
            print(count, line.replace("\n", ""), w.trans(line.replace("\n", "")))
