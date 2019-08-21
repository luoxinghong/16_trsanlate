# -*- coding:utf-8 -*-
from datetime import datetime
import os


def Main(source_file, target_dir, count):
    # 计数器
    flag = 0

    # 文件名
    num = 1

    # 存放数据
    dataList = []

    print("开始=====", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    with open(source_file, 'r', encoding="utf-8") as f_source:
        for line in f_source:
            flag += 1
            dataList.append(line)
            if flag == count:
                split_file_name = os.path.basename(source_file) + "{:0>2}".format(num)
                print(split_file_name)
                with open(os.path.join(target_dir, split_file_name), 'w+', encoding="utf-8") as f_target:
                    for data in dataList:
                        f_target.write(data)
                num += 1
                flag = 0
                dataList = []

    # 处理最后一批行数少于count行的
    with open(target_dir + "question.pattern_zh_{:0>2}".format(num), 'w+', encoding="utf-8") as f_target:
        for data in dataList:
            f_target.write(data)

    print("完成。。。。。", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    source_file = r"C:\Users\my\Desktop\SPIDER\19_翻译\data\segaa"
    target_dir = r"C:\Users\my\Desktop\SPIDER\19_翻译\split_files"
    count = 50000
    Main(source_file, target_dir, count)
