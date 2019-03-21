#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import urllib2
import re
import logging
import pytz

from datetime import datetime
from sr0wx_module import SR0WXModule

class CalendarSq9atk(SR0WXModule):
    """Klasa pobierająca dane kalendarzowe"""

    def __init__(self,language,service_url,city_id=3094802):
        self.__service_url = service_url
        self.__city_id = city_id
        self.__language = language
        self.__logger = logging.getLogger(__name__)


    def downloadFile(self, url):
        webFile = urllib2.urlopen(url)
        return webFile.read()

    def getSunsetSunrise(self):
        self.__logger.info("::: Pobieram dane o wschodzie i zachodzie słońca")
        r = re.compile(r'<h1>(.*)(\d\d:\d\d)(.*)(\d\d:\d\d)</h1>')
        url = self.__service_url+str(self.__city_id)
        html = self.downloadFile(url)
        matches = r.findall(html)
        return {
            'sunrise' : matches[0][1],
            'sunset' : matches[0][3],
        }

    def hourToNumbers(self, time="00:00"):
        datetime_object = datetime.strptime(time, '%H:%M')
        time_words = self.__language.read_datetime(datetime_object, '%H %M')
        return time_words

    def get_data(self):
        times = self.getSunsetSunrise()
        self.__logger.info("::: Przetwarzam dane...\n")

        sunrise = " ".join(["wscho_d_sl_on_ca","godzina",self.hourToNumbers(times['sunrise'])," "])
        sunset = " ".join(["zacho_d_sl_on_ca","godzina",self.hourToNumbers(times['sunset'])," "])

        message = " ".join([" _ kalendarium _ " ,sunrise ," _ " ,sunset ," _ "])
        return {
            "message": message,
            "source": "calendar_zoznam_sk",
        }







