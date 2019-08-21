import grequests
import logging
import json
from googletrans import Translator
from googletrans.utils import format_json
import multiprocessing
import datetime
import os


logging.basicConfig(level=logging.ERROR,  # 控制台打印的日志级别
                    filename="./logs/" + os.path.split(__file__)[-1].split(".")[0] + ".log",
                    filemode='a',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
translator = Translator(service_urls=['translate.google.cn'])


#  调用api会被限速
def exception_handler(request, exception):
    # logging.warning('exception when at %s :%s', request.url, exception)
    logging.warning('get response error when at:%s!!%s', request.url, exception)


def work(urls):
    reqs = (grequests.get(u, verify=True, allow_redirects=True, timeout=4) for u in urls)
    res = grequests.map(reqs, exception_handler=exception_handler, size=5)
    return res


def translate():
    file = open('./res/question.merge02_res', mode='a', encoding='utf-8')
    with open('./data/question.merge02', mode='r', encoding='utf-8') as f:
        urls = []
        num = 0
        total = 0
        for line in f:
            num += 1
            line = line.strip()
            token = translator.token_acquirer.do(line)
            url = "https://translate.google.cn/translate_a/single?client=t&sl=zh-cn&tl=en&hl=en&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=3&tsel=0&kc=1&tk={0}&q={1}".format(
                token, line)
            urls.append(url)
            if len(urls) >= 50:
                res = work(urls)
                for r in res:
                    if hasattr(r, 'status_code'):
                        if r.status_code == 200:
                            try:
                                a = format_json(r.text)
                                target = ''.join([d[0] if d[0] else '' for d in a[0]])
                                source = ''.join([d[1] if d[1] else '' for d in a[0]])
                            except Exception as e:
                                logging.warning('get txt error:%s', r.text)
                                source = ''
                                target = ''
                            if len(source) != 0 and len(target) != 0:
                                file.write(source + "===" + target + "\n")
                                total += 1
                                print(total, source, "===", target)
                            else:
                                logging.warning('get txt less:%s', r.text)
                        else:
                            print('status_code is not 200 error:', r.text)
                urls = []
    file.close()


def sentencetranslate(line):
    line = line.strip()
    text = translator.translate(line, src='zh-cn', dest='en').text
    return text


if __name__ == "__main__":
    translate()



