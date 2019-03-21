#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import urllib2
import re
import logging
import pytz
from datetime import datetime

from bs4 import BeautifulSoup
import unicodedata

from sr0wx_module import SR0WXModule

class MeteoSq9atk(SR0WXModule):
    """Klasa pobierająca dane kalendarzowe"""
        
    def __init__(self,language,service_url):
        self.__service_url = service_url
        self.__language = language
        self.__logger = logging.getLogger(__name__)

    def downloadFile(self, url):
        webFile = urllib2.urlopen(url) 
        return webFile.read()

    def getHour(self):
        time =  ":".join([str(datetime.now().hour), str(datetime.now().minute)])
        datetime_object = datetime.strptime(time, '%H:%M')
        time_words = self.__language.read_datetime(datetime_object, '%H %M')
        return time_words

    def parseForecastDesc(self, html):
        match = html.find_all("div", {"class":"forecastDesc"})[0].text
        return self.__language.rmv_pl_chars( match.strip().replace(" ", "_").replace(",","_") )
    
    def parseTemperature(self, html):
        match = html.find_all("li")[0].find_all("span")[1]               
        tempText = re.sub("[^(\-){0,1}(\s){0,1}0-9]", "", match.text)
        temp = self.__language.read_temperature(int(tempText))
        return temp 
   
    def parseClouds(self, html):
        match = html.find_all("li")[2].find_all("span")[1]
        tempText = re.sub("[^0-9]", "", match.text)
        temp = self.__language.read_percent(int(tempText))
        return temp 

    def parseWind(self, html):
        match = html.find_all("li")[3].find_all("span")[1]
        tempText = re.sub("[^0-9]", "", match.text)
        temp = self.__language.read_speed(int(tempText),"kmph")
        return temp 
    
    def parsePressure(self, html):
        match = html.find_all("li")[5].find_all("span")[1]
        tempText = re.sub("[^0-9]", "", match.text)
        temp = self.__language.read_pressure(int(tempText))
        return temp 
    
    def parseHumidity(self, html):
        match = html.find_all("li")[6].find_all("span")[1]
        tempText = re.sub("[^0-9]", "", match.text)
        temp = self.__language.read_percent(int(tempText))
        return temp 
    
    
    
    def get_data(self):
        self.__logger.info("::: Przetwarzam dane...\n")
        
        rawHtml = self.downloadFile(self.__service_url)
        soup = BeautifulSoup(rawHtml ,"lxml")
        
        now = soup.find_all("li", { "id" : "wts_p0" })[0]
        after = soup.find_all("li", { "id" : "wts_p3" })[0]
        forecast = soup.find_all("li", { "id" : "wts_p13" })[0]
            

        message = " ".join([ \
                        "stan_pogody_z_godziny", self.getHour(), \
                        
                        " _ ", self.parseForecastDesc(now), \
                        "temperatura", self.parseTemperature(now), \
                        "pokrywa_chmur", self.parseClouds(now), \
                        "predkosc_wiatru", self.parseWind(now), \
                        "cisnienie", self.parsePressure(now), \
                        "wilgotnosc", self.parseHumidity(now), \
                        
                        " _ ", "prognoza_na_nastepne","cztery", "godziny", \
                        " _ ", self.parseForecastDesc(after), \
                        "temperatura", self.parseTemperature(after), \
                        "pokrywa_chmur", self.parseClouds(after), \
                        "predkosc_wiatru", self.parseWind(after), \
                        "cisnienie", self.parsePressure(after), \
                        "wilgotnosc", self.parseHumidity(after), \
                        
                        " _ ", "prognoza_na_nastepne","dwanascie", "godzin", \
                        " _ ", self.parseForecastDesc(forecast), \
                        "temperatura", self.parseTemperature(forecast), \
                        "pokrywa_chmur", self.parseClouds(forecast), \
                        "predkosc_wiatru", self.parseWind(forecast), \
                        "cisnienie", self.parsePressure(forecast), \
                        "wilgotnosc", self.parseHumidity(forecast), \
                     ])

        return {
            "message": message,
            "source": "",
        }







