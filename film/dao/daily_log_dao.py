# -*- coding: UTF-8 -*-
'''
Created on 2017年12月10日

@author: Administrator
'''
from film.dao.base_dao import BaseDao
import datetime

class DailyLogItem():
    id = -1
    dateNo = 0
    websiteId=-1
    startDate=None
    endDate = None
    state = 0
    logType = '' # snatch / calc_grade
    
    def toString(self):
        pass
    
class DailyLogDao(BaseDao):
    log_type_snatch = 'snatch'
    log_type_calc_grade = 'calc_grade'
    log_type_calc_round = 'calc_round'
    log_type_calc_message = 'message'
    log_type_calc_send_message = 'send_message'
    
    def hasDailyLog(self,dateNo,websiteId,logType):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        sql = "select 1 from tf_daily_log where website_id='%s' and date_no='%s' and log_type='%s' " % (websiteId,dateNo,logType)
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)
        return num > 0
    
    def deleteFailed(self,dateNo,websiteId,logType):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        sql = "delete from tf_daily_log where website_id='%s' and date_no='%s' and state in (-1,0) and log_type='%s'" % (websiteId,dateNo,logType)
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)
        
    
    def insertStart(self,dateNo,websiteId,logType):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO tf_daily_log (date_no, website_id, start_date, state,log_type) VALUES ('%s', '%s', '%s', '%s','%s')" % \
                    (str(dateNo),str(websiteId),now,'0',logType)
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)
        
    def successEnd(self,dateNo,websiteId,logType):
        self.updateEnd(dateNo, websiteId, 1,'',logType)
        
    def failEnd(self,dateNo,websiteId,msg,logType):
        if self.hasDailyLog(dateNo, websiteId,logType) == False:
            self.insertStart(dateNo, websiteId,logType)
        self.updateEnd(dateNo, websiteId, -1,msg,logType)
        
    def updateEnd(self,dateNo,websiteId,state,msg,logType):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = msg.replace('\'','\\\'')
        sql = "update tf_daily_log set end_date='%s' ,state='%s',msg='%s' where date_no='%s' and website_id = '%s' and log_type = '%s'" % \
                    (now,str(state),msg,str(dateNo),str(websiteId),logType)
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)
    