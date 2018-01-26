# -*- coding: UTF-8 -*-
'''
Created on 2017年11月17日

@author: Administrator
'''
# 导入模块
import wxpy
from wxpy import *
from wechat_sender import *
from film.dao.message_send_dao import MessageSendDao
from psutil._compat import unicode
import datetime
from film.dao.message_dao import MessageDao
from film.dao.daily_log_dao import DailyLogDao

class WXUtil():
    def login(self):
        # 初始化机器人，扫码登陆
        bot = Bot(cache_path=True)
        friends = []
        messageSendDao = MessageSendDao()
        wxpersons = messageSendDao.getPersonName(MessageSendDao.send_type_wx_user)
        for wxperson in wxpersons:
            friends.extend(bot.friends().search(wxperson))
         
        wxgroups = messageSendDao.getPersonName(MessageSendDao.send_type_wx_group)
        for wxgroup in wxgroups:
            friends.extend(bot.groups().search(wxgroup))
        friends.append(bot.file_helper)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('微信开始监听咯----',now) 
        listen(bot, token='wx-1', receivers=friends)
#         listen(bot, token='wx-1')
        wxpy.embed()
class WXSender():
    def send(self,dateNo):
        friends = []
        messageSendDao = MessageSendDao()
        wxpersons = messageSendDao.getPersonName(MessageSendDao.send_type_wx_user)
        friends.extend(wxpersons)
        
        wxgroups = messageSendDao.getPersonName(MessageSendDao.send_type_wx_group)
        friends.extend(wxgroups)
        friendsStr = ','.join(friends)
        print('friendsStr:',friendsStr)
        
        sender = Sender(token='wx-1',receivers=friendsStr)
        messageDao = MessageDao()
        #场次多的
        roundContent= messageDao.selectContent(dateNo, DailyLogDao.log_type_calc_round)
        sender.send(roundContent)
        
        #评分高的
#         gradeContent= messageDao.selectContent(dateNo, DailyLogDao.log_type_calc_grade)
#         sender.send(gradeContent)
    
if __name__ == '__main__':
    WXUtil().login()
