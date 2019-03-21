#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

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


# TODO: sprawdzanie, dla których wodowskazów możemy czytać komunikaty 

import os
import urllib
import re

def format(s):
    """Zwraca "bezpieczną" nazwę dla nazwy danej rzeki/danego
    wodowskazu. Ze względu na to, że w Polsce zarówno płynie
    rzeka Ślęza jak i Ślęża oznaczany jest każdy niełaciński
    znak"""
    if str(s.__class__)=="<type 'str'>":
        s=unicode(s, 'utf-8')
    return s.lower().replace(u'ą',u'a_').replace(u'ć',u'c_').\
        replace(u'ę',u'e_').replace(u'ł',u'l_').\
        replace(u'ń',u'n_').replace(u'ó',u'o_').\
        replace(u'ś',u's_').replace(u'ź',u'x_').\
        replace(u'ż',u'z_').replace(u' ',u'_').\
        replace(u'-',u'_').replace(u'(',u'').\
        replace(u')',u'')


wodowskazy={}

_wodowskaz=re.compile('Stacja\:\ (.{1,}?)\<')
_rzeka=re.compile(u"""Rzeka\:\ (.{1,}?)\<|(Jezioro\ .{1,}?)\<|(Zalew\ .{1,}?)|(Morze\ Ba..tyckie)""", re.MULTILINE)
_stan=re.compile('Stan\ Wody\ H\ \[cm\]\:\ (.{1,}?)\<')
_nnw=re.compile('NNW\:(\d{1,})')
_ssw=re.compile('SSW\:(\d{1,})')
_www=re.compile('WWW\:(\d{1,})')
_przeplyw=re.compile('Przepływ\ Q\ \[m3/s\]:\ (.{1,}?)\<')
_czas=re.compile('Czas\(UTC\)\:\ (\d{4}-\d{2}-\d{2}\ \d{2}\:\d{2}\:\d{2})')

_przekroczenieStanu=re.compile('stan\ (ostrzegawczy|alarmowy)')
_przekroczenieStanuStan=re.compile('stan\ (?:ostrzegawczy|alarmowy)\</b\>\ \((\d{1,})cm\)')

def getFile(url):
    webFile = urllib.urlopen(url)
    contents = webFile.read()
    webFile.close()
    return contents

def flatten(x): # przerobić na lambda?
    """flatten(table) -> table[0] or None"""
    if x==[]:
        return None
    else:
        return x[0]

def zaladujRegion(region):
    """Funckcja służy do pobierania listy dostępnych wodowskazów ze strony IMGW
    dla danego regionu.


    Korzystamy tutaj z faktu, że 1. Hash tables w JS mają składnię identyczną do pythonowych
    słowników; 2. W pliku są 2 słowniki a nas interesuje tylko pierwszy; 3. Python potrafi 
    interpretować sam siebie :)

    2011-08-30: trzeba to jak najszybciej przerobić na JSON, eval is evil!"""

    global wodowskazy

    try:
        debug.log("IMGW-HYDRO", 'Pobieram dane dla regionu %s'%region)
        dane = getFile('http://www.pogodynka.pl/http/assets/products/podest/podest/hydro/mapy/dane%s.js'%str(region))
        debug.log("IMGW-HYDRO", 'Przetwarzam...')
        # NOTE: teraz trochę zabawnych rzeczy: następna linijka zadziała poprawnie tylko wtedy,
        # kiedy w następnej będzie coś w rodzaju "print"
        # wodowskazy.update(eval('{'+dane.split('{')[1].split('}')[0]+'}'))
        # print wodowskazy
        # próbujemy inaczej:
        wodowskazy = dict(eval('{'+dane.split('{')[1].split('}')[0]+'}'), **wodowskazy)
    except:
        debug.log("IMGW-HYDRO", 'Nie udało się pobrać danych o wodowskazach dla regionu %s'%region, buglevel=6)
        pass
    
