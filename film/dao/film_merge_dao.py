# -*- coding: UTF-8 -*-
'''
Created on 2017年12月10日

@author: Administrator
'''
from film.dao.base_dao import BaseDao
import datetime

class FilmMergeItem():
    id = -1
    filmName = ''
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
    duration = 0
    state = '1'
    
class FilmMergeDao(BaseDao):
    def insertNew(self,FilmMergeItem):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO tf_merge_film (film_name, grade, show_time, show_state, img, film_type, ver, actor, country, direct, init_date,state) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % \
                                (FilmMergeItem.filmName,str(FilmMergeItem.grade),str(FilmMergeItem.showTime),str(FilmMergeItem.showState),FilmMergeItem.img,FilmMergeItem.filmType,FilmMergeItem.ver,FilmMergeItem.actor,FilmMergeItem.country,FilmMergeItem.direct,now,str(FilmMergeItem.state))
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)
        return self.getByFilmName(FilmMergeItem.filmName)
    
    def getByFilmName(self,filmName):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = baseDao.getDictCursor(db)
        num = cursor.execute("select * from tf_merge_film where film_name ='%s' " % (filmName))
        if(num == 0):
            return None
        rows = cursor.fetchall()
        row = rows[0]
        filmMergeItem = FilmMergeItem()
        filmMergeItem.id = row['id']
        filmMergeItem.filmName = row['film_name']
        filmMergeItem.grade = row['grade']
        filmMergeItem.showTime = row['show_time']
        filmMergeItem.showState = row['show_state']
        filmMergeItem.img = row['img']
        filmMergeItem.filmType = row['film_type']
        filmMergeItem.ver = row['ver']
        filmMergeItem.actor = row['actor']
        filmMergeItem.country = row['country']
        filmMergeItem.direct = row['direct']
        filmMergeItem.initDate = row['init_date']
        filmMergeItem.duration = row['duration']
        filmMergeItem.state = row['state']
        baseDao.commitCloseDb(db)
        return filmMergeItem