# -*- coding: utf-8 -*-

import requests

headers = {
    "Accept": "text/javascript,text/html,application/xml,text/xml,*/*",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "www.toutiao.com",
    "Referer": "http://www.toutiao.com/ch/news_hot/",
    "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/60.0.3095.5Safari/537.36",
}

cookies = {
    "csrftoken": "15829c628ddba3c0c3e5c28182b5283a",
    "uuid": "w:88506056f1cb461ca78582bb3a3078c0",
    "UM_distinctid": "15cb028a075b-07ab5859695a01-61547420-e1000-15cb028a07636c",
    "tt_webid": "6432160511211521537",
    "_ga": "GA1.2.722475005.1497604072",
    "_gid": "GA1.2.840490493.1497604072",
    "_gat": "1",
    "CNZZDATA1259612802": "2101969168-1497600998-%7C1497600998",
    "__tasessionId": "fx3d7i6sb1497604071228"
}


def get_page(url=None, params=None, method='GET', headers=headers, cookies=cookies):
    if params and method == 'GET':
        parm = [v for k, v in params.items()]
        url = url + '?' + '&'.join(parm)
    res = requests.request(method=method, url=url, params=params, headers=headers, cookies=cookies)
    return res.content.decode('utf-8')
