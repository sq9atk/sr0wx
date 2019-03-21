#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import urllib2
import re
import logging
import pytz

from datetime import datetime
from sr0wx_module import SR0WXModule

class RadioactiveSq9atk(SR0WXModule):
    """Klasa pobierająca dane o promieniowaniu"""

    def __init__(self,language,service_url,sensor_id):
        self.__service_url = service_url
        self.__sensor_id = sensor_id
        self.__language = language
        self.__logger = logging.getLogger(__name__)

    def downloadFile(self, url):
        webFile = urllib2.urlopen(url)
        return webFile.read()

    def isSensorMatchedById(self, sensorId, string):
        pos = string.find(","+str(sensorId)+", ")
        return pos >= 0

    def isSensorRow(self, string):
        string = " "+string # na początku trzeba dodac spację bo inaczej find nie znajduje pierwszego znaku
        pos = string.find("Overlay(createMarker(")
        return pos >= 0
        
    def cleanUpString(self, string):
        string = string.replace("<br />","<br/>")
        string = string.replace("<br>","<br/>")
        string = string.replace("'","")
        
        string = string.replace("Last contact: ","")
        string = string.replace("Overlay(createMarker(new GLatLng","")
        string = string.replace(" Last sample: ","")
        string = string.replace("24 hours average: ","")
        string = string.replace(" uSv/h","")
        
        string = string.replace("(","")
        string = string.replace(")","")
        return string
                
    def prepareSensorData(self, string):
        string = self.cleanUpString(string)
        arr = string.split("<br/>")

        arrPart = arr[0].split(",")
        arr += arrPart
        return arr
  
    def getSensorData(self, html):
        dataArr = html.split("map.add")
        data = {}
        
        for row in dataArr:
            if self.isSensorRow(row):
                if self.isSensorMatchedById(self.__sensor_id, row):
                    sensorDataArr = self.prepareSensorData(row)

                    data['time'] = sensorDataArr[1]
                    data['current'] = sensorDataArr[10]
                    data['average'] = sensorDataArr[2]
        return data
        
    def get_data(self):
        self.__logger.info("::: Pobieram dane...")
        html = self.downloadFile(self.__service_url)

        self.__logger.info("::: Przetwarzam dane...\n")
        data = self.getSensorData(html)
        
        msvCurrent = int(float(data['current'])*100)
        msvAverage = int(float(data['average'])*100)
        
        averageValue = " ".join(["wartos_c__aktualna",self.__language.read_decimal( msvCurrent )+" ","mikrosjiwerta","na_godzine_"])
        currentValue = " ".join(["s_rednia_wartos_c__dobowa",self.__language.read_decimal( msvAverage )+" ","mikrosjiwerta","na_godzine_"])
        
        message = " ".join([" _ poziom_promieniowania _ " ,averageValue ," _ " ,currentValue ," _ "])
                
        return {
            "message": message,
            "source": "radioactiveathome_org",
        }
