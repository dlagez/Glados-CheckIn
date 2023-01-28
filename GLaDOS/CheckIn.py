#!/usr/bin/python
import pytz
from os import environ
from json import dumps
from requests import post, get
from datetime import datetime

def start(cookie):
    url = "https://glados.rocks/api/user/checkin"
    url2 = "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 " \
                "Safari/537.36 "
    payload = {
        'token': 'glados.network'
    }
    checkin = post(
        url,
        headers={'cookie': cookie, 'referer': referer, 'origin': origin, 
        'user-agent': useragent,
        'content-type': 'application/json;charset=UTF-8'}, 
        data=dumps(payload)
    )
    state = get(url2,
        headers={'cookie': cookie, 'referer': referer, 'origin': origin, 'user-agent': useragent})
    tz = pytz.timezone('Asia/Shanghai')
    time_now = str(datetime.now(tz=tz))[:19]
    print(f'现在时间是：{time_now}\ncheckin: {checkin.status_code} | state: {state.status_code}')

    if 'message' in checkin.text:
        mess = checkin.json()['message']
        time = state.json()['data']['leftDays']
        days = time.split('.')[0]
        print(mess)
        print('剩余天数：' + days + '天')

    checkin.close()
    state.close()

    return True


if __name__ == '__main__':
    ck = environ["cookie"]
    start(ck)
