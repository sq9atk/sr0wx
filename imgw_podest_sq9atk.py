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

# Python 2.7 (wymagane >= 2.7.9 ze wzgledu na HTTPS/SNI w urllib2)

import urllib2
import json
import logging
import os
import time

from sr0wx_module import SR0WXModule

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://hydro.imgw.pl/',
}
STATUS_URL = 'https://hydro-back.imgw.pl/station/hydro/status?id=%s'
CACHE_DIR = 'imgwpodest_data'
CACHE_TTL = 3600
TRENDY = {'up': 1, 'down': -1, 'const': 0, 'unknown': 0, 1: 1, -1: -1, 0: 0}


class ImgwPodestSq9atk(SR0WXModule):
    """Klasa przetwarza dane informujące o przekroczeniach stanów rzek w regionie."""

    def __init__(self, wodowskazy):
        self.__wodowskazy = wodowskazy
        self.__logger = logging.getLogger(__name__)
        self._dane = {}

    def _pobierzStatus(s, id_):
        """Status wodowskazu z cache'em plikowym (1h)."""
        path = os.path.join(CACHE_DIR, '%s.json' % id_)

        if os.path.exists(path) and time.time() - os.path.getmtime(path) <= CACHE_TTL:
            try:
                with open(path) as f:
                    return json.load(f)
            except ValueError:
                pass  # uszkodzony cache, pobierz ponownie

        req = urllib2.Request(STATUS_URL % id_, headers=HEADERS)
        raw = urllib2.urlopen(req, timeout=20).read()
        data = json.loads(raw)  # rzuci ValueError, zanim cokolwiek trafi na dysk

        tmp = path + '.tmp'
        with open(tmp, 'w') as f:
            f.write(raw)
        os.rename(tmp, path)  # zapis atomowy
        return data

    def zaladujWybraneWodowskazy(s):
        s.__logger.info("::: Pobieram dane o wodowskazach...")
        s._dane = {}

        if not os.path.isdir(CACHE_DIR):
            os.makedirs(CACHE_DIR)

        for wodowskaz in s.__wodowskazy:
            id_ = wodowskaz.split('.')[-1]
            try:
                sub = s._pobierzStatus(id_)
                st = sub.get('status')
                if 'exception' in sub or not st:
                    continue

                current = st.get('currentState')
                s._dane[id_] = {
                    'id': id_,
                    'nazwa': st['description'],
                    'rzeka': st['river'].split(' (')[0],
                    'region': st.get('province'),
                    'tendencja': TRENDY.get(st.get('trend'), 0),
                    'stan_cm': current['value'] if current else None,
                    'poziom_ostrzegawczy': st.get('warningValue'),
                    'poziom_alarmowy': st.get('alarmValue'),
                }
            except Exception:
                s.__logger.info("Nie udało się pobrać wodowskazu %s!" % id_)

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
        if '.' in wodowskaz:
            wodowskaz = wodowskaz.split('.')[1]

        dane = s._dane[wodowskaz]

        if dane['stan_cm'] is None:
            raise ValueError('brak stanu')

        if dane['poziom_alarmowy'] is not None and dane['stan_cm'] > dane['poziom_alarmowy']:
            stan = "alarmowy"
        elif dane['poziom_ostrzegawczy'] is not None and dane['stan_cm'] > dane['poziom_ostrzegawczy']:
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
            'tendencja': tendencja }

    def get_data(s):

        stanyOstrzegawcze = {}
        stanyAlarmowe = {}

        s.zaladujWybraneWodowskazy()

        for wodowskaz in s.__wodowskazy:
            try:
                w = s.pobierzDaneWodowskazu(wodowskaz)
                rzeka = w['rzeka']
                w['rzeka'] = s.bezpiecznaNazwa(w['rzeka'])
                w['nazwa'] = s.bezpiecznaNazwa(w['nazwa'])

                if w['przekroczenieStanu'] == 'ostrzegawczy':
                    s.__logger.info("::: Stan ostrzegawczy: " + wodowskaz + " - " + rzeka + ' - ' + w['nazwa_org'])
                    stanyOstrzegawcze.setdefault(w['rzeka'], []).append(w['nazwa'] + ' ' + w['tendencja'] + ' _ ')

                elif w['przekroczenieStanu'] == 'alarmowy':
                    s.__logger.info("::: Stan alarmowy: " + wodowskaz + " - " + rzeka + ' - ' + w['nazwa_org'])
                    stanyAlarmowe.setdefault(w['rzeka'], []).append(w['nazwa'] + ' ' + w['tendencja'] + ' _ ')

            except Exception:
                s.__logger.info("::: Brak danych!!! " + wodowskaz)

        if stanyOstrzegawcze != {} or stanyAlarmowe != {}:
            message = ' _ komunikat_hydrologiczny_imgw _ '

            if stanyAlarmowe != {}:
                message += ' przekroczenia_stanow_alarmowych '
                for rzeka in sorted(stanyAlarmowe.keys()):
                    message += ' rzeka %s wodowskaz %s ' % (rzeka, " wodowskaz ".join(sorted(stanyAlarmowe[rzeka])),)

            if stanyOstrzegawcze != {}:
                message += '_ przekroczenia_stanow_ostrzegawczych '
                for rzeka in sorted(stanyOstrzegawcze.keys()):
                    message += 'rzeka %s wodowskaz %s ' % (format(rzeka), " wodowskaz ".join([format(w) for w in sorted(stanyOstrzegawcze[rzeka])]),)
            message += ' '
        else:
            message = ' '

        s.__logger.info("::: Przekazuję przetworzone dane...\n")

        return {
            "message": message,
            "source": "imgw",
        }

