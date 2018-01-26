# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
import time
import datetime
import random
import sched
from selenium.common.exceptions import NoAlertPresentException
import json
import sys
import re
import pymysql
import configparser 


class RadNews():
    urls=[
            'http://www.pub.demo2016.2000cms.cn/cms_ys/system/2017/11/27/030014358.shtml',
            'http://www.pub.demo2016.2000cms.cn/cms_ys/system/2017/11/27/030014357.shtml',
            'http://www.pub.demo2016.2000cms.cn/cms_ys/system/2017/11/27/030014356.shtml',
            'http://www.pub.demo2016.2000cms.cn/cms_ys/system/2017/07/18/030013661.shtml',
            'http://www.pub.demo2016.2000cms.cn/cms_ys/system/2017/07/18/030013659.shtml',
            'http://www.pub.demo2016.2000cms.cn/cms_ys/system/2017/07/18/030013653.shtml',
            'http://www.pub.demo2016.2000cms.cn/cms_ys/system/2017/07/18/030013647.shtml',
            'http://www.pub.demo2016.2000cms.cn/cms_ys/system/2017/07/17/030013616.shtml',
            'http://www.pub.demo2016.2000cms.cn/cms_ys/system/2017/07/17/030013598.shtml',
          ]
#     db_url='127.0.0.1'
#     db_username="root"
#     db_password='123456'
#     db_name='cms2015_3bak'
    db_url='10.0.251.50'
    db_username="root"
    db_password='1234qwer'
    db_name='cms2015_3bak'
    db_encode='utf8'
    
    cur_click_times = 0
    tag_type = ''
    ini_path = 'pub.ini'
    prog_root='http://go108.enorth.com.cn:8080/pub'
    cur_full_id = 0
    
    dcap = dict(DesiredCapabilities.PHANTOMJS)  #设置userAgent
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")
#     dcap['acceptSslCerts'] = True
#     dcap['--ignore-ssl-errors'] = True



    proxy = [
                '--proxy=113.83.217.180:9797',
            ]
        
    def dealOnePageOneTag(self,url):
        driver = webdriver.PhantomJS(executable_path=r"C:\Program Files (x86)\phantomjs-2.1.1-windows\bin\phantomjs.exe",desired_capabilities=self.dcap,service_args=['--ignore-ssl-errors=true','--load-images=false'])
#         obj = webdriver.PhantomJS(executable_path=r"C:\Program Files (x86)\phantomjs-2.1.1-windows\bin\phantomjs.exe",desired_capabilities=self.dcap,service_args=self.proxy)
        driver.set_page_load_timeout(6)
        
#         script = "var page=this;page.onResourceRequested = function (request){page.browserLog.push(JSON.stringify(request));};page.navigationLocked=false"
       
        driver.get("https://go108.enorth.com.cn:8443/pub/auth/LoginAction!loginBegin.do")
        
        driver.find_element_by_id("userName").send_keys('root')
        driver.find_element_by_id("passWord").send_keys('1')
        driver.execute_script('submit();')
