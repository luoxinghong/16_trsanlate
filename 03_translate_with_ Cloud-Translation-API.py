#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: use_google_api.py
@time: 2019/7/5 9:43
@desc:
'''
from google.cloud import translate


# 无法添加google cloud 的支付方式，失败品
translate_client = translate.Client()

text = u'你好世界'
target = 'en'
translation = translate_client.translate(text, target_language=target)

print(u'Text:{}'.format(text))
print(u'translation:{}'.format(translation['translatedText']))
