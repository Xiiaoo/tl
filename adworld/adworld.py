import requests
import execjs
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor

ctx = execjs.compile(open('./adworld.js').read())
cookies = {
    'cngizm2ziytq3mwy': '9w7iMVClH1j1GVusGqNS56UNsaJV6q0H6KlTuPxOprRP9uFEFg==',
    'fogq4n2exnzc0otg': 'CQUJOgBTBVdbAwdHSh9HGhgQS0YYRUFEQ0YaeH52KXByfChxBg==',
}
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'en2uwnjgxodjhogi': '1',
    'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_info(pagenum):
    p = ctx.call('get_params', pagenum)
    params = {
        'qmze1yzvhyzcyyjr': quote(p),
    }
    response = requests.get('https://adworld.xctf.org.cn/api/event/release_event/list/',
                            params=params,
                            cookies=cookies,
                            headers=headers,
                            ).json()["data"]["rows"]
    for i in range(len(response)):
        data_dict = {}
        data_dict["release_name"] = response[i]["release_name"]
        data_dict["release_sponsor"] = response[i]["release_sponsor"]
        data_dict["order_start_time"] = response[i]["order_start_time"]
        print(data_dict)


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=5) as pool:
        for page in range(10):
            pool.submit(get_info, page)