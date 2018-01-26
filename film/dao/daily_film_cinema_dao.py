# -*- coding: UTF-8 -*-
'''
Created on 2017年12月10日

@author: Administrator
'''
from film.dao.base_dao import BaseDao
import datetime

class DailyFilmCinemaItem():
    id = -1
    websiteId=-1
    websiteFilmId = -1
    websiteCinemaId=-1
    grade = 0.0
    dateNo = 0
    showState = -1
    price = 0.0
    initDate = None
    showCinemaNum = 0
    showRoundNum = 0
    
class DailyFilmCinemaDao(BaseDao):
    def insert(self,DailyFilmCinemaItem):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            DailyFilmCinemaItem.grade = float(DailyFilmCinemaItem.grade)
        except:
            DailyFilmCinemaItem.grade = 0.0
        sql = "INSERT INTO tf_daily_film_cinema (website_id, website_film_id, website_cinema_id, grade, date_no, show_state, price, init_date,show_cinema_num,show_round_num) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s')" % \
                (str(DailyFilmCinemaItem.websiteId),str(DailyFilmCinemaItem.websiteFilmId),str(DailyFilmCinemaItem.websiteCinemaId),str(DailyFilmCinemaItem.grade),str(DailyFilmCinemaItem.dateNo),str(DailyFilmCinemaItem.showState),str(DailyFilmCinemaItem.price),now,str(DailyFilmCinemaItem.showCinemaNum),str(DailyFilmCinemaItem.showRoundNum))
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)
        
    def deleteOneDay(self,dateInt,websiteId):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        num = cursor.execute("delete from tf_daily_film_cinema where website_id='%s' and date_no='%s' " % \
                             (websiteId,dateInt))
        baseDao.commitCloseDb(db)
    