#         cookie = driver.get_cookies()
        print ('登陆完成')
        
        time.sleep(1)  
        print ('睡1s完成')
        self.cur_click_times = 0
        tagaslen = 0
        while True:
            try:
                driver.get(url)
                script = "var page=this;page.onNavigationRequested = function(url, type, willNavigate, main) {return false;};page.onCreate = function(url,url1) {};page.browserLog=[];page.onResourceRequested = function (request){page.browserLog.push(JSON.stringify(request));};"
                driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
                driver.execute('executePhantomScript', {'script': script, 'args': []})
                
                print ('current_url:',driver.current_url,'   url:',url)
                
                '''如果要处理的地址一开始就跳转了，判断一下他跳转到的页面是不是已经处理过'''
                current_url  =driver.current_url
                shortCurrentUrl = ''
                if(current_url.find('?')>0):
                    shortCurrentUrl = current_url[:current_url.find("?")].replace(self.prog_root,"").replace("//","/")
                else :
                    shortCurrentUrl = current_url.replace(self.prog_root,"").replace("//","/")
                # 打开数据库连接
                db = pymysql.connect(self.db_url,self.db_username,self.db_password,self.db_name,charset=self.db_encode)
                # 使用cursor()方法获取操作游标 
                cursor = db.cursor()
                num = cursor.execute("select 1 from bak_slf_define_full where url='%s' and id < '%s'" % (shortCurrentUrl,self.cur_full_id))
                if(num != 0):
                    # 关闭数据库连接
                    db.close()  
                    print('已经弄过:',shortCurrentUrl)
                    break
                # 关闭数据库连接
                db.close()  
                    
                
                '''处理iframe'''
                iframes = driver.find_elements_by_tag_name('iframe')
                for oneFrame in iframes:
                    src = oneFrame.get_property("src")
                    self.dealOneUrl(src,'GET','')
                
                tagas = []
                if(self.tag_type == 'a'):
                    '''通过javaScript修改display的值,使元素都可见'''
        #                 js = 'document.querySelectorAll("a")[0].style.display="block";'
        #                 driver.execute_script(js)
                    self.runJsFile('pub-showhide.js', driver);
                    tagas = driver.find_elements_by_tag_name("body")[0].find_elements_by_tag_name('a')
                    tagaslen = len(tagas)
                    
                    print(self.tag_type+"  cur_click_times:",self.cur_click_times,'/',tagaslen)
                    if(self.cur_click_times >= tagaslen - 1):
                        break
                    
                    tag = tagas[self.cur_click_times]
                    print(tag.text,'---',tag.get_property('href'))
                    tag.click()
                   
                elif self.tag_type == 'button':
                    self.runJsFile('pub-showhide.js', driver);
                    tagas = driver.find_elements_by_xpath("//input[@type='button']|//input[@type='submit'] ")
                    tagaslen = len(tagas)
                    
                    print(self.tag_type+"  cur_click_times:",self.cur_click_times,'/',tagaslen)
                    if(self.cur_click_times >= tagaslen - 1):
                        break
                    
                    tag = tagas[self.cur_click_times]
                    print(tag.text,'---',tag.get_property('value'))
                    tag.click()
                
                
                print ('after_click:',driver.current_url,'   url:',url)
                logs = driver.get_log('browser')
                print(len(logs))
                print(logs)
                print('----------------------------')
                for log in logs:
                    try:
                        urljson = json.loads(log)
                        postData = ''
                        if(urljson['method']=='POST'):
                            postData =urljson['postData']
                        self.dealOneUrl(urljson['url'],urljson['method'],postData)
                    except:
                        print('异常了：',log)
                        print(sys.exc_info()[0],sys.exc_info()[1])
                        
            except:
                print('大异常了：',driver.current_url)
#                 raise Exception("抛出一个异常")#
                print(sys.exc_info()[0],sys.exc_info()[1])
            if(self.cur_click_times >= tagaslen - 1):
                break
            self.cur_click_times = self.cur_click_times +1;
        driver.close()

    def dealOneUrl(self,url,method,postData):
#         url = urljson['url']
#         method = urljson['method']
        fullUrl = ''
        if(url.find('?') > 0):
            shortUrl = url[:url.find("?")].replace(self.prog_root,"").replace("//","/")
        else:
            shortUrl = url.replace(self.prog_root,"").replace("//","/")
        
        '''地址以.do或.jsp结尾的才有用'''
        if shortUrl.endswith(".do") or shortUrl.endswith(".jsp") :
            paramsResult = ''
            '''取参数'''
            if(method == 'POST'):
