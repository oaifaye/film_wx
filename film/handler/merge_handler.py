# -*- coding: UTF-8 -*-
'''
Created on 2017年12月16日

@author: Administrator
'''
from film.dao.cinema_dao import CinemaDao
from film.dao.cinema_merge_dao import CinemaMergeDao, CinemaMergeItem
from film.dao.film_dao import FilmDao
from film.dao.film_merge_dao import FilmMergeDao, FilmMergeItem

class MergeCinemaHandler():
    def merge(self):
        cinemaDao = CinemaDao()
        noMergeCinemas = cinemaDao.getNoMergeCinema()
        if len(noMergeCinemas) == 0:
            return
        cinemaMergeDao = CinemaMergeDao()
        for noMergeCinema in noMergeCinemas:
            cinemaMerge = cinemaMergeDao.getByCinemaName(noMergeCinema.cinemaName)
            mergeId = -1
            if cinemaMerge == None:
                cinemaMergeItem = CinemaMergeItem()
                cinemaMergeItem.cinemaName  =noMergeCinema.cinemaName
                cinemaMergeItem.addr  =noMergeCinema.addr
                cinemaMergeItem.area  =noMergeCinema.area
                cinemaMergeItem.state  =1
                insertRes = cinemaMergeDao.insertNew(cinemaMergeItem)
                mergeId = insertRes.id
            else :
                mergeId = cinemaMerge.id
            cinemaDao.updateCinemaMergeId(noMergeCinema.id, mergeId)
            
    def updateMergeCinemaArea(self):
        cinemaMergeDao = CinemaMergeDao()
        noAreaCinemas = cinemaMergeDao.getNoAreaCinema()
        if len(noAreaCinemas) == 0:
            return
        cinemaDao = CinemaDao()
        for noAreaCinema in noAreaCinemas:
            hasAreaCinemas = cinemaDao.getHasAreaCinema(noAreaCinema.id)
            for hasAreaCinema in hasAreaCinemas:
                if(hasAreaCinema.area!=''):
                    cinemaMergeDao.updateArea(noAreaCinema.id, hasAreaCinema.area)
                    break
            
class MergeFilmHandler():
    def merge(self):
        filmDao = FilmDao()
        noMergeFilms = filmDao.getNoMergeFilm()
        if len(noMergeFilms) == 0:
            return
        filmMergeDao = FilmMergeDao()
        for noMergeFilm in noMergeFilms:
            filmMerge = filmMergeDao.getByFilmName(noMergeFilm.filmName)
            mergeId = -1
            if filmMerge == None:
                filmMergeItem = FilmMergeItem()
                filmMergeItem.filmName = noMergeFilm.filmName
                filmMergeItem.grade = noMergeFilm.grade
                filmMergeItem.showTime = noMergeFilm.showTime
                filmMergeItem.showState = noMergeFilm.showState
                filmMergeItem.img = noMergeFilm.img
                filmMergeItem.filmType = noMergeFilm.filmType
                filmMergeItem.ver = noMergeFilm.ver
                filmMergeItem.actor = noMergeFilm.actor
                filmMergeItem.country = noMergeFilm.country
                filmMergeItem.direct = noMergeFilm.direct
                filmMergeItem.initDate = noMergeFilm.initDate
                filmMergeItem.duration = noMergeFilm.duration
                insertRes = filmMergeDao.insertNew(filmMergeItem)
                mergeId = insertRes.id
            else :
                mergeId = filmMerge.id
            filmDao.updateFilmMergeId(noMergeFilm.id,mergeId )
            
if __name__ == '__main__':
#     MergeCinemaHandler().merge()
#     MergeFilmHandler().merge()
    MergeCinemaHandler().updateMergeCinemaArea()
            