from urllib import parse
import execjs
import time
import uuid
import requests
import ddddocr
import random

def time_str(): return str(int(time.time()*1000))
def time_int(): return int(time.time()*1000)


def detect():
    shadeImage = open('小平台\\丰巢\\Captchas\\1.png', 'rb').read()
    slideImage = open('小平台\\丰巢\\Captchas\\2.png', 'rb').read()
    slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    res = slide.slide_match(slideImage, shadeImage, simple_target=True)
    print('识别出距离为：', res['target'][0])
    return res['target'][0]


def generate_track(y):
    begin_time, x, track, distance, zero_times = time_int(
    ), 0, [], detect(), random.randint(10, 16)
    second_times = zero_times+10
    track_time = begin_time
    # print('distance', distance)
    # print('zero_times', zero_times)
    while x <= distance:
        if x <= 11:
            track.append({'x': x, 'y': y, 'time': track_time})
            x += 1
            track_time += random.randint(1, 3)
        elif x > 11 and x <= distance/13*7:
            if random.randint(0, 2) == 0:
                while zero_times > 8:
                    zero_times -= 1
                    track.append({'x': x, 'y': y, 'time': track_time})
                    track_time += random.randint(1, 3)
            elif random.randint(1, 2) == 2:
                while second_times > 0:
                    x += 2
                    track.append({'x': x, 'y': y, 'time': track_time})
                    track_time += random.randint(1, 4)
                    second_times -= 1
            else:
                x += 1
                track.append({'x': x, 'y': y, 'time': track_time})
                track_time+random.randint(2, 5)
        else:
            if random.randint(0, 1) == 0:
                while zero_times > 0:
                    zero_times -= 1
                    track.append({'x': x, 'y': y, 'time': track_time})
                    track_time += random.randint(1, 3)
            else:
                track.append({'x': x, 'y': y, 'time': track_time})
                track_time += random.randint(4, 8)
                x += 1
    # print(len(track))
    print("滑动时间：",track_time-begin_time)
    # print(track)
    return track


# generate_track(22)


class FC:
    def __init__(self):
        self.captchaurl = "https://acs.fcbox.com/captcha/querySlideImage/"
        self.pbkeyurl = "https://www.fcbox.com/noshiro/getPublicKey"
        self.loginurl = "https://www.fcbox.com/passport/login"
        self.checkurl = "https://acs.fcbox.com/captcha/checkCode/"
        self.captchaheaders = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Access-Control-Request-Headers': 'content-type',
            'Access-Control-Request-Method': 'POST',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Origin': 'https://www.fcbox.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.fcbox.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }
        self.loginheaders = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'https://www.fcbox.com/pages/user/login.html',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'fc_version_no': '8066002',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        self.ctx = execjs.compile(
            open('小平台\\丰巢\\fengchao.js', 'r', encoding='utf-8').read())

    def get_captcha(self):
        req_uuid = str(uuid.uuid4())
        res = requests.post(
            self.captchaurl+req_uuid, headers=self.captchaheaders, json={}).json()
        shadeImageUrl = res['data']['shadeImageUrl']
        slideImageUrl = res['data']['slideImageUrl']
        checkId = res['data']['checkId']
        clientIp = res['data']['clientIp']
        aeskey = res['data']['key']
        pointY = res['data']['pointY']
        with open('小平台\\丰巢\\Captchas\\1.png', 'wb')as f:
            f.write(requests.get(shadeImageUrl).content)
        with open('小平台\\丰巢\\Captchas\\2.png', 'wb')as f:
            f.write(requests.get(slideImageUrl).content)
        return [clientIp, checkId, req_uuid, aeskey, pointY]

    def encrypt(self, ip, checkId, uuid, aeskey, guiji):
        return self.ctx.call('encrypt', ip, checkId, uuid, aeskey, guiji)

    def get_publickey(self):
        res=requests.post(self.pbkeyurl, headers=self.loginheaders).json()
        return res['data']

    def login(self, username, pwd, verifyCode):
        public_key=self.get_publickey()
        print(public_key)
        encrypt_pwd=self.ctx.call('rsa_encrypt',pwd, public_key)
        print('加密的密码:',encrypt_pwd)
        params = {
            'username': username,
            'password': encrypt_pwd,
            'verifyCode': verifyCode,
            '_': time_str()
        }
        print(params)
        res = requests.get(
            self.loginurl, headers=self.loginheaders, params=params)
        return res.json()

    def check(self, uuid, encrypt_params):
        return requests.post(self.checkurl+uuid, headers={
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://www.fcbox.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.fcbox.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }, data=encrypt_params).json()
    

if __name__ == '__main__':
    fc = FC()
    params = fc.get_captcha()
    guiji = generate_track(params[4])
    encrypt_guiji = fc.encrypt(params[0], params[1], params[2], params[3], guiji)
    # print(fc.check(params[2],encrypt_guiji))
    captcha_res=fc.check(params[2],encrypt_guiji)
    print(captcha_res)
    for i in range(100):
        if str(captcha_res["success"])=='False':
            params = fc.get_captcha()
            guiji = generate_track(params[4])
            encrypt_guiji = fc.encrypt(params[0], params[1], params[2], params[3], guiji)
            captcha_res=fc.check(params[2],encrypt_guiji)
            print(captcha_res)
        else:
            print(fc.login('18201928222','123456',captcha_res['data']['token']))
            break

