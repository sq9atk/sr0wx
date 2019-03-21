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

import urllib2
import re
import json
import logging
import base64
import subprocess

from sr0wx_module import SR0WXModule

class ImgwPodestSq9atk(SR0WXModule):
    """Klasa przetwarza dane informujące o przekroczeniach stanów rzek w regionie."""

    def __init__(self, wodowskazy):
        self.__wodowskazy = wodowskazy
        self.__logger = logging.getLogger(__name__)

    def zaladujWybraneWodowskazy(s):
        global wodowskazy
        s.__logger.info("::: Pobieram dane o wodowskazach...")
        try:        
            jsonData = json.dumps(s.__wodowskazy, separators=(',', ':'))
            b64data = base64.urlsafe_b64encode(jsonData)
            proc = subprocess.Popen("php imgw_podest_sq9atk.php "+b64data, shell=True, stdout=subprocess.PIPE)
        
            dane = proc.stdout.read()
            s.__logger.info("::: Przetwarzam...")
            wodowskazy = json.loads(dane)
            
        except:
            s.__logger.info("Nie udało się pobrać danych o wodowskazach!")

    def bezpiecznaNazwa(s, nazwa):
        return unicode(nazwa, 'utf-8').lower().\
            replace(u'ą',u'a_').replace(u'ć',u'c_').\
            replace(u'ę',u'e_').replace(u'ł',u'l_').\
            replace(u'ń',u'n_').replace(u'ó',u'o_').\
            replace(u'ś',u's_').replace(u'ź',u'z_').\
            replace(u'ż',u'z_').replace(u' ',u'_').\
            replace(u'-',u'_').replace(u'(',u'').\
            replace(u')',u'')    
        
    def pobierzDaneWodowskazu(s, wodowskaz):
        global wodowskazy

        if '.' in wodowskaz:
            wodowskaz = wodowskaz.split('.')[1]

        dane = wodowskazy[wodowskaz]
        
        # omijanie zrypanych wodowskazów
        #elif dane['poziom_alarmowy'] == None:
        #   stan = ""
        #elif dane['poziom_ostrzegawczy'] == None:
        #   stan = ""     
        
        if dane['stan_cm'] > dane['poziom_alarmowy']:
            stan = "alarmowy"
        elif dane['stan_cm'] > dane['poziom_ostrzegawczy']:
            stan = "ostrzegawczy"
        else:
            stan = ""
        
        
        if dane['tendencja'] == 1:
            tendencja = "tendencja_wzrostowa"
        elif dane['tendencja'] == -1:
            tendencja = "tendencja_spadkowa"
        else:
            tendencja = ""

        return {'numer': wodowskaz,
            'nazwa': dane['nazwa'].strip().encode("utf-8"),
            'nazwa_org': dane['nazwa'].lower().encode("utf-8"),
            'rzeka': dane['rzeka'].strip().encode("utf-8"),
            'stan': dane['stan_cm'],
            'przekroczenieStanu': stan,
           # 'przekroczenieStanuStan': stan,
            'tendencja': tendencja }    
        
        
        
    def get_data(s):

        stanyOstrzegawcze = {}
        stanyAlarmowe = {}

        zaladowaneRegiony = []
        s.zaladujWybraneWodowskazy()
        
        for wodowskaz in s.__wodowskazy:
            region = wodowskaz.split('.')[0]
            
            if region not in zaladowaneRegiony:
                zaladowaneRegiony.append(region)
                #w = s.pobierzDaneWodowskazu(wodowskaz)
            try:
                w = s.pobierzDaneWodowskazu(wodowskaz)
                rzeka = w['rzeka']
                w['rzeka'] = s.bezpiecznaNazwa(w['rzeka'])
                w['nazwa'] = s.bezpiecznaNazwa(w['nazwa'])

                if w['przekroczenieStanu'] == 'ostrzegawczy':
                    s.__logger.info("::: Stan ostrzegawczy: " + wodowskaz + " - " + rzeka + ' - ' + w['nazwa_org'])
                    if not stanyOstrzegawcze.has_key(w['rzeka']):
                        stanyOstrzegawcze[w['rzeka']] = [w['nazwa']+ ' ' + w['tendencja'] + ' _ ']
                        
                    else:
                        stanyOstrzegawcze[w['rzeka']].append(w['nazwa']+ ' ' + w['tendencja'] + ' _ ')
                        
                elif w['przekroczenieStanu'] == 'alarmowy':
                    s.__logger.info("::: Stan alarmowy: "+ wodowskaz+" - " + rzeka + ' - ' + w['nazwa_org'])
                    if not stanyAlarmowe.has_key(w['rzeka']):
                        stanyAlarmowe[w['rzeka']] = [w['nazwa']+ ' ' + w['tendencja'] + ' _ ']
                        
                    else:
                        stanyAlarmowe[w['rzeka']].append(w['nazwa']+ ' ' + w['tendencja'] + ' _ ')
                        
                else:
                    a=1
                    #s.__logger.info("Przetwarzam wodowskaz:    " + wodowskaz + " - " + rzeka + ' - ' + w['nazwa_org'])
            except:
                s.__logger.info("::: Brak danych!!! "+ wodowskaz+" - " + rzeka + ' - ' + w['nazwa_org'])
                pass

        message = "";
        if stanyOstrzegawcze!={} or stanyAlarmowe!={}:
            message += 'komunikat_hydrologiczny_imgw _ '

            if stanyAlarmowe!={}:
                # Sprawdzenie dla których wodowskazów mamy przekroczone
                # stany alarmowe -- włącz ctcss
             
                message +=' przekroczenia_stanow_alarmowych '
                for rzeka in sorted(stanyAlarmowe.keys()):
                    message +=' rzeka %s wodowskaz %s '%(rzeka, \
                        " wodowskaz ".join(sorted(stanyAlarmowe[rzeka])),)

            if stanyOstrzegawcze!={}:
                message += '_ przekroczenia_stanow_ostrzegawczych '
                for rzeka in sorted(stanyOstrzegawcze.keys()):
                    message += 'rzeka %s wodowskaz %s '%(format(rzeka), \
                        " wodowskaz ".join([format(w) for w in sorted(stanyOstrzegawcze[rzeka])]),)

        s.__logger.info("::: Przekazuję przetworzone dane...\n")

        message += ' _ '

        return {
            "message": message,
            "source": "imgw",
        }
