#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import logging, re, subprocess
import urllib2

from sr0wx_module import SR0WXModule

class GeoMagneticSq9atk(SR0WXModule):
    """Klasa pobierająca info o sytuacji geomagnetycznej"""

    def __init__(self, language, service_url):
        self.__language = language
        self.__service_url = service_url
        self.__logger = logging.getLogger(__name__)
    
        self.__days = ['dzis','jutro','po_jutrze']
        self.__conditions = {
            0:' ',
            1:'brak_istotnych_zaburzen__geomagnetycznych',   2:'lekkie_zaburzenia_geomagnetyczne',
            3:'umiarkowane_zabuz_enia_geomagnetyczne',      4:'mal_a_burza_geomagnetyczna',
            5:'umiarkowana_burza_geomagnetyczna',           6:'silna_burza_geomagnetyczna',
            7:'sztorm_geomagnetyczny',                      8:'duz_y_sztorm_geomagnetyczny'
        }
        self.__seasons = {
            0:' ',
            1:'kro_tko_po_po_l_nocy',    4:'nad_ranem',              7:'rano',
            10:'przed_pol_udniem',      13:'wczesnym_popol_udniem', 16:'po_pol_udniu',
            19:'wieczorem',             22:'przed_po_l_noca_',
        }
        self.__fluctuations = {
            0:'niezauwaz_alne', 1:'znikome', 2:'lekkie',       3:'podwyz_szone',
            4:'umiarkowane',    5:'duz_e',   6:'bardzo_duz_e', 7:'ekstremalne'
        }

    def downloadDataFromUrl(self, url):
        opener = urllib2.build_opener()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
        }
        opener.addheaders = headers.items()
        response = opener.open(url)

        return response.read()

        
    def getDataParsedHtmlData(self):
        self.__logger.info("::: Pobieram informacje...")
        
        html = self.downloadDataFromUrl(self.__service_url)
         
        
        r = re.compile(r'<td class="gm_td gm-(.*?)">\n(.*?)(\d)\n(.*?)</td>') #pobieramy listę wartości
        
        
        return r.findall(html)

    def groupValuesByDays(self, data):
        hour = 1
        dayNum = 1
        current_hour = 18
        output = {1:{},2:{},3:{}}

        for i, val in enumerate(data):
            if dayNum > 1 or hour > current_hour: # omijamy godziny z przeszłości
                value = data[i][2]
                output[dayNum][hour] = value

            hour += 3
            if hour > 22:
                hour = 1
                dayNum += 1
        return output

    def getStrongestConditionOfDay(self,data):
        maxValue = {
            'value':0,
            'at':0,
        }
        for key, row in data.iteritems():    
            if row > maxValue['value']:
                maxValue['value'] = row
                maxValue['at'] = key
        return maxValue

    def getDailyFluctuation(self, data):
        values = data.values()
        return int(max(values)) - int(min(values))
    
    def get_data(self):
        values = self.getDataParsedHtmlData()

        daysValues = self.groupValuesByDays(values)
        
        message = ' _ sytuacja_geomagnetyczna_w_regionie ';
        
        self.__logger.info("::: Przetwarzam dane...\n")
        for d, day in daysValues.iteritems():
            
            if len(day) > 0:
                a=1    
                message += " _ "+self.__days[d-1] + " "
                condition = self.getStrongestConditionOfDay(day) 
                
                message += self.__seasons[condition['at']] + " "
                message += self.__conditions[int(condition['value'])] + " "

                message += self.__fluctuations[self.getDailyFluctuation(day)] + " wahania_dobowe "

        return {
            "message": message + "_",
            "source": "gis_meteo",
        }
