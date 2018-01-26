# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
import time
import datetime
import random
import sched

# proxy = Proxy]
# {
# 'proxyType': ProxyType.MANUAL,
# 'httpProxy': '222.217.68.148:8089'  # 代理ip和端口
# }
# )

class RadNews():
    hourDic={
        '00':13,
        '01':5,
        '02':3,
        '03':3,
        '04':3,
        '05':9,
        '06':4,
        '07':14,
        '08':43,
        '09':56,
        '10':63,
        '11':64,
        '12':65,
        '13':65,
        '14':59,
        '15':56,
        '16':60,
        '17':71,
        '18':99,
        '19':114,
        '20':121,
        '21':95,
        '22':49,
        '23':15,
    }
    
    mod= 3.9

    urls=[
#           'http://www.pub.demo2016.2000cms.cn/test/system/2017/11/24/030014340.shtml',
#           'http://www.pub.demo2016.2000cms.cn/test/system/2017/11/24/030014324.shtml',
#           'http://www.pub.demo2016.2000cms.cn/test/system/2017/09/20/030013910.shtml',
#           'http://www.pub.demo2016.2000cms.cn/test/system/2017/09/20/030013911.shtml',
#           'http://www.pub.demo2016.2000cms.cn/test/system/2017/09/20/030013908.shtml',
#           'http://www.pub.demo2016.2000cms.cn/test/system/2017/09/20/030013922.shtml',
#           'http://www.pub.demo2016.2000cms.cn/jxnews/system/2016/11/14/030013413.shtml',
#           'http://www.pub.demo2016.2000cms.cn/jxnews/system/2016/10/25/030013219.shtml',
#           'http://www.pub.demo2016.2000cms.cn/jxnews/system/2016/10/25/030013218.shtml',
#           'http://www.pub.demo2016.2000cms.cn/jxnews/system/2016/10/24/030013131.shtml',
#           'http://www.pub.demo2016.2000cms.cn/jxnews/system/2016/10/08/030012503.shtml',
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
    
    dcap = dict(DesiredCapabilities.PHANTOMJS)  #设置userAgent
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")
    
    proxy = [
                '--proxy=113.83.217.180:9797',
            ]
    
    
    
    def dealOneHour(self,hour):
        print 'hour:',hour
        num = int(self.hourDic[hour])
        num = int(num * self.mod)
        print 'num:',num
        for i in range(0,num):
            url = random.choice(self.urls) 
            print 'i:',i,'  num:',num,'  url:',url
            try:
                self.dealOneUrl(url)
            except Exception as e:
                print url,'  e:',e
        
    def dealOneUrl(self,url):
        obj = webdriver.PhantomJS(executable_path=r"C:\Program Files (x86)\phantomjs-2.1.1-windows\bin\phantomjs.exe",desired_capabilities=self.dcap)
#         obj = webdriver.PhantomJS(executable_path=r"C:\Program Files (x86)\phantomjs-2.1.1-windows\bin\phantomjs.exe",desired_capabilities=self.dcap,service_args=self.proxy)
        obj.set_page_load_timeout(6)
        obj.get(url)
        obj.close()
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
    def dealAllTime(self ):
        now = datetime.datetime.now()
        print '开始定时任务咯：',now
        hour = now.strftime('%H')  
        self.dealOneHour(hour)
        
    def test(self ):
        print '开始1111'



if __name__ == '__main__':
    
#     print 99*1.1,'---',int(99*1.1)
    while True:
        RadNews().dealAllTime()
        time.sleep(3600)
    
