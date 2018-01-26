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
import re
from film.dao.daily_film_round_dao import DailyFilmRoundDao, DailyFilmRoundItem

'''猫眼处理类'''
class MaoyanHandler():
    website_id = 1
    
#     film_list_url = 'http://m.maoyan.com/'
    
    def dealOneDay(self,dateStr):
        #取我们从Fiddler中得到的Request URL
        film_list_url = 'http://m.maoyan.com/movielist?_v_=yes'
        headers = {'User-Agnet': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36', 'Connection': 'keep-alive'}
        #将POST需要的参数放入values字典中
        values = {}
        values['limit'] = '1000'  
        values['offset'] = '0'  
        #由于Request中的data参数必须是bytes二进制形式，用urlencode将字典转换成str，再encode编码成二进制。
        data = urllib.parse.urlencode(values).encode('utf-8')
        request = urllib.request.Request(url=film_list_url, data=data, headers=headers)
        response = urllib.request.urlopen(request)
        movieList = response.read().decode('utf-8')
        movieJsonList = json.loads(movieList)
        hotList = movieJsonList['hot']
        '''电影信息进tf_film表'''
        for movieJson in hotList:
            print('开始插入电影:',movieJson['id'],'---',movieJson['nm'])
            self.insertOneFilm(movieJson)
            print('完成插入电影:',movieJson['id'],'---',movieJson['nm'])
#         print(movieJsonList)
        '''按照电影获取影院列表'''
        film_cinema_url = 'http://m.maoyan.com/cinema/movie/moviedaycinemas?_v_=yes'
#         删一下今天的数据
        dateInt = int(dateStr.replace("-",""))
        self.deleteOneDay(dateInt)
        for movieJson in hotList:
            hasMore = True
            offset = 0
            movieId = movieJson['id']
            while hasMore == True:
                print('movieId:',movieId)
                try:
                    film_cinema_values = {}
                    film_cinema_values['limit'] = 20#必须20条一篇  
                    film_cinema_values['offset'] = offset
                    film_cinema_values['movieId'] = movieId  
                    film_cinema_values['day'] = dateStr 
                    #由于Request中的data参数必须是bytes二进制形式，用urlencode将字典转换成str，再encode编码成二进制。
                    film_cinema_data = urllib.parse.urlencode(film_cinema_values).encode('utf-8')
                    film_cinema_request = urllib.request.Request(url=film_cinema_url, data=film_cinema_data, headers=headers)
                    film_cinema_response = urllib.request.urlopen(film_cinema_request)
                    movieList = film_cinema_response.read().decode('utf-8')
                    movieCinemaJson = json.loads(movieList)
#                     print(movieCinemaJson)
                    paging = movieCinemaJson['paging']
                    if hasMore == True:
                        cinemas=movieCinemaJson['cinemas']
                        for cinema in cinemas:
                            print('开始插入影院:',dateInt,'---',cinema.get('nm'))
                            self.insertOneCinema(cinema)
                            print('完成插入影院:',dateInt,'---',cinema.get('nm'))
                            print('开始插入电影影院关联:',dateInt,'---',movieJson.get('nm'),'---',cinema.get('nm'))
                            self.inertOneDailyFilmCinema(dateInt, movieJson, cinema)
                            print('完成插入电影影院关联:',dateInt,'---',movieJson.get('nm'),'---',cinema.get('nm'))
#                             print(movieId,'------',cinema)
                    time.sleep(0.5)
                except:
    #                 raise Exception("抛出一个异常")#
                    print('按照电影影院异常:电影id=',movieId,sys.exc_info()[0],sys.exc_info()[1])
                hasMore = paging['hasMore']
#                 20条一篇
                offset = offset + 20
#                 print(movieId,'------',movieCinemaList)
            #记录每天每个电影的总场次
            self.insertDailyFilmRound(movieJson, dateInt)
            print('\n\n')
            time.sleep(1)
            
    def insertOneFilm(self,movieJson):
        filmItem = FilmItem()
        filmItem.filmName = movieJson['nm']
        filmItem.websiteId=self.website_id
        filmItem.websiteFilmId=movieJson['id']
        filmItem.grade = movieJson['score']
        if(movieJson.__contains__('showTimeInfo')):
            showTime = movieJson['showTimeInfo'][:10].replace('-','')
            filmItem.showTime = showTime
        if(movieJson.get('buy') == -1):
            filmItem.showState = 1
        elif(movieJson.get('buy') == -2):
            filmItem.showState = 0
        filmItem.img = movieJson.get('img')
        if(movieJson.__contains__('ver')):
            filmItem.ver = movieJson.get('ver')
        '''演员'''
        if(movieJson.__contains__('desc')):
            filmItem.actor = movieJson.get('desc').replace('主演:','')
        if(movieJson.__contains__('fra')):
            filmItem.country = movieJson.get('fra')
        filmItem.direct = movieJson['dir']
        filmItem.clob = str(movieJson).replace('\'','\\\'')
        filmItem.filmType=movieJson['cat']
        print('插入：',filmItem.filmName)
        filmDao= FilmDao()
        filmDao.insertNew( filmItem)
        print('完成：',filmItem.filmName)
        
    def insertOneCinema(self,cinemaJson):
        cinemaItem = CinemaItem()
        cinemaItem.cinemaName = cinemaJson.get('nm')
        cinemaItem.websiteId=self.website_id
        cinemaItem.websiteCinemaId=cinemaJson.get('id')
        cinemaItem.area = ''
#         cinemaItem.mergeId = -1
        cinemaItem.addr = cinemaJson.get('addr')
        cinemaItem.state = '1'
        cinemaDao = CinemaDao()
        cinemaDao.insertNew(cinemaItem)
        
    def inertOneDailyFilmCinema(self,dateInt,movieJson,cinemaJson):
        dailyFilmCinemaItem = DailyFilmCinemaItem()
        dailyFilmCinemaItem.websiteId=self.website_id
        dailyFilmCinemaItem.websiteFilmId = movieJson.get('id')
        dailyFilmCinemaItem.websiteCinemaId=cinemaJson.get('id')
        dailyFilmCinemaItem.grade = movieJson.get('score')
        print(dailyFilmCinemaItem.grade)
        dailyFilmCinemaItem.dateNo = dateInt
        if(movieJson.get('buy') == -1):
            dailyFilmCinemaItem.showState = 1
        elif(movieJson.get('buy') == -2):
            dailyFilmCinemaItem.showState = 0
        dailyFilmCinemaItem.price = cinemaJson.get('price')
        dailyFilmCinemaDao = DailyFilmCinemaDao()
        dailyFilmCinemaDao.insert(dailyFilmCinemaItem)
        return dailyFilmCinemaItem
    
    '''上映影院数/场次  例： 上映45天，累计票房9618万'''
    def insertDailyFilmRound(self,movieJson,dateInt):
        showInfo = movieJson.get('showInfo')
        movieId = movieJson['id']
        dailyFilmRoundDao = DailyFilmRoundDao()
        if(showInfo != None):
            showInfoObj = re.match(r'今天([0-9]*)家影院放映([0-9]*)场', showInfo)
            if showInfoObj:
                dailyFilmRoundItem = DailyFilmRoundItem()
                dailyFilmRoundItem.dateNo = dateInt
                dailyFilmRoundItem.showRoundNum = showInfoObj.group(2)
                dailyFilmRoundItem.showCinemaNum = showInfoObj.group(1)
                dailyFilmRoundItem.websiteId = self.website_id
                dailyFilmRoundItem.websiteFilmId = movieId
                dailyFilmRoundDao.insert(dailyFilmRoundItem)
    
    def deleteOneDay(self,dateInt):
        dailyFilmCinemaDao = DailyFilmCinemaDao()
        dailyFilmCinemaDao.deleteOneDay(dateInt, self.website_id);
        
        '''清空今天大众点评的tf_daily_fim_round表'''
        dailyFilmRoundDao = DailyFilmRoundDao()
        dailyFilmRoundDao.deleteOneDay(dateInt, self.website_id)
        
if __name__ == '__main__':
    MaoyanHandler().dealOneDay('2017-12-20')
#     s = '上映45天，累计票房9618万'
#     s = '1232qeq'
#     matchObj = re.match(r'上映([0-9]*)天，累计票房([0-9]*)万', s)
#     if(matchObj):
#         print('qweqweeqw')
#     help(matchObj.__bool__)
#     print("ddd",matchObj.lastindex)
#     print ("matchObj.group() : ", matchObj.group())
#     print ("matchObj.group(1) : ", matchObj.group(1))
#     print ("matchObj.group(2) : ", matchObj.group(2))
    
    