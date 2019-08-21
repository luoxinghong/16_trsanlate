#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 罗兴红
@contact: EX-LUOXINGHONG001@pingan.com.cn
@file: 09_youdao.py
@time: 2019/7/24 12:28
@desc:
'''
from youdao_tr.youdao_api import youdao_tr


if __name__ == '__main__':
    with open('./data/segaa', mode='r', encoding='utf-8') as f:
        count = 1
        for line in f:
            print(count, line.replace("\n", ""), "===", youdao_tr(line.replace("\n", ""), to_lang='en'))
            count += 1
