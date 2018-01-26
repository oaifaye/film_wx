# -*- coding: UTF-8 -*-
'''
Created on 2017年12月10日

@author: Administrator
'''
from film.dao.base_dao import BaseDao
import datetime

class CinemaMergeItem():
    id = -1
    cinemaName = ''
    area = ''
    addr = ''
    state = '1'
    initDate = None
    
class CinemaMergeDao(BaseDao):
    def insertNew(self,CinemaMergeItem):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO tf_merge_cinema (cinema_name, area, addr, state, init_date) VALUES ('%s', '%s', '%s', %s, '%s')" % \
                                (CinemaMergeItem.cinemaName,CinemaMergeItem.area,CinemaMergeItem.addr,str(CinemaMergeItem.state),now)
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)
        return self.getByCinemaName(CinemaMergeItem.cinemaName)
    
    def getByCinemaName(self,cinemaName):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = baseDao.getDictCursor(db)
        num = cursor.execute("select * from tf_merge_cinema where cinema_name ='%s' " % (cinemaName))
        if(num == 0):
            return None
        rows = cursor.fetchall()
        row = rows[0]
        cinemaMergeItem = CinemaMergeItem()
        cinemaMergeItem.id = row['id']
        cinemaMergeItem.cinemaName = row['cinema_name']
        cinemaMergeItem.area = row['area']
        cinemaMergeItem.addr = row['addr']
        cinemaMergeItem.state = row['state']
        baseDao.commitCloseDb(db)
        return cinemaMergeItem
    
    def getNoAreaCinema(self):
        cinemaMergeItems = self.doSelect("select * from tf_merge_cinema where area ='' or area is null")
        return cinemaMergeItems
    
    def doSelect(self,sql):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = baseDao.getDictCursor(db)
        print(sql)
        num = cursor.execute(sql)
        rows = cursor.fetchall()
        cinemaMergeItems = []
        for row in rows:
            cinemaMergeItem = CinemaMergeItem()
            cinemaMergeItem.id = row['id']
            cinemaMergeItem.cinemaName = row['cinema_name']
            cinemaMergeItem.area = row['area']
            cinemaMergeItem.addr = row['addr']
            cinemaMergeItem.state = row['state']
            cinemaMergeItems.append(cinemaMergeItem)
        baseDao.commitCloseDb(db)
        return cinemaMergeItems
    
    def updateArea(self,id,area):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        sql = "update tf_merge_cinema set area='%s' where id='%s'" % (area,id)
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)
        
    def getByGradeDesc(self,dateNo):
        sql = "select  distinct(d.id),d.cinema_name from \
            tf_daily_film_cinema a left join tf_cinema b on a.website_cinema_id=b.website_cinema_id, \
            tf_cinema c left join tf_merge_cinema d on c.merge_id = d.id \
            where a.date_no='%s' and d.area in ('红桥区','南开区') \
            order by a.grade desc limit 3" % (dateNo)
        cinemaMergeItems = self.doSelect(sql)
        return cinemaMergeItems