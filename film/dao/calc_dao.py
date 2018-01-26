# -*- coding: UTF-8 -*-
'''
Created on 2017年12月10日

@author: Administrator
'''
from film.dao.base_dao import BaseDao
import datetime

class CalcItem():
    id = -1
    dateNo = 0
    calcType=''
    websiteId = 0
    mergeCinemaId=None
    mergeFilmId=None
    initDate = None
    
class CalcDao(BaseDao):
    def insert(self,CalcItem):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO tf_calc (date_no, calc_type, website_id, merge_cinema_id, merge_film_id, init_date) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % \
                    (str(CalcItem.dateNo),str(CalcItem.calcType),str(CalcItem.websiteId),str(CalcItem.mergeCinemaId),str(CalcItem.mergeFilmId),now)
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)
    
#     def getNoMergeCinema(self):
#         cinemaItems = self.doSelect("select * from tf_cinema where merge_id is null and state=1")
#         return cinemaItems
    
    def doSelect(self,sql):
        items = []
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = baseDao.getDictCursor(db)
        print(sql)
        num = cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            item = CalcItem()
            item.id = row['id']
            item.dateNo = row['date_no']
            item.calcType=row['calc_type']
            item.websiteId = row['website_id']
            item.websiteCinemaId=row['website_cinema_id']
            item.websiteFilmId=row['website_film_id']
            item.initDate = row['init_date']
            items.append(item)
        baseDao.commitCloseDb(db)
        return items
    
    def deleteByDateNo(self,dateNo,calcType):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        sql = "delete from  tf_calc where date_no='%s' and calc_type='%s' " % (dateNo,calcType)
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)
    
    '''找出所有电影中评分最高的前三名'''
    def getGradeHiFilm(self,dateNo):
        mergeFilmIds = []
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = baseDao.getDictCursor(db)
        sql = "select  distinct(b.merge_id) merge_film_id from  \
             tf_daily_film_cinema a left join tf_film b on a.website_film_id=b.website_film_id \
             left join tf_merge_film c on b.merge_id=c.id \
            where a.date_no='%s'  \
            order by a.grade desc limit 3" % (dateNo)
        print(sql)
        num = cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            mergeFilmIds.append(row['merge_film_id'])
        baseDao.commitCloseDb(db)
        return mergeFilmIds
    
    '''获取一个电影在那些电影院看哪些网站买票比较合适'''
    def getCheapCimane(self,filmMergeId,dateNo):
        calcItems = []
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = baseDao.getDictCursor(db)
        sql = "select a.website_id website_id, b.merge_id cinema_merge_id,d.merge_id film_merge_id \
                from tf_daily_film_cinema a left join tf_cinema b on a.website_cinema_id = b.website_cinema_id  \
                left join tf_film d on a.website_film_id = d.website_film_id left join tf_merge_cinema f on b.merge_id=f.id \
                where d.merge_id='%s' and a.date_no='%s' and f.area in ('红桥区','南开区') \
                order by a.price limit 1" % (str(filmMergeId),str(dateNo))
        print(sql)
        num = cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            calcItem= CalcItem()
            calcItem.dateNo = dateNo
            calcItem.websiteId = row['website_id']
            calcItem.mergeCinemaId=row['cinema_merge_id']
            calcItem.mergeFilmId=row['film_merge_id']
            calcItems.append(calcItem)
        baseDao.commitCloseDb(db)
        return calcItems
    
    '''找出所有影院里排片最高的前三名'''
    def getMostRoundFilms(self,dateNo):
        mergerFilmIds = []
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = baseDao.getDictCursor(db)
        sql = "select b.merge_id merge_id\
            from tf_daily_film_round a left join tf_film b on a.website_film_id=b.website_film_id \
                left join tf_merge_film c on b.merge_id = c.id \
            where a.date_no='%s' \
            group by b.merge_id \
            order by (a.show_round_num) desc limit 3" % (dateNo)
        print(sql)
        num = cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            mergerFilmIds.append(row['merge_id'])
        baseDao.commitCloseDb(db)
        return mergerFilmIds