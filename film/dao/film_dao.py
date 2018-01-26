# -*- coding: UTF-8 -*-
'''
Created on 2017年12月10日

@author: Administrator
'''
from film.dao.base_dao import BaseDao
import datetime

class FilmItem():
    id = -1
    filmName = ''
    websiteId=-1
    websiteFilmId=None
    grade = 0.0
    showTime = -1
    showState = -1
    img = ''
    filmType = ''
    ver = ''
    actor = ''
    country = ''
    direct = ''
    initDate = None
    clob = ''
    duration = 0
    state='1'
    mergeId = 0
    
    def toString(self):
        pass
    
class FilmDao(BaseDao):
    def insertNew(self,FilmItem):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        num = cursor.execute("select 1 from tf_film where website_id='%s' and website_film_id='%s' " % \
                             (FilmItem.websiteId,FilmItem.websiteFilmId))
        if num > 0:
            return 
        if FilmItem.grade.isdigit() == False:
            FilmItem.grade = 0.0
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO tf_film (film_name, website_id, website_film_id,grade, show_time, show_state, img, ver, actor, country, direct,film_type,init_date,clob,state) VALUES ('%s', '%s', '%s','%s','%s', '%s', '%s','%s', '%s','%s', '%s', '%s','%s','%s','%s')" % \
                                (FilmItem.filmName,FilmItem.websiteId,FilmItem.websiteFilmId,str(FilmItem.grade),
                                str(FilmItem.showTime),
                                str(FilmItem.showState),
                                FilmItem.img,
                                FilmItem.ver,
                                FilmItem.actor,
                                FilmItem.country,
                                FilmItem.direct,
                                FilmItem.filmType,
                                now,FilmItem.clob,FilmItem.state)
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)
        
    def getNoMergeFilm(self):
        filmItems = []
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = baseDao.getDictCursor(db)
        num = cursor.execute("select * from tf_film where merge_id is null and state=1 " )
        rows = cursor.fetchall()
        for row in rows:
            filmItem = FilmItem()
            filmItem.id = row['id']
            filmItem.filmName = row['film_name']
            filmItem.websiteId=row['website_id']
            filmItem.websiteFilmId=row['website_film_id']
            filmItem.grade = row['grade']
            filmItem.showTime = row['show_time']
            filmItem.showState = row['show_state']
            filmItem.img = row['img']
            filmItem.filmType = row['film_type']
            filmItem.ver = row['ver']
            filmItem.actor = row['actor']
            filmItem.country = row['country']
            filmItem.direct = row['direct']
            filmItem.initDate = row['init_date']
            filmItem.clob = row['clob']
            filmItem.duration = row['duration']
            filmItem.mergeId = row['merge_id']
            filmItems.append(filmItem)
        baseDao.commitCloseDb(db)
        return filmItems
    
    def getByWebsiteFilmId(self,websiteFilmId):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = baseDao.getDictCursor(db)
        num = cursor.execute("select * from tf_film where website_film_id = '%s' ",websiteFilmId )
        rows = cursor.fetchall()
        row = rows[0]
        filmItem = FilmItem()
        filmItem.id = row['id']
        filmItem.filmName = row['film_name']
        filmItem.websiteId=row['website_id']
        filmItem.websiteFilmId=row['website_film_id']
        filmItem.grade = row['grade']
        filmItem.showTime = row['show_time']
        filmItem.showState = row['show_state']
        filmItem.img = row['img']
        filmItem.filmType = row['film_type']
        filmItem.ver = row['ver']
        filmItem.actor = row['actor']
        filmItem.country = row['country']
        filmItem.direct = row['direct']
        filmItem.initDate = row['init_date']
        filmItem.clob = row['clob']
        filmItem.duration = row['duration']
        filmItem.mergeId = row['merge_id']
        baseDao.commitCloseDb(db)
        return filmItem
        
    def updateFilmMergeId(self,id,mergeId):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        sql = "update tf_film set merge_id='%s' where id='%s' " % (mergeId,id)
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)    