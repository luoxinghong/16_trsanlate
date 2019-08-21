#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mtranslate import translate
import os
import time
import multiprocessing
import logging
from retrying import retry
import datetime


def try_agin(res):
    if "urllib.erro" in res:
        return True
    else:
        return False


@retry(retry_on_result=try_agin, stop_max_attempt_number=3)
def get_res(data):
    res = translate(data, "en", "zh")
    return res


def crawl(file_path, res_path):
    count = 0
    with open(file_path, mode='r', encoding='utf-8') as f:
        for line in f:
            count += 1
            to_translate_data = line.strip().replace("\n", "")

            try:
                res = get_res(to_translate_data)
            except Exception as e:
                res = "None"

            line = to_translate_data + "===" + res + "\n"
            print(count, line.replace("\n", ""))
            with open(res_path, "a", encoding="utf-8") as g:
                g.write(line)
                g.close()


if __name__ == "__main__":
    data_dir = r"C:\Users\my\Desktop\SPIDER\19_翻译\split_files"
    res_dir = r"C:\Users\my\Desktop\SPIDER\19_翻译\zh_to_en"

    files = [os.path.join(data_dir, file_name) for file_name in os.listdir(data_dir)]
    res_files = [os.path.join(res_dir, file_name) for file_name in os.listdir(data_dir)]

    p = multiprocessing.Pool(processes=5)
    for index, file_path in enumerate(files):
        p.apply_async(crawl, args=(file_path, res_files[index]))
    p.close()
    p.join()


    # 单文件，单进程
    # data_file = r"C:\Users\my\Desktop\SPIDER\19_翻译\data\segaa"
    # res_dir = "/home/lxh/mtranslate/zh_to_en"
    # crawl(data_file, res_dir)