#                 postData = urljson['postData']
                paramsResult = self.dealParam(postData)
                fullUrl = self.prog_root + shortUrl + "?" + postData
            else:
                if(url.find("?") > 0):
                    paramStr = url[url.find("?") + 1:]
                    paramsResult = self.dealParam(paramStr)
                fullUrl = url
            msg = shortUrl + '--------'+paramsResult[0]
            self.insertUrl(shortUrl, paramsResult[0],paramsResult[1],paramsResult[2],fullUrl)
            print (msg)
            
    '''将参数去掉值用逗号连接'''
    def dealParam(self,paramStr):
        params = ''
        paramsHasId = ''
        paramsEndwidthId = ''
        params1 = paramStr.split('&')
        for params2 in params1:
            param = params2[:params2.find("=")]
            if( params == ''):
                params = param
            else:
                params = params + ',' + param 
            if param.find('Id') > 0 or param.find("id") > 0:
                if( paramsHasId == ''):
                    paramsHasId = param
                else:
                    paramsHasId = paramsHasId + ',' + param 
            if param.endswith('Id')  or param.endswith("id"):
                if( paramsEndwidthId == ''):
                    paramsEndwidthId = param
                else:
                    paramsEndwidthId = paramsEndwidthId + ',' + param 
        return params ,paramsHasId,paramsEndwidthId,paramsEndwidthId

    def runJsFile(self,jsFilePath,driver):
#         file_object = open(jsFilePath,'utf-8')
#         try:
#             all_the_text = file_object.read( )
        driver.execute_script("var tags=document.getElementsByTagName('*');for(var i=0;i < tags.length; i++){tags[i].style.display= 'block';tags[i].removeAttribute('disabled')}")
#         driver.execute_script("var tags=document.getElementsByTagName('a');for(var i=0;i < tags.length; i++){tags[i].style.display= 'block';}")
#         finally:
#             file_object.close( )

    def insertUrl(self,url,paramStr,paramsHasId,paramsEndwidthId,fullUrl):
        # 打开数据库连接
        db = pymysql.connect(self.db_url,self.db_username,self.db_password,self.db_name,charset=self.db_encode)
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        
        num = cursor.execute("select 1 from bak_slf_define where url='%s' " % (url))
        if(num == 0):
            # 使用execute方法执行SQL语句
            cursor.execute("INSERT INTO bak_slf_define (url,param,param_has_id,param_endwidth_id) VALUES ('%s', '%s', '%s', '%s')" % (url,paramStr,paramsHasId,paramsEndwidthId))
        
        num = cursor.execute("select 1 from bak_slf_define_full where url='%s'" % (url))
        if(num == 0):
            cursor.execute("INSERT INTO bak_slf_define_full (url,full_url) VALUES ('%s', '%s')" % (url,fullUrl))
        
        # 关闭数据库连接
        db.close()  
        
    
        
    def dealOnePage(self,url):
        self.tag_type='button'
        self.dealOnePageOneTag(url);
        
        self.tag_type='a'
        self.dealOnePageOneTag(url);
        
    def dealAllPage(self):
        while True:
            cf = configparser.ConfigParser()
            cf.read(self.ini_path)  
            self.cur_full_id = cf.get("baseconf", "cur_full_id") 
            
            # 打开数据库连接
            db = pymysql.connect(self.db_url,self.db_username,self.db_password,self.db_name,charset=self.db_encode)
            # 使用cursor()方法获取操作游标 
            cursor = db.cursor(pymysql.cursors.DictCursor)
            
            num = cursor.execute("select * from bak_slf_define_full where id>'%s' order by id" % (self.cur_full_id))
            if(num == 0):
                db.close() 
                return 
            rows = cursor.fetchall()
            for row in rows:
                fullUrl = row['full_url']
                self.dealOnePage(fullUrl)
                
                cf.set("baseconf", "cur_full_id", str(row['id']))  
                self.cur_full_id = row['id']
                cf.write(open(self.ini_path, "w"))
            
            # 关闭数据库连接
            db.close()  
        

    def addColData(self):
        # 打开数据库连接
        db = pymysql.connect(self.db_url,self.db_username,self.db_password,self.db_name,charset=self.db_encode)
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        num = cursor.execute("select * from bak_slf_define")
        if(num == 0):
            db.close() 
            return 
        rows = cursor.fetchall()
        for row in rows:
            url = row['url']
            cursor.execute("select * from tpriv_page_define where page_name='"+url+"'")
            rows1 = cursor.fetchall()
            row1 = rows1[0]
            cursor.execute("update bak_slf_define set page_id = '%s', obj_name = '%s', oper_name = '%s' where url='%s'" % (row1['page_id'],row1['obj_name'],row1['oper_name'],url))
        # 关闭数据库连接
        db.close()  
        
    def addColData1(self):
        # 打开数据库连接
        db = pymysql.connect(self.db_url,self.db_username,self.db_password,self.db_name,charset=self.db_encode)
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        num = cursor.execute("select * from bak_slf_define")
        if(num == 0):
            db.close() 
            return 
        rows = cursor.fetchall()
        for row in rows:
            url = row['url']
            cursor.execute("select * from tpriv_page_define where page_name='"+url+"'")
            rows1 = cursor.fetchall()
            row1 = rows1[0]
            cursor.execute("update bak_slf_define set page_id = '%s', obj_name = '%s', oper_name = '%s' where url='%s'" % (row1['page_id'],row1['obj_name'],row1['oper_name'],url))
        # 关闭数据库连接
        db.close()  

