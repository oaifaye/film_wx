# -*- coding: UTF-8 -*-

from selenium import webdriver

import urllib.request
import urllib.parse
import json
import time
from film.dao.film_dao import FilmItem, FilmDao
from film.dao.cinema_dao import CinemaItem, CinemaDao
import sys
from film.dao.daily_film_cinema_dao import DailyFilmCinemaDao,\
    DailyFilmCinemaItem
import lxml.html
from film.util.http_util import HttpUtil
from film.dao.daily_film_round_dao import DailyFilmRoundDao, DailyFilmRoundItem


# if __name__ == '__main__':
    
#     ss = '2017-12-15下周五上映'
#     print(ss[:10])

'''大众点评处理类'''
class DianpingHandler():
    website_id = 2
    page_encode = 'utf-8'
    
#     film_list_url = 'http://m.maoyan.com/'
    
    def dealOneDay(self,dateStr):
#         driver = webdriver.PhantomJS(executable_path=r"C:\Program Files (x86)\phantomjs-2.1.1-windows\bin\phantomjs.exe",desired_capabilities=self.dcap,service_args=['--ignore-ssl-errors=true','--load-images=false'])
#         driver.set_page_load_timeout(6)
#         driver.get(self.film_list_url)
        pageno = 1
        dateInt = int(dateStr.replace("-",""))
#         删一下今天的数据
        self.deleteOneDay(dateInt)
            
        #取我们从Fiddler中得到的Request URL
        film_list_url = 'http://t.dianping.com/movie/tianjin/playing?pageno='
        #由于Request中的data参数必须是bytes二进制形式，用urlencode将字典转换成str，再encode编码成二进制。
        while True:
            httpUtil = HttpUtil()
            doc = httpUtil.getLxmlDocFromUrl(film_list_url+str(pageno), self.page_encode)
            
            '''解析正文'''
            listitem = doc.xpath("//dl[@class='list-item']")
            if(len(listitem) == 0):
                break
            
            filmItems = []
            '''电影信息进tf_film表'''
            for filmDl in listitem:
                filmItem = self.insertOneFilm(filmDl)
                filmItems.append(filmItem)
                
            '''影院信息进tf_cinema表'''
            film_cinema_list_url = 'http://t.dianping.com/movie/ajax/movieDetail?cid=10&movieId='
            for filmItem1 in filmItems:
                #影院数/场次
                showCinemaNum = 0
                showRoundNum = 0
                #取出所有的区
                websiteFilmId = filmItem1.websiteFilmId
                try:
                    doc1 = httpUtil.getLxmlDocFromUrl(film_cinema_list_url+str(websiteFilmId), self.page_encode)
                except:
                    continue
                    print(filmItem1.filmName,'大众点评按照电影异常：',sys.exc_info()[0],sys.exc_info()[1])
                dailyFilmRoundDao = DailyFilmRoundDao()
                regiontriggers = doc1.xpath("//a[@class='J_region_trigger on']|//a[@class='J_region_trigger']")
                for regiontrigger in regiontriggers :
                    districtId = regiontrigger.xpath("attribute::data-id")[0]
                    areaName = regiontrigger.text
                    try:
                        doc3 = httpUtil.getLxmlDocFromUrl(film_cinema_list_url+str(websiteFilmId)+'&districtId='+districtId, self.page_encode)
                    except:
                        continue
                        print(filmItem1.filmName,'大众点评按照电影异常：',sys.exc_info()[0],sys.exc_info()[1])
                    
                    print(districtId,'--',areaName)
                    cinemaList = doc3.xpath("//div[@class='cinema-list']/span[@class='item']")
                    for cinema in cinemaList:
                        try:
                            cinemaid= cinema.xpath('a')[0].xpath("attribute::data-id")[0]
                            cinemaName = cinema.xpath('a')[0].text
                            print(film_cinema_list_url+str(websiteFilmId)+'&districtId='+districtId+"&cinemaId"+cinemaid+"&date="+dateStr)
                            doc2 = httpUtil.getLxmlDocFromUrl(film_cinema_list_url+str(websiteFilmId)+'&districtId='+districtId+"&cinemaId"+cinemaid+"&date="+dateStr, self.page_encode)
                            #计算最便宜的钱数和这个电影院的场次
                            cheapestArr = self.getCheapest(doc2)
                            cheapest = cheapestArr[0]
                            showCinemaNum = showCinemaNum + 1
                            showRoundNum = showRoundNum + cheapestArr[1]
                            cinemaItem = self.insertOneCinema(cinemaid,cinemaName,cheapest,areaName)
                            self.inertOneDailyFilmCinema(dateInt, filmItem1, cinemaItem, cheapest,showCinemaNum,showRoundNum)
                            print(filmItem1.filmName,areaName,cinemaid+cinemaName+str(cheapest))
                            time.sleep(0.5)
                        except:
    #                 raise Exception("抛出一个异常")#
                            print(filmItem1.filmName,'大众点评按照电影影院异常：',sys.exc_info()[0],sys.exc_info()[1])
                #记录每天每个电影的总场次
                dailyFilmRoundItem = DailyFilmRoundItem()
                dailyFilmRoundItem.dateNo = dateInt
                dailyFilmRoundItem.showRoundNum = showRoundNum
                dailyFilmRoundItem.showCinemaNum = showCinemaNum
                dailyFilmRoundItem.websiteId = self.website_id
                dailyFilmRoundItem.websiteFilmId = websiteFilmId
                dailyFilmRoundDao.insert(dailyFilmRoundItem)
            pageno = pageno +1 
            time.sleep(1)
    
    def insertOneFilm(self,filmDl):
        filmItem = FilmItem()
        filmItem.websiteId=self.website_id
        filmItem.showState = 1
        #图片
        filmItem.img = filmDl.xpath("dt/a/img")[0].xpath("attribute::src")[0]
        print(filmItem.img)
        dds = filmDl.xpath("dd")
        ddsindex = 0
        #0电影名称、id、imx/3d/2d、评分
        dd0 = dds[ddsindex].xpath("child::*")
        filmItem.filmName = dd0[0].text
        filmItem.websiteFilmId=dd0[0].xpath('attribute::href')[0].replace('/movie/','')
        if len(dd0[1].xpath('child::*')) > 0:
            filmItem.ver = dd0[1].xpath('child::*')[0].text
            print(filmItem.ver)
        filmItem.grade = dd0[2].xpath('child::*')[0].text
        print(filmItem.grade)
        ddsindex = ddsindex + 1
        
        #如果有class='story-tip'的元素 跳过
        ddsclasses = dds[ddsindex].xpath("attribute::class")
        print(ddsclasses)
        for ddsclass in ddsclasses:
            if ddsclass == 'story-tip':
                ddsindex = ddsindex + 1
                break
        
        #1导演
        filmItem.direct = dds[ddsindex].xpath('child::text()')[0]
        ddsindex = ddsindex + 1
        print(filmItem.direct)
        #2演员
        if len(dds[ddsindex].xpath('child::text()')) > 0:
            filmItem.actor = dds[ddsindex].xpath('child::text()')[0]
        ddsindex = ddsindex + 1
        print(filmItem.actor)
        #3类型
        filmItem.filmType = dds[3].xpath('child::text()')[0]
        ddsindex = ddsindex + 1
        print(filmItem.filmType)
        #4时长
        dd4text = dds[ddsindex].xpath('child::text()')[1].replace('\n','').replace('\t','').replace(' ','')
        ddsindex = ddsindex + 1
        print(dd4text)
        filmItem.country = dd4text[:dd4text.find('/')]
        print(filmItem.country)
        filmItem.duration = dd4text[dd4text.find('/')+1:].replace('分钟','')
        print(filmItem.duration)
        
        #5上映时间
        filmItem.showTime = dds[ddsindex].xpath('child::text()')[0].replace('上映','').replace('-','')
        ddsindex = ddsindex + 1
        print(filmItem.showTime)
        
        print('大众点评插入：',filmItem.filmName)
        filmDao= FilmDao()
        filmDao.insertNew(filmItem)
        print('大众点评完成：',filmItem.filmName)
        return filmItem
        
    def getCheapest(self,doc):
        prices = doc.xpath("//td[@class='s-price']")
        cheapest = 0
        for price in prices:
            if price.text.find('¥')>-1:
                priceNum = float(price.text[1:])
                if(priceNum < cheapest or cheapest == 0):
                    cheapest = priceNum
        return cheapest,len(prices)
    
    def insertOneCinema(self,websiteCinemaId,cinemaName,cheapest,areaName):
        cinemaItem = CinemaItem()
        cinemaItem.cinemaName = cinemaName
        cinemaItem.websiteId=self.website_id
        cinemaItem.websiteCinemaId=websiteCinemaId
        cinemaItem.area = areaName
