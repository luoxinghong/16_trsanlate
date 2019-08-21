import execjs
import os
import time
import subprocess


# 调用node运行js文件，速度有限
def translate(file):
    count = 0
    with open('./data/{}'.format(file), mode='r', encoding='utf-8') as f:
        for line in f:
            with open('index.js', "w", encoding="utf-8") as j:
                js_str = '''translate = require('google-translate-api');
    translate('%s', {to: 'en'}).then(res => {
        console.log(res.text);
        //console.log(res.from.language.iso);
    }).catch(err => {
        console.error(err);
    })
    ''' % (line.strip().replace("\n", ""))
                j.write(js_str)
                j.close()

            res = subprocess.getoutput("node index.js")
            txt = line.strip().replace("\n", "")
            # print(txt)
            # print(res)
            # print("*"*30)
            if "Error" not in res:
                count += 1
                print(count,txt,"===",res)
                with open('./res/{}_res'.format(file), mode='a', encoding='utf-8') as r:
                    r.write(txt + "===" + res + "\n")
                    r.close()
            else:
                with open('./res/{}_res'.format(file), mode='a', encoding='utf-8') as h:
                    h.write(txt + "===" + "None" + "\n")
                    h.close()


if __name__ == "__main__":
    translate("question.pattern")


