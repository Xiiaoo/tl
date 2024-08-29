import requests
import execjs
import pymongo


class YS:
    def __init__(self):
        self.url = 'https://www.chinaindex.net/iIndexMobileServer/teleplay/rank/waiting/fans'
        self.ctx = execjs.compile(
            open('小平台\\影视综rank\\ys.js', 'r', encoding='utf-8').read())
        self.cookies = {
            'Hm_lvt_2873e2b0bdd5404c734992cd3ae7253f': '1724723381',
            'Hm_lpvt_2873e2b0bdd5404c734992cd3ae7253f': '1724723381',
            'HMACCOUNT': '111F64E2B3E87098',
            'mobile_iindex_uuid': '5e134c1b-f9ac-5a43-8b81-c2cc58ae4610',
        }
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'https://www.chinaindex.net/ranklist/5/1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'UUID': '5e134c1b-f9ac-5a43-8b81-c2cc58ae4610',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'funcID': 'undefined',
            'incognitoMode': '0',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.params = {
            'sign': '46cf510e48f99667216bfa781d6bebab',
        }
        self.mongoclient = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.mongoclient['Wecent']['ChinaIndex']

    def req(self):
        res = requests.get(self.url, headers=self.headers,
                           params=self.params, cookies=self.cookies).json()
        return [res['data'], res['lastFetchTime']]

    def decrypt(self):
        data = self.req()
        decrypt_data = self.ctx.call('decrypt', data[0], data[1])
        for rank_info in decrypt_data['rank_list']:
            item=dict()
            item['id']=rank_info['object_info']['id']
            item['name']=rank_info['object_info']['name']
            item['tags']=rank_info['object_info']['tags']
            self.save_info(item)
            
    def save_info(self,item):
        self.db.insert_one(item)
        print('保存成功')



if __name__ == '__main__':
    ys = YS()
    results=ys.decrypt()