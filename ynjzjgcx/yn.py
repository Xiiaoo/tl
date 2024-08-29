import requests
import execjs
import ddddocr
import json
import base64


def detect():
    shadeImage = open('小平台\\云南建设\\Captchas\\bigImage.png', 'rb').read()
    slideImage = open('小平台\\云南建设\\Captchas\\smallImage.png', 'rb').read()
    slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    res = slide.slide_match(slideImage, shadeImage, simple_target=True)
    print('识别出距离为：', res['target'][0])
    return res['target'][0]


class YN:
    def __init__(self):
        self.genVcodeurl = 'https://www.ynjzjgcx.com/prod-api/mohurd-pub/vcode/genVcode'
        self.qureyurl = 'https://www.ynjzjgcx.com/prod-api/mohurd-pub/dataServ/findBaseEntDpPage'
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://www.ynjzjgcx.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.ynjzjgcx.com/dataPub/enterprise',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'appId': '84ded2cd478642b2',
            'isToken': 'false',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.ctx = execjs.compile(
            open('小平台\\云南建设\\yn.js', 'r', encoding='utf-8').read())

    def genVcode(self):
        json_data = {
            'params': self.ctx.call('get_params', {
                "key": "query"
            })
        }
        res = json.loads(requests.post(
            self.genVcodeurl, headers=self.headers, json=json_data).json()["data"])
        with open('小平台\\云南建设\\Captchas\\smallImage.png', 'wb')as f:
            f.write(base64.b64decode(res['smallImage']))
        with open('小平台\\云南建设\\Captchas\\bigImage.png', 'wb')as f:
            f.write(base64.b64decode(res['bigImage']))
        return [res['slideId'], res['yHeight']]

    def query(self, pageNum, pageSize):
        params = {
            "pageNum": pageNum,
            "pageSize": pageSize,
            "certificateType": "",
            "name": "",
            "slideId": self.genVcode()[0],
            "key": "query",
            "width": detect()
        }
        json_data = {
            'params': self.ctx.call('get_params', params)
        }
        res = requests.post(
            self.qureyurl, headers=self.headers, json=json_data).json()
        if res["code"] == 200:
            unique_by_hash = {}
            for data in res['data']['records']:
                hash_value = hash(data['name'])
                if hash_value not in unique_by_hash:
                    unique_by_hash[hash_value] = {
                        'name': data['name'],
                        'creditCode': data['creditCode'],
                        'address': data['address'],
                    }
            print(unique_by_hash)
            return unique_by_hash
        else:
            return 0

    def write(self, data):
        with open('小平台\\云南建设\\yn.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    yn = YN()
    data = {}
    for i in range(10):
        j = i
        yn.genVcode()
        res = yn.query(j+1, 10)
        if res != 0:
            data.update(res)
            
    yn.write(data)
