from film.handler.dinping_handler import  DianpingHandler
import datetime
from film.dao.daily_log_dao import DailyLogDao
import sys
import time
from film.handler.maoyan_handler import MaoyanHandler
from film.handler.merge_handler import MergeCinemaHandler, MergeFilmHandler
from film.dao.calc_dao import CalcDao
from film.handler.calc_handler import Calc
from film.handler.message_handler import MessageHandler
from film.wx.wx import WXSender, WXUtil
from film.dao.message_dao import MessageDao

class Timer():
    def doTask(self):
        self.doOneDay(datetime.datetime.now())
        
    def doMessgeTask(self):
        self.doOneDayMessage(datetime.datetime.now())
            
    def doOneDay(self,date):
        print("当前时间："+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        todayStr = date.strftime("%Y-%m-%d")
        dateNo = int(date.strftime("%Y%m%d"))
        dailyLogDao= DailyLogDao()
        try:
            maoyanHandler = MaoyanHandler()
            dailyLogDao.deleteFailed(dateNo, maoyanHandler.website_id,dailyLogDao.log_type_snatch)
            if dailyLogDao.hasDailyLog(dateNo,maoyanHandler.website_id,dailyLogDao.log_type_snatch) == False:
                dailyLogDao.insertStart(dateNo, maoyanHandler.website_id,dailyLogDao.log_type_snatch)
                maoyanHandler.dealOneDay(todayStr)
                dailyLogDao.successEnd(dateNo, maoyanHandler.website_id,dailyLogDao.log_type_snatch)
        except:
            msg = '猫眼抓电影电影发生异常：'+str(sys.exc_info()[0])+str(sys.exc_info()[1])
            print(msg)
            dailyLogDao.failEnd(dateNo, maoyanHandler.website_id, msg,dailyLogDao.log_type_snatch)
            
        try:
            dianpingHandler = DianpingHandler()
            dailyLogDao.deleteFailed(dateNo, dianpingHandler.website_id,dailyLogDao.log_type_snatch)
            if dailyLogDao.hasDailyLog(dateNo,dianpingHandler.website_id,dailyLogDao.log_type_snatch) == False:
                dailyLogDao.insertStart(dateNo, dianpingHandler.website_id,dailyLogDao.log_type_snatch)
                dianpingHandler.dealOneDay(todayStr)
                dailyLogDao.successEnd(dateNo, dianpingHandler.website_id,dailyLogDao.log_type_snatch)
        except:
            msg = '大众点评抓电影电影发生异常：'+str(sys.exc_info()[0])+str(sys.exc_info()[1])
            print(msg)
            dailyLogDao.failEnd(dateNo, dianpingHandler.website_id, msg,dailyLogDao.log_type_snatch)

        try:
            print ('开始和数据：'+todayStr)
            MergeCinemaHandler().merge()
            MergeFilmHandler().merge()
            print ('完成和数据：'+todayStr)
        except:
            msg = '和数据发生异常：'+str(sys.exc_info()[0])+str(sys.exc_info()[1])
            print(msg)
            
        print ('开始归档评分数据：'+todayStr)
        try:
            calc = Calc()
            dailyLogDao.deleteFailed(dateNo, -1,dailyLogDao.log_type_calc_grade)
            if dailyLogDao.hasDailyLog(dateNo,-1,dailyLogDao.log_type_calc_grade) == False:
                dailyLogDao.insertStart(dateNo, -1,dailyLogDao.log_type_calc_grade)
                calc.calcByGrade(dateNo)
                dailyLogDao.successEnd(dateNo, -1,dailyLogDao.log_type_calc_grade)
        except:
            msg = '归档评分发生异常：'+str(sys.exc_info()[0])+str(sys.exc_info()[1])
            print(msg)
            dailyLogDao.failEnd(dateNo, -1, msg,dailyLogDao.log_type_calc_grade)
        print ('完成归档评分数据：'+todayStr)
        
        print ('开始归档评分数据：'+todayStr)
        try:
            calc = Calc()
            dailyLogDao.deleteFailed(dateNo, -1,dailyLogDao.log_type_calc_round)
            if dailyLogDao.hasDailyLog(dateNo,-1,dailyLogDao.log_type_calc_round) == False:
                dailyLogDao.insertStart(dateNo, -1,dailyLogDao.log_type_calc_round)
                calc.calcByGrade(dateNo)
                calc.calcByMostRound(dateNo)
                dailyLogDao.successEnd(dateNo, -1,dailyLogDao.log_type_calc_round)
        except:
            msg = '归档评分发生异常：'+str(sys.exc_info()[0])+str(sys.exc_info()[1])
            print(msg)
            dailyLogDao.failEnd(dateNo, -1, msg,dailyLogDao.log_type_calc_round)
        print ('完成归档评分数据：'+todayStr)
        
        print ('开始向message表插数据：'+todayStr)
        try:
            dailyLogDao.deleteFailed(dateNo, -1,dailyLogDao.log_type_calc_message)
            if dailyLogDao.hasDailyLog(dateNo,-1,dailyLogDao.log_type_calc_message) == False:
                dailyLogDao.insertStart(dateNo, -1,dailyLogDao.log_type_calc_message)
                messageHandler = MessageHandler()
                messageHandler.insertOneDay(dateNo)
                dailyLogDao.successEnd(dateNo, -1,dailyLogDao.log_type_calc_message)
        except:
            msg = '向message表插数据发生异常：'+str(sys.exc_info()[0])+str(sys.exc_info()[1])
            print(msg)
            dailyLogDao.failEnd(dateNo, -1, msg,dailyLogDao.log_type_calc_message)
        print ('完成向message表插数据：'+todayStr)
        
    def doOneDayMessage(self,date):
        todayStr = date.strftime("%Y-%m-%d")
        dateNo = int(date.strftime("%Y%m%d"))
        
        dailyLogDao = DailyLogDao()
        print ('开始发微信：'+todayStr)
        try:
            '''7点以后、今天没有发过、message表里有数据才发微信'''
            nowH = int(datetime.datetime.now().strftime("%H"))
            if(nowH > 7):
                dailyLogDao.deleteFailed(dateNo, -1,dailyLogDao.log_type_calc_send_message)
                if dailyLogDao.hasDailyLog(dateNo,-1,dailyLogDao.log_type_calc_send_message) == False:
                    messageDao = MessageDao()
                    roundContent= messageDao.selectContent(dateNo, DailyLogDao.log_type_calc_round)
                    gradeContent= messageDao.selectContent(dateNo, DailyLogDao.log_type_calc_grade)
                    if(roundContent != None and gradeContent != None):
                        ''''开始发微信'''
                        print ('真的发微信：'+todayStr)
                        dailyLogDao.insertStart(dateNo, -1,dailyLogDao.log_type_calc_send_message)
                        WXSender().send(dateNo=dateNo)
                        dailyLogDao.successEnd(dateNo, -1,dailyLogDao.log_type_calc_send_message)
                        print ('真的完成发微信：'+todayStr)
        except:
            msg = '发微信发生异常：'+str(sys.exc_info()[0])+str(sys.exc_info()[1])
            print(msg)
            dailyLogDao.failEnd(dateNo, -1, msg,dailyLogDao.log_type_calc_send_message)
        print ('完成发微信：'+todayStr)
        
        print("当前时间："+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
if __name__ == '__main__':
    
    '''起其它任务'''
    while True:
        Timer().doTask()
        Timer().doMessgeTask()
        time.sleep(3600*1)
# timestr = "time2009-12-14"
# t = time.strptime(timestr, "time%Y-%m-%d")
# print (t)
