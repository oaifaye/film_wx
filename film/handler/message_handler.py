'''
Created on 2017年12月20日

@author: Administrator
'''
from film.dao.message_dao import MessageDao, MessageItem
from film.handler.calc_handler import Calc
class MessageHandler():
    ms_template_grade_head = "评分高的小电影推荐：\n"
    ms_template_round_head = "大家伙儿都在看小电影：\n"
    ms_template_body = "[%s(%s)]:建议去[%s]买张[%s]影院的票;\n"
    
    def insertOneDayOneType(self,dateNo,calcType):
        messageDao= MessageDao()
        #删除今天
        messageDao.deleteOneDay(dateNo, calcType)
        templateHead = ''
        if(Calc.calc_type_grade == calcType):
            templateHead = self.ms_template_grade_head
        elif (Calc.calc_type_round == calcType):
            templateHead = self.ms_template_round_head
        messageContentItems = messageDao.getCalcMessage(dateNo, calcType)
        msContent = str(dateNo)+templateHead
        for messageContentItem in messageContentItems:
            ms = (self.ms_template_body % \
                  (messageContentItem.filmName,messageContentItem.filmType,messageContentItem.websiteName,messageContentItem.cinemaName))
            msContent = msContent + ms
        print(msContent)
        messageItem = MessageItem()
        messageItem.dateNo = dateNo
        messageItem.msType = calcType
        messageItem.content = msContent
        messageDao.insert(messageItem)
    
    def insertOneDay(self,dateNo):
        self.insertOneDayOneType(dateNo, Calc.calc_type_grade)
        self.insertOneDayOneType(dateNo, Calc.calc_type_round)

        
if __name__ == '__main__':
    MessageHandler().insertOneDay( 20171220, Calc.calc_type_grade)