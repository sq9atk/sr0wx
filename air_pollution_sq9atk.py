#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import urllib2
import logging
import json
import socket

from pprint import pprint

# LISTA STACJI Z NUMERAMI
# https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?size=2000

from sr0wx_module import SR0WXModule

class AirPollutionSq9atk(SR0WXModule):
    """Klasa pobierająca info o zanieczyszczeniach powietrza"""

    __ENVELOPE_KEYS = ('@context', 'meta', 'links', 'totalPages')

    F_SENSOR_ID = u'Identyfikator stanowiska'
    F_STATION_ID = u'Identyfikator stacji'
    F_PARAM_NAME = u'Wskaźnik'
    F_PARAM_CODE = u'Wskaźnik - kod'
    F_DATA_VALUE = u'Wartość'
    F_STATION_NAME = u'Nazwa stacji'

    def __init__(self, language, service_url, city_id=1, station_id=3):
        self.__language = language
        self.__service_url = service_url
        self.__station_id = station_id
        self.__logger = logging.getLogger(__name__)

        self.__stations_url = "station/findAll"
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

    def extractPayload(self, data):
        if not data:
            return None
        for key, value in data.items():
            if key not in self.__ENVELOPE_KEYS:
                return value
        return None

    def getStationName(self):
        url = self.__service_url + self.__stations_url + "?size=2000"
        stationName = ''
        rows = self.extractPayload(self.getJson(url)) or []
        for station in rows:
            if station.get(self.F_STATION_ID) == self.__station_id:
                stationName = station.get(self.F_STATION_NAME, '')
                break
        return stationName

    def getSensorValue(self, sensorId):
        url = self.__service_url + self.__sensor_url + str(sensorId)
        rows = self.extractPayload(self.getJson(url)) or []
        value = None
        for item in rows:
            val = item.get(self.F_DATA_VALUE)
            if isinstance(val, (int, float)):
                value = val
                break
        return value

    F_GENERAL_CATEGORY = u'Nazwa kategorii indeksu'

    def getLevelIndexData(self):
        url = self.__service_url + self.__index_url + str(self.__station_id)
        return self.extractPayload(self.getJson(url)) or {}

    def getGeneralIndexName(self, levelIndexData):
        category = levelIndexData.get(self.F_GENERAL_CATEGORY)
        return self.mbstr2asci(category) if category else 'empty'

    def categoryKeyFor(self, paramCode):
        # UWAGA: GIOŚ ma literówkę we własnym API - to pole używa
        # "wskażnika" (przez "ż"), podczas gdy wszystkie inne pola
        # tego samego obiektu AqIndex poprawnie piszą "wskaźnika"
        return u'Nazwa kategorii indeksu dla wskażnika ' + paramCode

    def getSensorsData(self, levelIndexData):
        url = self.__service_url + self.__station_url + str(self.__station_id)
        rows = self.extractPayload(self.getJson(url)) or []
        sensors = []
        for row in rows:
            paramCode = row[self.F_PARAM_CODE]
            value = self.getSensorValue(row[self.F_SENSOR_ID])
            if value is not None and value > 1:  # czasem tu schodzi none
                qualityIndexName = self.mbstr2asci(paramCode) + "IndexLevel"
                category = levelIndexData.get(self.categoryKeyFor(paramCode))
                index = self.mbstr2asci(category) if category else 'empty'
                sensors.append([
                    row[self.F_SENSOR_ID],
                    qualityIndexName,
                    self.mbstr2asci(row[self.F_PARAM_NAME]),
                    value,
                    index
                ])
        if len(sensors) > 0:
            return sensors
        else:
            raise Exception("brak danych pomiarowych")

    LEVELS = {
        'bardzo_dobry'  :'poziom_bardzo_dobry _ ',
        'dobry'         :'poziom_dobry _ ',
        'dostateczny'   :'poziom_dostateczny _ ',
        'umiarkowany'   :'poziom_umiarkowany _ ',
        'zly'           :'poziom_zl_y _ ', # ten jest chyba nieuzywany
        'zl_y'          :'poziom_zl_y _ ',
        'bardzo_zly'    :'poziom_bardzo_zl_y _ ', # ten też jest chyba nieuzywany
        'bardzo_zl_y'   :'poziom_bardzo_zl_y _ ',
        'empty'         : ''
    }

    def prepareMessage(self, data):
        message = " "
        for row in data:
            message += " " + row[2]
            message += " " + self.__language.read_micrograms( int(row[3]) )
            message += " " + self.LEVELS[row[4]]
        return message


    def get_data(self):
        self.__logger.info("::: Pobieram informacje o skażeniu powietrza...")
        self.__logger.info("::: Przetwarzam dane...\n")

        levelIndexData = self.getLevelIndexData()
        sensorsData = self.getSensorsData(levelIndexData)
        valuesMessage = self.prepareMessage(sensorsData)
        generalIndexName = self.getGeneralIndexName(levelIndexData)

        message = " "
        message = " _ informacja_o_skaz_eniu_powietrza _ "
        message += " stacja_pomiarowa " + self.mbstr2asci(self.getStationName()) + " _ "
        message += " ogolny_stan_powietrza " + self.LEVELS[generalIndexName]
        message += valuesMessage
        print "\n"
        return {
            "message": message,
            "source": "powietrze_malopolska_pl",
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
