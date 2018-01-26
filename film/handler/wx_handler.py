# -*- coding: UTF-8 -*-
'''
Created on 2017年12月21日

@author: Administrator
'''

from wxpy.api.bot import *
import time
from wxpy.api.consts import *
from wxpy.api.bot import Bot

class WXHandler():
    bot = None
    def login(self):
        self.bot = Bot(cache_path=True)
    # 搜索名称含有 "游否" 的男性深圳好友
    
    def sendFriend(self,msg,friendName):
        my_friend = self.bot.friends().search(unicode( '文件传输助手' ))
    # # 发送文本给好友
    # my_friend[0].send('Hello WeChat!')
    # print my_friend
    # for i in range(1,101):
    #     my_friend[0].send('宝儿'+str(i))
    #     time.sleep(0.5)
    
    my_groups = bot.groups().search(unicode( 'wxpy' ))
    print my_groups
    for i in range(1,101):
        my_groups[0].send(i)
        time.sleep(0.5)