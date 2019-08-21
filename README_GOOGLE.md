***********项目目标***********
尽可能快的爬取google翻译zh-CN转en



***********实现方式一***********
①npm install --save google-translate-api
②安装好包，然后在node_modules目录下找到google-translate-api和google-translate-token这两个文件夹，将里面index.js里的几个https://translate.google.com全部替换为 https://translate.google.cn，就能不翻墙使用这个谷歌翻译api了，跟cn网站那个是同一个服务器。
需要替换域名的两个文件路径为：node_modules/google-translate-api/index.js 和 node_modules/google-translate-token/index.js
③index.js:
translate = require('google-translate-api');

translate('请问如何调用谷歌翻译API', {to: 'en'}).then(res => {
    console.log(res.text);
    //=> I speak English
    console.log(res.from.language.iso);
    //=> nl
}).catch(err => {
    console.error(err);
});
④执行$ node index.js    正常的话就会打印出>>>
How to call Google Translate API
zh-CN

参考地址：https://www.npmjs.com/package/google-translate-api
安装node https://www.jianshu.com/p/a86a62484915

不足：效率不高



***********实现方式二***********
使用python库googletrans

但是在面对大规模需要翻译的句子时就会很慢，所以可以使用协程的方法。
这里我们使用了基于gevents库的grequests库。
仔细看了下googletrans库的核心代码，发现主要是构造一个url，然后发起get请求，得到一个json的结果，从中提取出翻译结果。
构造url的过程需要一个token，根据某些规则生成，所以为了方便还是调用googletrans的部分函数。
具体的参考代码如

①pip3 install googletrans
②#使用方法
from googletrans import Translator
translator = Translator(service_urls=['translate.google.cn'])
source = '我还是不开心！'
text = translator.translate(source,src='zh-cn',dest='en').text
print(text)

"i'm still not happy!"
不足：会被识别限速



***********实现方式三***********
使用google的收费Cloud Translation API  
参考地址：https://cloud.google.com/translate/docs/translating-text
https://cloud.google.com/sdk/docs/quickstart-windows?hl=zh-CN
不足：可惜需要创建项目，绑定结算方式，结算方式的卡需要支持境外付款，所以没有实现，后续有时间再弄



***********实现方式四***********
利用从github上copy下来的mtranslate包，配合异步多进程，可以无限制的爬取，局限就看你的带宽和机器了
由于受带宽的影响，或者vpn不稳定，导致获取的响应异常，这时的解决办法是设置该翻译结果为None，等爬完一轮再利用handle_res.py再爬一遍

linux上配置小火箭：https://i.jakeyu.top/2017/03/16/centos%E4%BD%BF%E7%94%A8SS%E7%BF%BB%E5%A2%99/

备注
①可以查看mtranslate里面的源码，修改timeout参数
②可以使用split_txt_file.py分割txt，再启用多进程爬取，效率有所提高
--------
后面发现其实google翻译在中国区没有被屏蔽，我们可以把mtranslate/core.py里的base_link改成中国区的地址


