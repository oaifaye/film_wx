# -*- coding: UTF-8 -*-
'''
Created on 2017年12月10日

@author: Administrator
'''
from film.dao.base_dao import BaseDao
import datetime

class CinemaItem():
    id = -1
    cinemaName = ''
    websiteId=-1
    websiteCinemaId=None
    area = ''
    mergeId = -1
    addr = ''
    state = '1'
    initDate = None
    
class CinemaDao(BaseDao):
    def insertNew(self,CinemaItem):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        num = cursor.execute("select 1 from tf_cinema where website_id='%s' and website_cinema_id='%s' " % \
                             (CinemaItem.websiteId,CinemaItem.websiteCinemaId))
        if num > 0:
            return 
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("INSERT INTO tf_cinema (cinema_name, website_cinema_id, website_id, area, addr, state, init_date) VALUES ('%s', '%s', '%s', %s, '%s', '%s', '%s')" % \
                                (CinemaItem.cinemaName,str(CinemaItem.websiteCinemaId),str(CinemaItem.websiteId),CinemaItem.area,CinemaItem.addr,str(CinemaItem.state),now))
        num = cursor.execute("INSERT INTO tf_cinema (cinema_name, website_cinema_id, website_id, area, addr, state, init_date) VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                (CinemaItem.cinemaName,CinemaItem.websiteCinemaId,CinemaItem.websiteId,str(CinemaItem.area),CinemaItem.addr,CinemaItem.state,now))
        baseDao.commitCloseDb(db)
    
    def getNoMergeCinema(self):
        cinemaItems = self.doSelect("select * from tf_cinema where merge_id is null and state=1")
        return cinemaItems
    
    def getHasAreaCinema(self,mergeId):
        cinemaItems = self.doSelect("select * from tf_cinema where merge_id='%s' " % (mergeId))
        return cinemaItems
    
    def doSelect(self,sql):
        cinemaItems = []
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = baseDao.getDictCursor(db)
        print(sql)
        num = cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            cinemaItem = CinemaItem()
            cinemaItem.id = row['id']
            cinemaItem.cinemaName = row['cinema_name']
            cinemaItem.websiteId=row['website_id']
            cinemaItem.websiteCinemaId=row['website_cinema_id']
            cinemaItem.area = row['area']
            cinemaItem.mergeId = row['merge_id']
            cinemaItem.addr = row['addr']
            cinemaItem.state = row['state']
            cinemaItems.append(cinemaItem)
        baseDao.commitCloseDb(db)
        return cinemaItems
    
    def updateCinemaMergeId(self,id,mergeId):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        sql = "update tf_cinema set merge_id='%s' where id='%s' " % (mergeId,id)
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)