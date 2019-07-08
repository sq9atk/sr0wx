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

import re
import urllib
from config import prospect_mp as config
import datetime
import debug
import json
import os 
lang=None


def bezpiecznaNazwa(s):
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

def downloadFile(url):
    webFile = urllib.urlopen(url)
    return webFile.read()

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

_przekroczenie = re.compile('(Delta)(?:(?:.{1,}?)Przekroczony\ stan\ (ostrzegawczy|alarmowy))?')

def pobierzOstrzezenia(domena,stacja):
    global przekroczenie,debug
    domena,stacja = (domena.lower(), stacja.upper())
    # testowe -- nie używać na produkcji! nie siać zamętu!
    #url = "http://www.biala.prospect.pl/wizualizacja/punkt_pomiarowy.php?"+\
    #      "prze=TUBI&rok=2010&miesiac=06&dzien=04&godzina=19&minuta=-3"
    #url = "http://www.biala.prospect.pl/wizualizacja/punkt_pomiarowy.php?"+\
    #      "prze=TUBI&rok=2010&miesiac=06&dzien=03&godzina=23&minuta=27"


    try:
       url = "http://www.%s.prospect.pl/wizualizacja/punkt_pomiarowy.php?prze=%s"%(domena,stacja)
       plik = downloadFile(url)
       wynik = _przekroczenie.findall(plik)
       if wynik[0]==('Delta', ''):
           return None
       elif wynik[0][1] in ('ostrzegawczy','alarmowy'):
           return wynik[0][1]
       else:
           debug.log('PROSPECT-MP', u'Regex nie zwrócił oczekiwanych danych',\
                   buglevel=5)
           return None
    except:
        debug.log('PROSPECT-MP', u'Regex nie zwrócił oczekiwanych danych',\
                buglevel=5)
        pass
        return None


def getData(l):
    data = {"data":"", "needCTCSS":False, "allOK":True, 
            "source":"rwd_prospect"}
    
    if not os.path.exists('prospect_mp.json'):
        stany = generuj_json(nie_zapisuj=True)
    else:
        stany = json.loads(unicode(open('prospect_mp.json','r').read(),'utf-8'))
        
    if stany['ostrzegawczy']!={} or stany['alarmowy']!={}:
        data['data'] += 'lokalny_komunikat_hydrologiczny '

        if stany['alarmowy']:
            # Sprawdzenie dla których wodowskazów mamy przekroczone 
            # stany alarmowe -- włącz ctcss
            data['needCTCSS']=True
            data['data']+=' przekroczenia_stanow_alarmowych '
            for rzeka in sorted(stany['alarmowy'].keys()):
                data['data']+='rzeka %s wodowskaz %s '%(bezpiecznaNazwa(rzeka), \
                    " wodowskaz ".join(bezpiecznaNazwa(r) for r in sorted(stany['alarmowy'][rzeka])),)

        if stany['ostrzegawczy']:
            data['data']+='_ przekroczenia_stanow_ostrzegawczych '
            for rzeka in sorted(stany['ostrzegawczy'].keys()):
                data['data']+='rzeka %s wodowskaz %s '%(bezpiecznaNazwa(rzeka), \
                    " wodowskaz ".join(bezpiecznaNazwa(r) for r in sorted(stany['ostrzegawczy'][rzeka])),)

    if os.path.exists('prospect_mp.json'):
        os.remove('prospect_mp.json')

    debug.log("PODEST_MP", "finished...")
    return data

def show_help():
    print u"""
Uruchamiając ten skrypt z linii komend możesz wygenerować w łatwy sposób 
fragment słownika sr0wx dla rzek i wodowskazów wskazanych w pliku config.py

Należy uruchomić prospect_mp podając jako parametr gen, np.

python prospect_mp.py gen > pl_google/prospect_mp_dict.py

a następnie

python google_tts_downloader.py prospect_mp_dict.py

aby dociągnąć niezbędne pliki."""

def generuj_slownik():
    # generowanie listy słów słownika; ostatnie słowo (rozielone spacją)
    # jest nazwą pliku docelowego

    print """#!/usr/bin/python
# -*- coding: utf-8 -*-

# Caution! I am not responsible for using these samples. Use at your own risk
# Google, Inc. is the copyright holder of samples downloaded with this tool.

# Generated automatically by prospect_mp.py. Feel free to modify it SLIGHTLY.

LANGUAGE = 'pl'

START_MARKER = 'ę. '
END_MARKER = ' k'

CUT_START = 0.9
CUT_END=0.7

download_list = [ """

    frazy = []
    for wpis in config.wodowskazy:
        frazy.append(wpis[1])
        frazy.append(wpis[2])

    for fraza in set(frazy):
        print "\t['ę. %s', '%s'],"%(fraza, str(bezpiecznaNazwa(fraza)),)


    print """['lokalny komunikat hydrologiczny]', 
        ['przekroczenia stanów ostrzegawczych'],
        ['przekroczenia stanów alarmowych'], ['rzeka'], ['wodowskaz'],
        ['err wu de prospekt','rwd_prospect']
        ]"""


def generuj_json(nie_zapisuj=False):
    """Generuje plik prospect_mp.json oraz zwraca jego zawartość. Plik te
    zawiera informacje o przekroczeniach stanów ostrzegawczych i/lub
    alarmowych"""

    #json_file = open('prospect_mp.json','w')
        

    stany = {'ostrzegawczy':{}, 'alarmowy':{}}

    for w in config.wodowskazy:
        try:
            domena, rzeka, wodowskaz, stacja = w
            debug.log('PROSPECT-MP', ', '.join((domena,stacja,)))
            stan = pobierzOstrzezenia(domena,stacja)

            # Chłyt debugowy sprawdzający, czy mamy wszystkie sample: wszystkie 
            # rzeki przełączamy na stan ostrzegawczy -- nie zapomnij wyłączyć!
            #stan='alarmowy'
            # Koniec chłytu

            if stan in ('ostrzegawczy','alarmowy'):
                if not stany[stan].has_key(rzeka):
                    stany[stan][rzeka]=[]
                stany[stan][rzeka].append(wodowskaz)
        except:
            raise
            debug.log('PROSPECT-MP', u'Pobieranie danych zakończyło się '+\
                   u'błędem', buglevel=5)
            pass

    if nie_zapisuj==False:
        json.dump(stany, open('prospect_mp.json','w'))
    return  stany

if __name__ == '__main__':
    from config import prospect_mp as config
    class DummyDebug:
        def log(self,module,message,buglevel=None):
            pass

    debug = DummyDebug()
    import sys
    # tak, wiem, że można to zrobić bardziej elegancko (getopt), ale dla 2
    # opcji nie ma chyba sensu...
    if len(sys.argv)==2 and sys.argv[1]=='gen':
        generuj_slownik()
    elif len(sys.argv)==2 and sys.argv[1]=='json':
        generuj_json()
    else:
        show_help()
