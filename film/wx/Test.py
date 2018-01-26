'''
Created on 2017年12月21日

@author: Administrator
'''
from film.wx.wx import WXSender
from wechat_sender.sender import Sender

# help(Sender())
# sender = Sender(token='wx-1',receivers='www,津门四庭柱')
# sender.send("！！！！！")

WXSender().send(20171222)