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
import logging
import json

from sr0wx_module import SR0WXModule

class MeteoalarmSq9atk(SR0WXModule):
    """Klasa przetwarza dane na temat zagrożeń meteorologicznych."""

    def __init__(self,region):
        self.__region = region
        self.__logger = logging.getLogger(__name__)

        self.warningsPrefix = "zagrozenia_meteorologiczne_dla_wojewodztwa"
        self.warningsLevel = "poziom_zagrozenia"
        self.warningsLevels = ["nieokreslony","","niski","sredni","wysoki"]
        self.warnings = [
            "","silny_wiatr","snieg_lub_oblodzenie", 
            "burze","mgly","wysokie_temperatury",
            "niskie_temperatury","zjawiska_strefy_brzegowej","pozary_lasow",
            "lawiny","intensywne_opady_deszczu","inne_zagrozenia"]
        self.regions = {
            'PL001':"mazowieckiego",        'PL002':"lubuskiego", 
            'PL003':"zachodniopomorskiego", 'PL004':"pomorskiego", 
            'PL005':"dolnoslaskiego",       'PL006':"opolskiego",
            'PL007':"śląskiego",            'PL008':"malopolskiego", 
            'PL009':"podkarpackiego",       'PL010':"świętokrzyskiego",
            'PL011':"łódzkiego",            'PL012':"wielkopolskiego",
            'PL013':"kujawsko_pomorskiego", 'PL014':"warminsko_mazurskiego", 
            'PL015':"lubelskiego",          'PL016':"podlaskiego",
            'IE003':"dolnoslaskiego",
        }

    def getDataFromUrl(self, url):
        dane = urllib2.urlopen(url)
        self.__logger.info("Przetwarzam...\n")
        zagrozenia = json.load(dane)
        return zagrozenia
    
    def downloadFile(self, url):
        webFile = urllib2.urlopen(url)
        return webFile.read()

    def getWarnings(self, region, tomorrow=False):
        r = re.compile('pictures/aw(\d[01]?)([0234]).jpg')
        url = "http://www.meteoalarm.eu/index3.php?area=%s&day=%s&lang=EN" % (str(region),str(int(tomorrow)))
        result = []
        for line in self.downloadFile(url).split('\n'):
            matches = r.findall(line)
            if len(matches) is not 0 and int(matches[0][0])!=0:
                result = [
                    self.warnings[ int(matches[0][0]) ],
                    self.warningsLevel,
                    self.warningsLevels[ int(matches[0][1]) ],
                ]
        return " ".join(result)


    def get_data(self):
        self.__logger.info("::: Pobieram i przetwarzam dane...\n")

        today=""
        tomorrow=""
        today = self.getWarnings(self.__region, False)
        tomorrow = self.getWarnings(self.__region, True)
    
        message = "";
        if today== "" and tomorrow== "":
            pass
        elif today!= "" and tomorrow=="":
            message += " ".join([self.warningsPrefix," ",self.regions[self.__region],"_","dzis","_", today])
        elif today== "" and tomorrow!="":
            message += " ".join([self.warningsPrefix," ",self.regions[self.__region],"_", "jutro","_", tomorrow])
        else:
            message += " ".join([self.warningsPrefix," ",self.regions[self.__region],"_", "dzis","_", today,"_","jutro","_",tomorrow])

        message += " _ "

        return {
            "message": message,
            "source": "meteoalarm_eu",
        }







