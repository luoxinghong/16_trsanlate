translate = require('google-translate-api');
translate('请问如何调用谷歌翻译API', {to: 'en'}).then(res => {
    console.log(res.text);
    console.log(res.from.language.iso);
}).catch(err => {
    console.error(err);
})

