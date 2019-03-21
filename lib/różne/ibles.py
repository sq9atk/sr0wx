#!/usr/env/python -tt
# -*- encoding=utf8 -*-
#
#   Copyright 2009-2012 Michal Sadowski (sq6jnx at hamradio dot pl)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import urllib
import pygame
import datetime
import re
from config import ibles  as config

lang=None

def downloadFile(url):
    webFile = urllib.urlopen(url)
    return webFile.read()

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

strefy = [
        (  0,  0),
        ( 80,120), ( 40,190), (100,180),    # strefy:  1,  2,  3,
        ( 70,240), (140, 90), (200, 80),    #       :  4,  5,  6,
        (260, 50), (400, 90), (380,150),    #       :  7,  8,  9,
        (410,190), (510, 90), (550, 90),    #       : 10, 11, 12,
        (500,170), (550,200), (170,170),    #       : 13, 14, 15,
        (140,220), (200,200), (250,140),    #       : 16, 17, 18,
        (260,200), (320,170), (100,280),    #       : 19, 20, 21,
        ( 80,310), (170,260), (180,310),    #       : 22, 23, 24,
        (260,270), (250,350), (360,260),    #       : 25, 26, 27,
        (310,330), (360,360), (480,220),    #       : 28, 29, 30,
        (460,280), (440,340), (430,390),    #       : 31, 32, 33,
        (420,450), (560,310), (560,400),    #       : 34, 35, 36,
        (120,370), (180,390), (250,420),    #       : 37, 38, 39,
        (330,440), (390,490), (490,490),    #       : 40, 41, 42
        ]

poziomy = {
        #  R   G   B   A
        (255,  0,  0,255):  3, # zagrożenie duże
        (255,255,  0,255):  2, # zagrożenie średnie
        (  0,255,  0,255):  1, # zagrożenie małe
        (  0,  0,255,255):  0, # brak zagrożenia

        (250,250,212,255): -1, # rejon nieobjęty prognozowaniem
        (160,160,160,255): -2, # brak danych
        }

poziomy_nazwy = ['', 'male', 'srednie', 'duze', ]

def get_forecast_url():
    """Podaje dokładnie taki URL, na który powołuje się strona 
    ``http://bazapozarow.ibles.pl/zagrozenie/``, niekiedy bowiem poranne raporty
    o zagrożeniu pożarowym są wydawane na godziny południowe. W przypadku,
    gdy bieżąca data i czas na komputerze jest z zakresu 1 października -- 31
    marca zwraca None, gdyż w tym okresie zagrożenie pożarowe lasów nie jest
    prognozowane."""

    _url=re.compile('mapa\.php\?rok=(\d{4})&mies=(\d{1,2})&'+\
            'dzien=(\d{1,2})&godz=(\d)&mapa=(\d)&ver=(\d)')

    url = "http://bazapozarow.ibles.pl/zagrozenie/mapa.php?"\
            +"rok=%s&mies=%s&dzien=%s&godz=%s&mapa=0&ver=0"

    # debug trick: odkomentuj poniższą linię aby funkcja zwróciła adres do mapki
    # na której "sporo się dzieje ;)
    #return url%('2011','6','7','1')
    # koniec tricka

    now = datetime.datetime.now()
    year, month, day, hour = now.year, now.month, now.day, now.hour

    if month not in range(4,10):
        return None
    else:
        webfile = downloadFile('http://bazapozarow.ibles.pl/zagrozenie/')
        return url%( _url.findall(webfile)[0][0:-2] ) # dlaczego [0:-2]?!?

def getData(l):
    global lang
    lang = my_import(l+"."+l)
    data = {"data":"", "needCTCSS":False, "debug":None, 
            "source":"ibles", "allOK":True}

    url = get_forecast_url()
    if url is None:
        return data

    mapa=downloadFile(url)
    f=open('ibles.png','wb')
    f.write(mapa)
    f.close()
    s= pygame.image.load('ibles.png')

    zagrozenie = 0

    for strefa in config.strefy:
        polozenie = strefy[strefa]
        kolor = tuple(s.get_at(polozenie))
        zagrozenie=max(zagrozenie, poziomy[kolor])

    if zagrozenie>0:
        print zagrozenie
        data['data']=' '.join( ('w_lasach_wystepuje ',
                poziomy_nazwy[zagrozenie],
                'zagrozenie_pozarowe',))

    return data

if __name__=='__main__':
    getData('pl_google')
