#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import urllib
import logging
import socket
import subprocess
import re
import urllib2

from pprint import pprint
from sr0wx_module import SR0WXModule

class PropagationSq9atk(SR0WXModule):
    """Klasa pobierająca dane o propagacji"""

    def __init__(self,language,service_url):
        self.__service_url = service_url
        self.__language = language
        self.__logger = logging.getLogger(__name__)
        
        self.__levels = {
            'good': 'warunki_podwyzszone', 
            'fair': 'warunki_normalne', 
            'poor': 'warunki_obnizone', 
            'closed': 'pasmo_zamkniete'
        }

    def downloadDataFromUrl(self, url):
        self.__logger.info("::: Odpytuję adres: " + url)
        opener = urllib2.build_opener()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
        }
        opener.addheaders = headers.items()
        response = opener.open(url)

        return response.read()

    def collectBandConditions (self, html):
        r = re.compile(r'<table.*?>.*?</table>', re.DOTALL)
        tables = r.findall(html)
        # bierzemy drugą tabelkę ze strony bo w niej są dane
        tableHtml = tables[1] 

        r = re.compile(r'<tbody>(.*?)</tbody>', re.DOTALL)
        tbody_content = r.search(tableHtml)
        tbody_html = tbody_content.group(1)

        r_rows = re.compile(r'<tr>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?</tr>', re.DOTALL)
        matches = r_rows.findall(tbody_html)

        bands_data = []
        for match in matches:
            day = match[1].split()[0].split()[0].lower()
            night = match[2].split()[0].split()[0].lower()

            bands_data.append({
                'band': match[0].strip().split()[0],
                'day': self.__levels[ day ],
                'night': self.__levels[ night ]
            })

        return bands_data
        
    def prepareData(self, data, dayTime):
        result = list()
        for row in data:
            if row['band'] == '600': # pasmo 136kHz pomijamy
                continue
            string = row['band'] + '_metrow' + ' ' + row[dayTime]
            result[:0] = [string]
        return result

    def get_data(self):
        html = self.downloadDataFromUrl(self.__service_url)
        
        self.__logger.info("::: Przetwarzam dane...\n")
        
        data = self.collectBandConditions (html)
        day = self.prepareData(data, 'day')
        night = self.prepareData(data, 'night')
        
        message = '';
        if len(day) and len(night):        
            message = " ".join([
                " _ informacje_o_propagacji ",
                " _ dzien _ ",
                " _ pasma _ ",
                " _ " .join( day ),
                " _ noc _ ",
                " _ pasma _ ",
                " _ " .join( night ),
                " _ "
            ])

        return {
            "message": message,
            "source": "noaa",
        }