def pobierzDaneWodowskazu(wodowskaz):
    global wodowskazy
    if '.' in wodowskaz:
        wodowskaz = wodowskaz.split('.')[1] # pozbywamy się numeru regionu
    dane = wodowskazy[wodowskaz] # po co cały czas mieszać słownikiem

    #print dane
    #print _rzeka.findall(dane)
    
    return {'numer':wodowskaz,
        'nazwa':flatten(_wodowskaz.findall(dane)),
        'rzeka': (' '.join(flatten(_rzeka.findall(dane)))).split('->')[0],
        'stan':flatten(_stan.findall(dane)),
        'nnw':flatten(_nnw.findall(dane)),
        'ssw':flatten(_ssw.findall(dane)),
        'www':flatten(_www.findall(dane)),
        'przeplyw':flatten(_przeplyw.findall(dane)),
        'czas':flatten(_czas.findall(dane)),
        'przekroczenieStanu':flatten(_przekroczenieStanu.findall(dane)),
        'przekroczenieStanuStan':flatten(_przekroczenieStanuStan.findall(dane)),}

def getData(l):
    data = {"data":"", "needCTCSS":False, "allOK":True, "source":"imgw"} 

    stanyOstrzegawcze = {}
    stanyAlarmowe = {}

    # Sprawdzenie w config jakie regiony będziemy spawdzać. Wodowskazy zapisane
    # są jako region.wodowskaz, np. rzeka Bystrzyca wodowskaz Jarnołtów będzie
    # zapisany jako 3.151160190. Ładujemy regiony

    zaladowaneRegiony = []
    for wodowskaz in config.wodowskazy:
        region = wodowskaz.split('.')[0]
        if region not in zaladowaneRegiony:
            zaladujRegion(region)
            zaladowaneRegiony.append(region)
	try:
            w = pobierzDaneWodowskazu(wodowskaz)
            
            # Chłyt debugowy sprawdzjący, czy mamy wszytkie sample: wszystkie rzeki
            # przełączamy na stan ostrzegawczy -- nie zapomnij wyłączyć!
            #w['przekroczenieStanu']='alarmowy'
            # Koniec chłytu

            w['rzeka']=bezpiecznaNazwa(w['rzeka'])
            w['nazwa']=bezpiecznaNazwa(w['nazwa'])

            if w['przekroczenieStanu']=='ostrzegawczy':
                if not stanyOstrzegawcze.has_key(w['rzeka']):
                    stanyOstrzegawcze[w['rzeka']]=[w['nazwa']]
                else:
                    stanyOstrzegawcze[w['rzeka']].append(w['nazwa'])
            elif w['przekroczenieStanu']=='alarmowy':
                if not stanyAlarmowe.has_key(w['rzeka']):
                    stanyAlarmowe[w['rzeka']]=[w['nazwa']]
                else:
                    stanyAlarmowe[w['rzeka']].append(w['nazwa'])
        except:
            debug.log("IMGW-HYDRO", 'Brak danych dla wodowskazu %s'%str(wodowskaz))
            pass

    if stanyOstrzegawcze!={} or stanyAlarmowe!={}:
        data['data'] += 'komunikat_hydrologiczny_imgw _ '

        if stanyAlarmowe!={}:
            # Sprawdzenie dla których wodowskazów mamy przekroczone 
            # stany alarmowe -- włącz ctcss
            data['needCTCSS']=True
            data['data']+=' przekroczenia_stanow_alarmowych '
            for rzeka in sorted(stanyAlarmowe.keys()):
                data['data']+='rzeka %s wodowskaz %s '%(rzeka, \
                    " wodowskaz ".join(sorted(stanyAlarmowe[rzeka])),)

        if stanyOstrzegawcze!={}:
            data['data']+='_ przekroczenia_stanow_ostrzegawczych '
            for rzeka in sorted(stanyOstrzegawcze.keys()):
                data['data']+='rzeka %s wodowskaz %s '%(format(rzeka), \
                    " wodowskaz ".join([format(w) for w in sorted(stanyOstrzegawcze[rzeka])]),)

    debug.log("IMGW-HYDRO", "finished...")

    return data