if __name__ == '__main__':
#     RadNews().dealOnePage('http://go108.enorth.com.cn:8080/pub/page_guide_visual/PageGuideVisualDragAction!visualDragNewsBegin.do?vo.guideId=100036158&channelId=91000000000000000&treeStartId=91000000000000000&svo.channelId=91000000000000000')
#         RadNews().dealAllPage()
#     driver = webdriver.PhantomJS(executable_path=r"C:\Program Files (x86)\phantomjs-2.1.1-windows\bin\phantomjs.exe",service_args=['--ignore-ssl-errors=true','--load-images=false'])
#     help(driver)
#     RadNews().addColData()
    RadNews().addColData1()
#      urljson = json.loads('{"headers":[{"name":"Accept","value":"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01"},{"name":"Referer","value":"http://go108.enorth.com.cn:8080/pub/guide_design/PageGuideDesignAction!Main.do?isCrossDomain=0&channelId=92000000000000000&pageGuideId=100008004&treeStartId=92000000000000000&svo.channelId=92000000000000000"},{"name":"X-Requested-With","value":"XMLHttpRequest"},{"name":"User-Agent","value":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "}],"id":606,"method":"GET","time":"2017-12-05T07:48:31.087Z","url":"http://go108.enorth.com.cn:8080/pub/js/lang/zh-cn.js?_=1512460110725"}')
    #         driver.find_element_by_class_name("update").click()
#         driver.execute_script('save();')
        
#         try:
#             alert = driver.switch_to.alert
#             print (alert.text)
#             alert.accept()
#         except Exception:
#             print("没有alert")
        
        
        
#         print ('page_source------------',driver.page_source)
        
#         driver.get(url)
#         driver.find_element_by_class_name("update").click()
#         driver.re
#         time.sleep(3)  
#         print (driver.current_url)
#         print (driver.find_element_by_tag_name('body').get_attribute('innerHTML'))
        
#         driver.get(url)
#         tags = driver.find_element_by_tag_name('*') 
#         for tag in tags:
#             tag.get_property
#         driver.close()
#         time.sleep(1)
        
#     obj.find_element_by_id('kw')                    #通过ID定位
#     obj.find_element_by_class_name('s_ipt')         #通过class属性定位
#     obj.find_element_by_name('wd')                  #通过标签name属性定位
#     obj.find_element_by_tag_name('input')           #通过标签属性定位
#     obj.find_element_by_css_selector('#kw')         #通过css方式定位
#     obj.find_element_by_xpath("//input[@id='kw']")  #通过xpath方式定位
#     obj.find_element_by_link_text("贴吧")           #通过xpath方式定位
 
#     su = obj.find_element_by_id('su')                    #通过ID定位
#     print su.get_property("value"),'--',su.location()
#     print obj.find_element_by_id('kw').tag_name   #获取标签的类型
