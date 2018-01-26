# -*- coding: UTF-8 -*-
'''
Created on 2017年12月10日

@author: Administrator
'''
from film.dao.base_dao import BaseDao
import datetime

class MessageItem():
    id = -1
    dateNo = 0
    content=''
    msType=''  #calc_round / calc_grade
    state = 0
    initDate = None
    
    def toString(self):
        pass
    
class MessageContentItem():
    filmName = ''
    cinemaName = ''
    websiteName= ''
    filmType=''
    actor = ''
    
class MessageDao(BaseDao):
    def deleteOneDay(self,dateNo,msType):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = baseDao.getDictCursor(db)
        sql = "delete from tf_message where date_no='%s' and ms_type='%s'" % (dateNo,msType)
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)
        
    def insert(self,MessageItem):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO tf_message (date_no, content, ms_type,state,init_date) VALUES ('%s', '%s', '%s', '%s', '%s')" % \
                (str(MessageItem.dateNo),str(MessageItem.content),str(MessageItem.msType),'1',now)
        print(sql)
        num = cursor.execute(sql)
        baseDao.commitCloseDb(db)
        
        
    def selectContent(self,dateNo,msType):    
        sql = "select * from tf_message where date_no='%s' and ms_type='%s'" % (str(dateNo),msType)
        items =  self.doSelect(sql)
        if len(items) == 0 :
            return None
        return items[0].content
    
    def doSelect(self,sql):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = baseDao.getDictCursor(db)
        print(sql)
        num = cursor.execute(sql)
        rows = cursor.fetchall()
        items = []
        for row in rows:
            item = MessageItem()
            item.id = row['id']
            item.dateNo = row['date_no']
            item.msType=row['ms_type']
            item.content = row['content']
            item.state=row['state']
            item.initDate = row['init_date']
            items.append(item)
        baseDao.commitCloseDb(db)
        return items
    
    def getCalcMessage(self,dateNo,calcType):
        baseDao = BaseDao()
        db = baseDao.getDB()
        # 使用cursor()方法获取操作游标 
        cursor = baseDao.getDictCursor(db)
        sql = "select b.film_name,c.cinema_name,d.website_name,b.film_type,b.actor \
            from tf_calc a left join tf_merge_film b on a.merge_film_id=b.id left join tf_merge_cinema c on a.merge_cinema_id=c.id \
                left join tf_website d on a.website_id=d.id \
            where a.date_no='%s' and a.calc_type='%s'" % (dateNo,calcType)
        print(sql)
        num = cursor.execute(sql)
        rows = cursor.fetchall()
        items = []
        for row in rows:
            messageContentItem= MessageContentItem()
            messageContentItem.filmName = row['film_name']
            messageContentItem.cinemaName = row['cinema_name']
            messageContentItem.websiteName= row['website_name']
            messageContentItem.filmType=row['film_type']
            messageContentItem.actor = row['actor']
            items.append(messageContentItem)
        baseDao.commitCloseDb(db)
        return items
        