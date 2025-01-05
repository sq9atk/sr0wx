#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import re
import logging
import socket
import requests

from pprint import pprint

from sr0wx_module import SR0WXModule

class MeteoalarmSq9atk(SR0WXModule):
    """Klasa pobierająca informacje z meteoalarm.pl"""

    def __init__(self, language, service_url, region_id):
        self.__service_url = service_url
        self.__language = language
        self.__region_id = region_id
        self.__logger = logging.getLogger(__name__)

        self.__levels = { '1' : 'niski', '2' : 'sredni', '3' : 'wysoki' }
        self.__regions = {
            '14':'mazowieckiego',        '08':'lubuskiego',            '32':'zachodniopomorskiego',
            '22':'pomorskiego',          '02':'dolnoslaskiego',        '16':'opolskiego',
            '24':'slaskiego',            '12':'malopolskiego',         '18':'podkarpackiego',
            '26':'swietokrzyskiego',     '10':'lodzkiego',             '30':'wielkopolskiego',
            '04':'kujawsko-pomorskiego', '28':'warmińsko-mazurskiego', '06':'lubelskiego',
            '20':'podlaskiego',
        }
        self.__warnings = {
            'o01': 'burze',                 'o02': 'deszcz_i_grad',         'o03': 'mgla',
            'o06': 'ulewny_deszcz',         'o08': 'zamiec_sniezna',        'o04': 'marznaca_mgla',
            'o11': 'snieg_lub_oblodzenie',  'o07': 'marznacy_deszcz',       'o08': 'sniezyca',
            'o09': 'przymrozki',            'o10': 'roztopy',               'o05': 'niskie_temperatury',
            'o13': 'silny_wiatr',           'o12': 'wysokie_temperatury',   'o14': 'zawieje_sniezne'
        }

    def getHtmlFromUrl(self, url):
        try:
            self.__logger.info("::: Odpytuję adres: " + url)
            resp = requests.get(url, timeout=8)
            if resp.status_code != 200:
                self.__logger.error("::: Data response code error - %s \n" % resp.status_code)
                return ''

            return resp.content

        except requests.exceptions.RequestException as e:
            self.__logger.error("::: Data download error - %s \n" % e)
            return ''


    def findDataInHtml(self, html):
        self.__logger.info("::: Przetwarzam dane...\n")
        patternTable = re.compile(r'<table[^>]*class="[^>]*meteo_table[^>]*"[^>]*>.*?</table>', re.DOTALL)
        matchTable = patternTable.search(html)

        if matchTable:
            tableHtml = matchTable.group(0)

            levelMatch = re.search(r'<b>(\d+)</b>', tableHtml, re.DOTALL)
            level = levelMatch.group(1) if levelMatch else None

            imgMatch = re.search(r'<div class="zagrozenia-ikony">(.*?)</div>', tableHtml, re.DOTALL)
            images = re.findall(r'<img.*?src="images/(.*?).png"', imgMatch.group(1)) if imgMatch else []

            # deduplicate values
            images = list(set(images)) 
            
            # Wypisujemy nazwy plików zamiast atrybutów alt
            return [level, images]
        else:
            return []


    def get_data(self):
        self.__logger.info("::: Pobieram dane o zagrożeniach...")
        html = self.getHtmlFromUrl(self.__service_url + str(self.__region_id))

        data = self.findDataInHtml(html)
        message = ''

        try:
            level = data[0]
            warnings = data[1]
            message += " ".join([
                ' _ zagrozenia_meteorologiczne_dla_wojewodztwa ',
                self.__regions[self.__region_id],
                ' _ ',
                ' '.join(self.__warnings[key] for key in warnings),
                ' _ poziom_zagrozenia ',
                ' '.join([self.__levels[level]]),
                ' _ '
            ])
        except:
            None

        return {
            "message": message,
            "source": "meteoalarm_pl",
        }
