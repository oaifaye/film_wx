# -*- coding: UTF-8 -*-
'''
Created on 2017年12月10日

@author: Administrator
'''
from film.dao.base_dao import BaseDao
import datetime

class MessageSendItem():
    id = -1
    personName=''
    sendType=''
    state=1
    initDate = None
    
class MessageSendDao(BaseDao):
    send_type_wx_user = 'wx_user'
    send_type_wx_group = 'wx_group'
    
    def getPersonName(self,sendType):
        personNames = []
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = baseDao.getDictCursor(db)
        sql = "select * from tf_message_send where state=1 and send_type='%s' order by id desc" % (sendType)
        print(sql)
        num = cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            personNames.append(row['person_name'])
        baseDao.commitCloseDb(db)
        return personNames
    