def show_help():
    print u"""
Lista wodowskazów danej zlewni dostępna po podaniu parametru:

 1. Zlewnia Sanu
 2. Zlewnia Górnej Wisły
 3. Zlewnia Górnej Odry
 4. Zlewnia górej Odry i środkowej Odry
 5. Zlewnia Bugu
 6. Zlewnia Środkowej Wisły
 7. Zlewnia Warty do Poznania
 8. Zlewnia Noteci
 9. Zlewnia Nawii
10. Zlewnia Zalewu Wiślenego
11. Zlewnia Dolnej Wisły do Torunia
12. Zlewnia Dolnej Wisły od Torunia
13. Zlewnia rzek przymorza i Zalewu Gdańskiego
14. Zlewnia dolnej Odry do Kostrzynia i zalewu Szczecińskiego

Mapę zlewni można zobaczyć na stronie:
http://www.pogodynka.pl/polska/podest/"""

def bezpiecznaNazwa(s):
    """Zwraca "bezpieczną" nazwę dla nazwy danej rzeki/danego
    wodowskazu. Ze względu na to, że w Polsce zarówno płynie
    rzeka Ślęza jak i Ślęża oznaczany jest każdy niełaciński
    znak"""
    return unicode(s, 'utf-8').lower().replace(u'ą',u'a_').replace(u'ć',u'c_').\
        replace(u'ę',u'e_').replace(u'ł',u'l_').\
        replace(u'ń',u'n_').replace(u'ó',u'o_').\
        replace(u'ś',u's_').replace(u'ź',u'x_').\
        replace(u'ż',u'z_').replace(u' ',u'_').\
        replace(u'-',u'_').replace(u'(',u'').\
        replace(u')',u'')

def podajListeWodowskazow(region):
    rv = []
    for wodowskaz in wodowskazy.keys():
        try:
            w = pobierzDaneWodowskazu(wodowskaz)
            rv.append(w)
        except:
            debug.log("IMGW-HYDRO", 'Brak danych dla wodowskazu %s'%str(wodowskaz))
            pass
    return rv

if __name__ == '__main__':
    class DummyDebug:
        def log(self,module,message,buglevel=None):
            pass

    debug = DummyDebug()
    import sys
    # tak, wiem, że można to zrobić bardziej elegancko (getopt), ale dla 2
    # opcji nie ma chyba sensu...
    if len(sys.argv)==3 and sys.argv[1]=='gen' and int(sys.argv[2]) in range(1,14+1):
        region = sys.argv[2]
        # generowanie listy słów słownika; ostatnie słowo (rozielone spacją)
        # jest nazwą pliku docelowego
    
        print """#!/usr/bin/python
# -*- coding: utf-8 -*-

# Caution! I am not responsible for using these samples. Use at your own risk
# Google, Inc. is the copyright holder of samples downloaded with this tool.

# Generated automatically by imgw_podest.py. Feel free to modify it SLIGHTLY.

LANGUAGE = 'pl'

START_MARKER = 'ę. '
END_MARKER = ' k'

CUT_START = 0.9
CUT_END=0.7

download_list = [ """
        frazy = [u'komunikat hydrologiczny imgw', 
                u'przekroczenia stanów ostrzegawczych',
                u'przekroczenia stanów alarmowych', u'rzeka', u'wodowskaz']
        for fraza in set(frazy):
            #print fraza.encode('utf-8')
            print "\t['%s', '%s'],"%(fraza.encode('utf-8'),
                    format(fraza).encode('utf-8'),)

        frazy=[]
        zaladujRegion(int(region))
        for w in podajListeWodowskazow(int(region)):
            frazy.append(w['rzeka'])
            frazy.append(w['nazwa'])
        for fraza in set(frazy):
            print "\t['ę. %s', '%s'],"%(fraza, str(bezpiecznaNazwa(fraza)),)
        print ']'
    elif len(sys.argv)==2 and int(sys.argv[1]) in range(1,14+1):
        # podaje listę wodowskazów w danym regionie (danej zlewni)
        region = sys.argv[1]
        zaladujRegion(int(region))
        for w in podajListeWodowskazow(int(region)):
            print "'%s.%s',   # Nazwa: %s, rzeka: %s"%(region, w['numer'], w['nazwa'], w['rzeka'])
    else:
        show_help()
else:
    import debug
    from config import imgw_podest as config
