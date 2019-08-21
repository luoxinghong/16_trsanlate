----
tags: python, requests, json, pyexecjs
----
爬虫最重要的就是反反爬虫, 所谓的反反爬虫就是针对反爬虫做出应对的策略, 从而照样爬取数据. 但前提是要了解反爬虫的策略.


1. User-Agent + Referer检测
2. Cookie验证
3. 验证码
4. IP限制频次
5. js 渲染
6. ajax 异步传输数据




## 1. 百度爬虫准备

```python
pip install requests
pip install PyExecJs
```
`PyExecJs` 是一个使用 python 执行 js 代码的模块. 像这样的模块还有 `js2py`, `phantomjs`, `selenium` 等

## 2. 寻找请求信息
### 2.1 get
打开百度翻译网站就发现发现它的 url 是: https://fanyi.baidu.com/?aldtype=16047#auto/zh
所以不难看出这是一个 get 请求的 url, 应该可以在开发者工具中找到 `?aldtype=16047` 文件, 如下图示:

![?aldtype=16047](https://img2018.cnblogs.com/blog/1692539/201907/1692539-20190718233713859-1316318731.png)

所有的get 请求相关的信息, 都可以在这里获取了.

### 2.2 post
而 get 肯定不是我们真正要找的 url, 在线翻译的网站, 一般都会通过 post 请求实现实时翻译. 那么, 我们就需要在开发者工具中继续找有 post 请求的文件.
不小心发现一个叫 `verify?token=` 什么什么的文件是一个 post 请求的, 但状态码 `Status Code` 不是请求错误(403), 就是重定向(302). 所以不是我们要找的.
遇到这样的问题, 一般情况下先提交一下翻译的内容, 然后再去抓包工具里(开发者工具)看, 发现一个叫 `v2transapi` 的文件是我们所要寻找的.
所以我们可以在这里索取我们想要的`post`信息, 真正要找的`post`请求url是: https://fanyi.baidu.com/v2transapi.
然而, 啪啪啪…, 写完代码之后, 解析得到的信息是含有 `error`的. 说明有问题.

于是乎, 在开发者工具中, 怒怼`ctrl+shift+f`键, 在search 输入框中输入 `v2transapi`, 接着怼回车, 双击查找到的结果, 好像发现了一些端倪.
里面包藏着乱七八糟的 js 代码, 有点晕, 还不知道到底是不是所要找的内容, 但这是目前唯一掌握的线索了, 还是要坚持看一看.
果不其然, 看到了熟悉又陌生的内容 `$.ajax({type:"POST",url:"/v2transapi",cache:!1,data:p})`.
据分析(ps: 如果不想一步步往下分析, 那么可以在那一行打个断点), 里面的 data 对应的内容 p, 是我们的下一个线索.
既然它可以使用 p 变量, 那么 p 肯定是已经被赋值了的, 那么网上一找应该就不难发现 p: `p={from:g.fromLang,to:g.toLang,query:a,transtype:n,simple_means_flag:3,sign:m(a),token:window.common.token};`
有些似曾相识啊. 据分析, 这个 p 正是我们的 `form data`, 各个参数都一样, 如下图所示:

![form data](https://img2018.cnblogs.com/blog/1692539/201907/1692539-20190719001200133-1477600728.png)

这么多数据, 哪一个才是我们最需要关心的呢? 自然是`sign`, 因为它貌似使用了 m 函数来加密了, 而且在之前的分析步骤中, 可以发现它是一个可变数据, 其他的参数是不变的，可以直接从抓包工具上获取.
所以我们要进一步去分析 `sign`.
在 `$.ajax({type:"POST",url:"/v2transapi",cache:!1,data:p})` 处打个断点, 然后再翻译的输入框中, 随便输入要翻译的内容, 这时候进入了调试的状态.
接着寻找刚才找到的 m 函数之处, 鼠标移动到 m 之上, 发现弹出的是这样的内容, 如下图:

![](https://img2018.cnblogs.com/blog/1692539/201907/1692539-20190719003443601-627880792.png)

说明 m 指向的是与 e 函数相关的, 接着我们把 e 函数相关的内容拷贝下来, 存到一个.js 文件中, 然后使用 execjs 来执行 js 代码即可.

## 3. 上代码
### 3.1 py 文件
```python
import json
import re

import execjs
import js2py
import requests


class baidu_translate():
    def __init__(self):
        self.GET_URL = 'https://fanyi.baidu.com/?aldtype=16047#zh/en/'
        self.POST_URL = 'https://fanyi.baidu.com/v2transapi'

        self.GET_HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0', 'Accept': '*/*', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Host': 'fanyi.baidu.com', 'Origin': 'https://fanyi.baidu.com', 'Referer': 'https://fanyi.baidu.com/', 'X-Requested-With': 'XMLHttpRequest',
            # 'cookie': '',
        }
        self.POST_HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'fanyi.baidu.com',
            'Origin': 'https://fanyi.baidu.com',
            'Referer': 'https://fanyi.baidu.com/?aldtype=16047',
            'X-Requested-With': 'XMLHttpRequest',
        }

        self._session = requests.session()
        self._data = {
            'from': 'zh',
            'to': 'en',
            'transtype': 'realtime',
            'simple_means_flag': '3',
            # 'query': '',  # 要翻译的词或句, 变项
            # 'sign': '',  # Ajax(js) 加密, 变项
            # 'token': '',  # 不变项
        }
        # 可以直接拿浏览器上的 token, 因为 token 是不变的
        self._get_token()

    def _get_token(self):
        response = self._session.get(self.GET_URL, headers=self.GET_HEADERS)
        html = response.text
        li = re.search(r"<script>\s*window\[\'common\'\] = ([\s\S]*?)</script>", html)
        token = re.search(r"token: \'([a-zA-Z0-9]+)\',", li.group(1))
        self._data['token'] = token.group(1)

    def _get_sign(self):
        # 将 使用 js 加密的函数 copy 到 baidu_translate.js 文件中
        # 然后使用 execjs 执行
        with open('baidu_translate.js') as fp:
            sign = execjs.compile(fp.read()).call('e', self._query)
            self._data['sign'] = sign

    def translate(self, query):
        self._query = query
        self._get_sign()
        self._data['query'] = self._query
        print(self._data)
        response = self._session.post(self.POST_URL, data=self._data, headers=self.POST_HEADERS)
        content = response.content.decode()
        dict_data = json.loads(content)
        # print(dict_data)
        ret = dict_data['trans_result']['data'][0]['dst']
        print(ret)


if __name__ == "__main__":
    trans = baidu_translate()
    trans.translate('百度翻译, 我在爬你')

```

### 3.2 js 文件

```javascript
var i = "320305.131321201"

function a(r){if(Array.isArray(r)){for(var o=0,t=Array(r.length);o<r.length;o++)t[o]=r[o];
return t}return Array.from(r)}

function n(r,o){for(var t=0;t<o.length-2;t+=3){var a=o.charAt(t+2);a=a>="a"?a.charCodeAt(0)-87:Number(a),a="+"===o.charAt(t+1)?r>>>a:r<<a,r="+"===o.charAt(t)?r+a&4294967295:r^a
}return r}

function e(r) {
        var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
        if (null === o) {
            var t = r.length;
            t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr( - 10, 10))
        } else {
            for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)"" !== e[C] && f.push.apply(f, a(e[C].split(""))),
            C !== h - 1 && f.push(o[C]);
            var g = f.length;
            g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice( - 10).join(""))
        }
        var u = void 0,
        l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
        u = null !== i ? i: (i = window[l] || "") || "";
        for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
            var A = r.charCodeAt(v);
            128 > A ? S[c++] = A: (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)), S[c++] = A >> 18 | 240, S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224, S[c++] = A >> 6 & 63 | 128), S[c++] = 63 & A | 128)
        }
        for (var p = m,
        F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++) p += S[b],
        p = n(p, F);
        return p = n(p, D),
        p ^= s,
        0 > p && (p = (2147483647 & p) + 2147483648),
        p %= 1e6,
        p.toString() + "." + (p ^ m)
    }
```

### 