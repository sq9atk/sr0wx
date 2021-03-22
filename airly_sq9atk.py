#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import urllib2
import logging
from datetime import datetime
import json as JSON
import socket

from sr0wx_module import SR0WXModule

class AirlySq9atk(SR0WXModule):
    """Klasa pobierająca dane o zanieszczyszczeniach"""

    def __init__(self, language, api_key, lat, lon, service_url, mode, maxDistanceKM, installationId):
        self.__language = language
        self.__api_key = api_key
        self.__lat = str(lat)
        self.__lon = str(lon)
        self.__service_url = service_url
        self.__mode = mode
        self.__maxDistanceKM = str(maxDistanceKM)
        self.__installationId = str(installationId)
        self.__logger = logging.getLogger(__name__)
        self.__levels = {
            'VERY_LOW': 'bardzo_dobry',
            'LOW':      'dobry',
            'MEDIUM':   'umiarkowany',
            'HIGH':     'zly', 
            'VERY_HIGH':'bardzo_zly',
        }


    def get_data(self):
        self.__logger.info("::: Pobieram dane o zanieczyszczeniach...")
        
        api_service_url = self.prepareApiServiceUrl()
        self.__logger.info( api_service_url )
        
        jsonData = JSON.loads(self.getAirlyData(api_service_url))

        self.__logger.info("::: Przetwarzam dane...\n")
        
        message = "".join([
                        " _ ",
                        " informacja_o_skaz_eniu_powietrza ",
                        " _ ",
                        " godzina ",
                        self.getHour(),
                        " _ stan_ogolny ",
                        self.__levels[jsonData['current']['indexes'][0]['level']],
                        self.getPollutionLevel(jsonData['current']['values']),
                        " _ ",
                     ])
        return {
            "message": message,
            "source": "airly",
        }


    def getPollutionLevel(self, json):
        message = '';
        for item in json:
            if item['name'] == 'PM1':
                message += ' _ pyl__zawieszony_pm1 '
                message += self.__language.read_micrograms( int(item['value']) ) + ' '
                
            if item['name'] == 'PM25':
                message += ' _ pyl__zawieszony_pm25 '
                message += self.__language.read_micrograms( int(item['value']) ) + ' '
                
            if item['name'] == 'PM10':
                message += ' _ pyl__zawieszony_pm10 '
                message += self.__language.read_micrograms( int(item['value']) ) + ' '
        return message;
        
        
    def prepareApiServiceUrl(self):
        api_url = 'https://airapi.airly.eu/v2/measurements/'
        urls = {
            'installationId': api_url + 'measurements/installation?installationId=' + self.__installationId,
            'point':          api_url + 'measurements/point?lat=' + self.__lat + '&lng=' + self.__lon,
            'nearest':        api_url + 'nearest?lat=' + self.__lat + '&lng=' + self.__lon + '&maxDistanceKM=' + self.__maxDistanceKM,
        };
        return urls[self.__mode]
        
        
    def getAirlyData(self, url):
        request = urllib2.Request(url, headers={'Accept': 'application/json', 'apikey': self.__api_key})
        try:
            webFile = urllib2.urlopen(request, None, 30)
            return webFile.read()
        except urllib2.URLError, e:
            print e
        except socket.timeout:
            print "Timed out!"
        return ""


    def getHour(self):
        time =  ":".join([str(datetime.now().hour), str(datetime.now().minute)])
        datetime_object = datetime.strptime(time, '%H:%M')
        msg = self.__language.read_datetime(datetime_object, '%H %M')
        return msg


    def getVisibility(self, value):
        msg = ' _ ';
        msg += ' widocznosc ' + self.__language.read_distance( int(value/1000) )
        return msg


