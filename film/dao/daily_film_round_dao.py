# -*- coding: UTF-8 -*-
'''
Created on 2017年12月10日

@author: Administrator
'''
from film.dao.base_dao import BaseDao
import datetime

class DailyFilmRoundItem():
    id = -1
    websiteId=-1
    websiteFilmId = -1
    dateNo = 0
    showRoundNum = 0
    showCinemaNum = 0
    initDate = None
    
class DailyFilmRoundDao(BaseDao):
    def insert(self,DailyFilmRoundItem):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO tf_daily_film_round (website_id, website_film_id, date_no,show_round_num,show_cinema_num, init_date) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % \
                (str(DailyFilmRoundItem.websiteId),str(DailyFilmRoundItem.websiteFilmId),str(DailyFilmRoundItem.dateNo),str(DailyFilmRoundItem.showRoundNum),str(DailyFilmRoundItem.showCinemaNum),now)
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)
        
    def deleteOneDay(self,dateInt,websiteId):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        num = cursor.execute("delete from tf_daily_film_round where date_no='%s' and website_id='%s' " % (dateInt,websiteId))
        baseDao.commitCloseDb(db)
    
