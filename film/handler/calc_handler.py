'''
Created on 2017年12月17日

@author: Administrator
'''
from film.dao.cinema_merge_dao import CinemaMergeDao
from film.dao.calc_dao import CalcDao
from film.dao.film_dao import FilmDao

class Calc():
    calc_type_grade = 'calc_grade'
    calc_type_round = 'calc_round'
    
    def calcByGrade(self,dateNo):
        calcDao = CalcDao()
        mergeFilmIds = calcDao.getGradeHiFilm(dateNo)
        calcDao.deleteByDateNo(dateNo, self.calc_type_grade)
        for mergeFilmId in mergeFilmIds:
            calcItems = calcDao.getCheapCimane(mergeFilmId, dateNo)
            if(len(calcItems) == 0):
                continue
            calcItem = calcItems[0]
            calcItem.calcType = self.calc_type_grade
            calcDao.insert(calcItem)
                
    def calcByMostRound(self,dateNo):
        calcDao = CalcDao()
        mergeFilmIds = calcDao.getMostRoundFilms(dateNo)   
        calcDao.deleteByDateNo(dateNo, self.calc_type_round)
        for mergeFilmId in mergeFilmIds:
            calcItems = calcDao.getCheapCimane(mergeFilmId, dateNo)
            if(len(calcItems) == 0):
                continue
            calcItem = calcItems[0]
            calcItem.calcType = self.calc_type_round
            calcDao.insert(calcItem)
    
if __name__ == '__main__':
    Calc().calcByGrade(20171220)
    Calc().calcByMostRound(20171220)