#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: 07_baidu_js.py
@time: 2019/7/23 16:48
@desc:
'''
import json
import re
import execjs
import requests
import urllib
import logging
import os

logging.basicConfig(level=logging.ERROR,  # 控制台打印的日志级别
                    filename="./logs/" + os.path.split(__file__)[-1].split(".")[0] + ".log",
                    filemode='a',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )


class baidu_translate():
    def __init__(self):
        self.GET_URL = 'https://fanyi.baidu.com/?aldtype=16048#zh/en/'
        self.POST_URL = 'https://fanyi.baidu.com/v2transapi'

        self.HEADERS = {
            'cookie': 'PSTM=1552873591; BIDUPSID=48708A2BFAC92F364FD0CF37200AEF6E; H_WISE_SIDS=130611_126894_100806_131727_131890_126065_120173_131380_131602_131905_118894_118876_131401_118856_118832_118789_130762_131650_131576_131535_131534_131529_130222_131294_131872_131391_129565_107317_131796_131396_130125_131874_130570_131196_117333_130349_117429_131240_130076_129647_131246_127024_131436_131035_129835_129375_130412_129901_129480_129646_124030_131171_131423_132041_110085_131769_127969_131506_123290_131954_128201_131548_131827_131264_131263_128603_131038_131928_100457; BAIDUID=679C237920995A9051CF3492A63CF142:FG=1; MCITY=-340%3A; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=L48OJeC62lrsipnwblobwUEXToVpR5rTH6aozfS3xlHdHnpXW1wTEG0Pjx8g0Ku-S2EqogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0P3J; H_BDCLCKID_SF=tR-tVCtatCI3HnRv5t8_5-LH-UoX-I62aKDsKPQpBhcqEIL4hjjoej5y5pu82h5fQmTv-p5NB-TpSMbSj4Qo3fDdbNQM2JJMMGuLbhRT5p5nhMJN3j7JDMP0-xPfa5Oy523iob3vQpPMVhQ3DRoWXPIqbN7P-p5Z5mAqKl0MLIOkbC_CjT-bjjv0eUnjK46K-IKX3-b-24t_Hn7zeTr5yf4pbtbLBT5QfmJ8b40a0l5nfU5HWhOqyUnQbPnnBPjz0Coy_-taJ-chj-Ts3x6qLTKkQN3T-PKO5bRiLRoebCjBDn3oyT3JXp0nj4Rly5jtMgOBBJ0yQ4b4OR5JjxonDhOyyGCHtj-eJbIO_CvO-n5_HtJYq4bMK4FQqxby26nWyJR9aJ5nalP-DKTs2qQbjf_n-qJP0lvn5m3ion3vQpnDoljkhTJ2jj-h5f78Wp5Z5mAqKl0MLPbtbb0xynoDbbQL2fnMBMPj52OnaIQc3fAKftnOM46JehL3346-35543bRTohFLtCvjDb7GbKTD-tFO5eT22-usJHnlQhcH0hOWsIOeDtoD5P_FQP78L5J0aCohMbRkLx7MMhulDUC0DjJbDH8Ht5n-HDrKBRbaHJOoDDvRKxQcy4LdjG5x-5OAWIrf3JR7y43lsfn2bqOoeh4V3-Aq544faKJ3WJuKbqK-HqjCh-caQfbQ0-7OqP-jW5ILbK_EBn7JOpkRbUnxy50rQRPH-Rv92DQMVU52QqcqEIQHQT3mDUThDH-OJ6tttJ3KB6rtKRTffjrnhPF3X53bXP6-35KHaTreB4J8bboSDno63foi3-4ZKbKtbq37JD6yXJQRt-nSObbShR3i3T_W3-oxJpOBMnbMopvaHx8KstjvbURvDP-g3-AJQU5dtjTO2bc_5KnlfMQ_bf--QfbQ0abZqtJHKbDqoD_yJU5; delPer=0; PSINO=6; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; locale=zh; BDUSS=WQ3WlpUY1Q4a1IwWTNqckgzVDZjYUlGNk0xVFhFWXJzS1pXSVNYVkswZGZXbDVkSVFBQUFBJCQAAAAAAAAAAAEAAACQGPg01~PXqtPS1985OQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAF~NNl1fzTZdS; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; H_PS_PSSID=29548_1438_21104_29578_29522_29518_28519_29098_29568_28836_29221_26350; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1563872346,1563872350,1563878595,1563878612; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1563878612; yjs_js_security_passport=a4b1d1ec9be4db83ee04796e0741f90c92c3e8c4_1563878642_js; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D',
            'origin': 'https://fanyi.baidu.com',
            'referer': 'https://fanyi.baidu.com/?aldtype=16047',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

        self._session = requests.session()
        self._data = {
            'from': 'zh',
            'to': 'en',
            'transtype': 'realtime',
            'simple_means_flag': '3',
        }
        # 可以直接拿浏览器上的 token, 因为 token 是不变的
        self._get_token()

    def _get_token(self):
        response = requests.get('https://fanyi.baidu.com', headers=self.HEADERS)
        html = response.text
        li = re.search(r"<script>\s*window\[\'common\'\] = ([\s\S]*?)</script>", html)
        token = re.search(r"token: \'([a-zA-Z0-9]+)\',", li.group(1))
        self._data['token'] = token.group(1)

    def _get_sign(self):
        # 将 使用 js 加密的函数 copy 到 baidu_translate.js 文件中
        # 然后使用 execjs 执行
        with open('./js/baidu_translate.js') as fp:
            sign = execjs.compile(fp.read()).call('e', self._query)
            self._data['sign'] = sign

    def translate(self, query):
        self._query = query
        self._get_sign()
        self._data['query'] = self._query
        response = self._session.post(self.POST_URL, data=self._data, headers=self.HEADERS)
        content = response.content.decode()
        dict_data = json.loads(content)
        ret = dict_data['trans_result']['data'][0]['dst']
        print(query, '===', ret)


if __name__ == "__main__":
    trans = baidu_translate()
    trans.translate('百度翻译, 我在爬你')
