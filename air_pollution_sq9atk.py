#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import urllib2
import logging
import json
import socket

from pprint import pprint

# LISTA STACJI Z NUMERAMI
# http://api.gios.gov.pl/pjp-api/rest/station/findAll

from sr0wx_module import SR0WXModule

class AirPollutionSq9atk(SR0WXModule):
    """Klasa pobierająca info o zanieczyszczeniach powietrza"""

    def __init__(self, language, service_url, city_id=1, station_id=3):
        self.__language = language
        self.__service_url = service_url
        self.__station_id = station_id
        self.__logger = logging.getLogger(__name__)

        self.__stations_url = "station/findAll/"
        self.__station_url = "station/sensors/"
        self.__sensor_url = "data/getData/"
        self.__index_url = "aqindex/getIndex/"

    def getJson(self, url):
        self.__logger.info("::: Odpytuję adres: " + url)
        
        try:
            data = urllib2.urlopen(url, None, 45)
            return json.load(data)
        except urllib2.URLError, e:
            print e
        except socket.timeout:
            print "Timed out!"

        return {}

    def getStationName(self):
        url = self.__service_url + self.__stations_url
        stationName = ''
        for station in self.getJson(url):
            if station['id'] == self.__station_id:
                stationName = station['stationName']
        return stationName

    def getSensorValue(self, sensorId):
        url = self.__service_url + self.__sensor_url + str(sensorId)
        data = self.getJson(url)
        return [
            data['key'],
            data['values'][1]['value']
        ]

    def getLevelIndexData(self):
        url = self.__service_url + self.__index_url + str(self.__station_id)
        return self.getJson(url)


    def getSensorsData(self):
        url = self.__service_url + self.__station_url + str(self.__station_id)
        levelIndexArray = self.getLevelIndexData()
        sensors = []
        for row in self.getJson(url):
            value = self.getSensorValue(row['id'])
            if(value[1]>1): # czasem tu schodzi none
                qualityIndexName = self.mbstr2asci(value[0]) + "IndexLevel"
                index = levelIndexArray[qualityIndexName]
                sensors.append([
                    row['id'],
                    qualityIndexName,
                    self.mbstr2asci(row['param']['paramName']),
                    value[1],
                    self.mbstr2asci(index['indexLevelName'])
                ])
        return sensors

    def prepareMessage(self, data):
        levels =  {
            'bardzo_dobry'  :'poziom_bardzo_dobry',
            'dobry'         :'poziom_dobry',
            'dostateczny'   :'poziom_dostateczny',
            'umiarkowany'   :'poziom_umiarkowany',
            'zly'           :'poziom_zl_y', # ten jest chyba nieuzywany
            'zl_y'           :'poziom_zl_y',
            'bardzo_zly'    :'poziom_bardzo_zl_y', # ten też jest chyba nieuzywany
            'bardzo_zl_y'    :'poziom_bardzo_zl_y'
        }
        message = " "
        for row in data:
            message += " " + row[2]
            message += " " + self.__language.read_micrograms( int(row[3]) )
            message += " " + levels[row[4]] + ' _ '
        return message


    def get_data(self):
        self.__logger.info("::: Pobieram informacje o skażeniu powietrza...")

        stationName = self.mbstr2asci(self.getStationName())

        message = " "
        message = " _ informacja_o_skaz_eniu_powietrza _ "
        message += " stacja_pomiarowa " + stationName + " _ "

        self.__logger.info("::: Przetwarzam dane...\n")

        sensorsData = self.getSensorsData()
        valuesMessage = self.prepareMessage(sensorsData)

        message += valuesMessage
        print "\n"
        return {
            "message": message,
            # "source": "powietrze_malopolska_pl",
        }

    def mbstr2asci(self, string):
        """Zwraca "bezpieczną" nazwę dla wyrazu z polskimi znakami diakrytycznymi"""
        return string.lower().\
            replace(u'ą',u'a_').replace(u'ć',u'c_').\
            replace(u'ę',u'e_').replace(u'ł',u'l_').\
            replace(u'ń',u'n_').replace(u'ó',u'o_').\
            replace(u'ś',u's_').replace(u'ź',u'x_').\
            replace(u'ż',u'z_').replace(u' ',u'_').\
            replace(u'-',u'_').replace(u'(',u'').\
            replace(u')',u'').replace(u'.',u'').\
            replace(u',',u'')









