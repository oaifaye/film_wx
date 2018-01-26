'''
Created on 2017年12月10日

@author: Administrator
'''
import pymysql

class BaseDao():

    db_url='127.0.0.1'
    db_username="root"
    db_password='123456'
    db_name='ai'
    db_encode='utf8'
    
    def getDB(self):
        # 打开数据库连接
        db = pymysql.connect(self.db_url,self.db_username,self.db_password,self.db_name,charset=self.db_encode)
        return db
    
    def getDictCursor(self,db):
        return db.cursor(pymysql.cursors.DictCursor)
    
    def commitCloseDb(self,db):
        # 关闭数据库连接
        db.commit()
        db.close()
        
#     def insert(self):
#          
#         # 使用cursor()方法获取操作游标 
#         cursor = db.cursor(pymysql.cursors.DictCursor)
#         
#         num = cursor.execute("select 1 from bak_slf_define where url='%s' " % (url))
#         if(num == 0):
#             # 使用execute方法执行SQL语句
#             cursor.execute("INSERT INTO bak_slf_define (url,param,param_has_id,param_endwidth_id) VALUES ('%s', '%s', '%s', '%s')" % (url,paramStr,paramsHasId,paramsEndwidthId))
#         
#         num = cursor.execute("select 1 from bak_slf_define_full where url='%s'" % (url))
#         if(num == 0):
#             cursor.execute("INSERT INTO bak_slf_define_full (url,full_url) VALUES ('%s', '%s')" % (url,fullUrl))
        
        