#         cinemaItem.mergeId = -1
#         cinemaItem.addr = cinemaJson.get('addr')
        cinemaItem.state = '1'
        cinemaDao = CinemaDao()
        cinemaDao.insertNew(cinemaItem)
        return cinemaItem
        
    def inertOneDailyFilmCinema(self,dateInt,filmItem,cinemaItem,cheapest,showCinemaNum,showRoundNum):
        dailyFilmCinemaItem = DailyFilmCinemaItem()
        dailyFilmCinemaItem.websiteId=self.website_id
        dailyFilmCinemaItem.websiteFilmId = filmItem.websiteFilmId
        dailyFilmCinemaItem.websiteCinemaId=cinemaItem.websiteCinemaId
        dailyFilmCinemaItem.grade = filmItem.grade
        dailyFilmCinemaItem.dateNo = dateInt
        dailyFilmCinemaItem.showState = 1
        dailyFilmCinemaItem.price = cheapest
#         dailyFilmCinemaItem.showCinemaNum = showCinemaNum
#         dailyFilmCinemaItem.showRoundNum = showRoundNum
        dailyFilmCinemaDao = DailyFilmCinemaDao()
        dailyFilmCinemaDao.insert(dailyFilmCinemaItem)
    
    def deleteOneDay(self,dateInt):
        dailyFilmCinemaDao = DailyFilmCinemaDao()
        dailyFilmCinemaDao.deleteOneDay(dateInt, self.website_id);
        
        '''清空今天大众点评的tf_daily_fim_round表'''
        dailyFilmRoundDao = DailyFilmRoundDao()
        dailyFilmRoundDao.deleteOneDay(dateInt, self.website_id)
        
if __name__ == '__main__':
    DianpingHandler().dealOneDay('2017-12-20')