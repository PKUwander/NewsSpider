# -*- coding: utf-8 -*-
# @Time    : 2019/11/27 23:00
# @Author  : Leon
# @Email   : 1446684220@qq.com
# @File    : test.py
# @Desc    :
# @Software: PyCharm

from WechatPCAPI import WechatPCAPI
import time
import logging
from queue import Queue
import threading


logging.basicConfig(level=logging.INFO)
queue_recved_message = Queue()


# 这是消息回调函数，所有的返回消息都在这里接收，建议异步处理，防止阻塞
def on_message(message):
    print(message)


def main():
    help(WechatPCAPI)

    wx_inst = WechatPCAPI(on_message=on_message, log=logging)
    wx_inst.start_wechat(block=True)

    while not wx_inst.get_myself():
        time.sleep(5)

    print('登陆成功')
    print(wx_inst.get_myself())

    time.sleep(10)

    # 开启保存文件图片等功能，不调用默认不保存，调用需要放在登陆成功之后
    wx_inst.start_auto_save_files()
    # wx_inst.send_text_and_at_someone('22941059407@chatroom', 'wxid_6ij99jtd6s4722', '车臣', '你好')
    # time.sleep(2)
    # wx_inst.send_text_and_at_someone('22941059407@chatroom', 'wxid_6ij99jtd6s4722', '车臣', 'aaasss')
    # wx_inst.send_text(to_user='filehelper', msg='作者QQ:\r1446684220')
    # wx_inst.send_img(to_user='filehelper', img_abspath=r'C:\Users\Leon\Pictures\1.jpg')
    # time.sleep(1)
    # wx_inst.send_link_card(
    #     to_user='filehelper',
    #     title='博客',
    #     desc='我的博客，红领巾技术分享网站',
    #     target_url='http://www.honglingjin.online/',
    #     img_url='http://honglingjin.online/wp-content/uploads/2019/07/0-1562117907.jpeg'
    # )
    # time.sleep(1)

    # 这个是获取群具体成员信息的，成员结果信息也从上面的回调返回
    # wx_inst.get_member_of_chatroom('22941059407@chatroom')

    # # 删除好友
    # wx_inst.get_friends("wx_123231212121")  # 参数写wxid

    # # 更新好友 一般不用调，后台会维护好友表，但是不放心表不准，可以先调用这个再调get_friends
    # wx_inst.update_frinds()

    # 这个是更新所有好友、群、公众号信息的，结果信息也从上面的on_message返回
    # wx_inst.get_friends()


if __name__ == '__main__':
    main()
