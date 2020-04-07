#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Author: wander

from WechatPCAPI import WechatPCAPI
import time
import logging
from queue import Queue
import threading

import requests
import pandas as pd
import time
import datetime
import random

logging.basicConfig(level=logging.INFO)
queue_recved_message = Queue()

news_str = 'news截至北京时间2时，这是因为python环境不是3.7导致的，下载python3.7位安装使'

# 这是消息回调函数，所有的返回消息都在这里接收，建议异步处理，防止阻塞
def on_message(message):
    print(message)


def main():
    global news_str
    help(WechatPCAPI)

    wx_inst = WechatPCAPI(on_message=on_message, log=logging)
    wx_inst.start_wechat(block=True)

    while not wx_inst.get_myself():
        time.sleep(5)

    print('登陆成功')
    print(wx_inst.get_myself())

    time.sleep(10)
    while(1):
        news=cai_spider()
        news=''.join(news.split())
        if news_str[-14:-1]==news[-14:-1]:
            print('请等�?0s')
            time.sleep(50)
        else:
            i=0
            df = pd.DataFrame(columns=['time', 'news'])
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            news_str = news
            print(news)
            df.loc[i, 'time'] = now
            df.loc[i, 'news'] = news
            df.to_csv('news.csv', mode='a', header=False)
            wx_inst.send_text(to_user='wxid', msg=news)

# 此函数随机返回proxy_list里面的一个代理ip
def get_random_proxy():
    proxy_list = [
        ip    ]
    proxy = random.choice(proxy_list)
    return proxy

def cai_spider():
    # df_fin=pd.DataFrame(columns=['time','news'])
    try:
        global news_str
        i=0
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }

        url='https://www.cls.cn/nodeapi/roll/get_update_roll_list?last_time=1585566918&refresh_type=0&rn=20&subscribedColumnIds=&' \
            'hasFirstVipArticle=1&app=CailianpressWeb&os=web&sv=6.8.0&sign=9f0c06834f2c5952efffab7c799be805'

        proxies = {'http': 'http://' + get_random_proxy()}

        data= requests.get(url,headers=headers,proxies=proxies)       # 最基本的不带参数的get请求

        if data.status_code==200:
            data_j=data.json()
            content=data_j['data']
            content_2=content['roll_data']
            content_3=content_2[0]
            content_detail=content_3['content']

            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            news_s= now+content_detail
            return news_s

    except Exception as e:

        print('连接错误')
        return news_str

if __name__ == '__main__':
    main()
