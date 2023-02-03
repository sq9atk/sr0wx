#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import urllib2
import logging
from datetime import datetime
import json as JSON
import socket

from sr0wx_module import SR0WXModule


class OpenWeatherSq9atk(SR0WXModule):
    """Klasa pobierająca dane o promieniowaniu"""

    def __init__(self, language, api_key, lat, lon, service_url):

        self.__service_url = service_url
        self.__lat = lat
        self.__lon = lon
        self.__api_key = api_key   
        self.__language = language
        self.__logger = logging.getLogger(__name__)

        self.events = {
            200: 'burza_z_lekkimi_opadami_deszczu', # thunderstorm with light rain
            201: 'burza_z_opadami_deszczu',           # thunderstorm with rain
            202: 'burza_z_silnymi_opadami_deszczu', # thunderstorm with heavy rain
            210: 'niewielka_burza',                 # light thunderstorm
            211: 'burza',                           # thunderstorm
            212: 'silna_burza',                     # heavy thunderstorm
            221: 'przelotna_burza',                 # ragged thunderstorm
            230: 'burza_z_lekką_mżawką',            # thunderstorm with light drizzle
            231: 'burza_z_mżawką',                  # thunderstorm with drizzle
            232: 'burza_z_silną_mżawką',            # thunderstorm with heavy drizzle

            300: 'lekka_mzawka',                 # light intensity drizzle
            301: 'mzawka',                       # drizzle
            302: 'silna_mzawka',                 # heavy intensity drizzle
            310: 'lekki_mzacy_deszcz',           # light intensity drizzle rain
            311: 'mzacy_deszcz',                 # drizzle rain
            312: 'silny_mzacy_deszcz',           # heavy intensity drizzle rain
            313: 'ulewa_z_mzawka',               # shower rain and drizzle
            314: 'silna_ulewa_z_mzawka',         # heavy shower rain and drizzle
            321: 'ulewa_z_mzawka',               # shower drizzle

            500: 'lekkie_opady_deszczu',             # light rain     10d
            501: 'umiarkowane_opady_deszczu ',       # moderate rain     10d
            502: 'intensywne_opady_deszczu',         # heavy intensity rain     10d
            503: 'bardzo_intensywne_opady_deszczu',  # very heavy rain     10d
            504: 'oberwanie_chmury',                 # extreme rain     10d
            511: 'marznacy_deszcz',                  # freezing rain 
            520: 'lekka_ulewa',                      # light intensity shower rain     09d
            521: 'ulewa',                            # shower rain     09d
            522: 'silna_ulewa',                      # heavy intensity shower rain     09d
            531: 'przelotna_ulewa',                  # ragged shower rain     09d

            600: 'niewielkie_opady_sniegu',      #light snow 
            601: 'opady_sniegu',                 #snow 
            602: 'intensywne_opady_sniegu',      #heavy snow 
            611: 'snieg_z_deszczem',             #sleet 
            612: 'snieg_z_deszczem',             #shower sleet 
            615: 'snieg_z_niewielkim_deszczem',  #light rain and snow 
            616: 'snieg_z_deszczem',             #rain and snow 
            620: 'lekka_sniezyca',               #light shower snow 
            621: 'śniezyca',                     #showersnow 
            622: 'intensywna_sniezyca',          #heavy shower snow  

            701: 'zamglenia',           # mist     
            711: 'zadymienie',          # smoke     
            721: 'mgla',                # haze     
            731: 'kusz_i_piach',        # sand, dust whirls     
            741: 'mgla',                # fog     
            751: 'piasek',              # sand     
            761: 'pyl',                 # dust     
            762: 'pyl_wulkaniczny',     # volcanic ash     
            771: 'szkwaly',             # squalls     
            781: 'tornado',             # tornado     

            800: 'bezchmurnie',
            801: 'lekkie_zachmurzenie', 
            802: 'niewielkie_zachmurzenie', 
            803: 'zachmurzenie_umiarkowane', 
            804: 'pochmurno'
        }

    def downloadFile(self, url):
        try:
            webFile = urllib2.urlopen(url, None, 30)
            return webFile.read()
        except urllib2.URLError, e:
            print e
        except socket.timeout:
            print "Timed out!"
        return ""

    def getHour(self):
        time =  ":".join([str(datetime.now().hour), str(datetime.now().minute)])
        datetime_object = datetime.strptime(time, '%H:%M')
        time_words = self.__language.read_datetime(datetime_object, '%H %M')
        return time_words

    def getWeather(self, json):    
        message = ' _ ';
        for row in json:
            if row['id'] in self.events:
                message += ' ' + self.events[row['id']] + ' '
        return message

    def getClouds(self, json):
        msg = ' ';
        if json['all'] > 0:
            msg += ' _ pokrywa_chmur ' + self.__language.read_percent( int(json['all']) )
        return msg

    def getMainConditions(self, json):
        msg = ' _ '
        msg += ' temperatura ' + self.__language.read_temperature( int(json['temp']) )
        msg += ' cisnienie ' + self.__language.read_pressure( int(json['pressure']) )
        msg += ' wilgotnosc ' + self.__language.read_percent( int(json['humidity']) )
        return msg

    def getVisibility(self, json):
        msg = ' _ ';
        msg += ' widocznosc ' + self.__language.read_distance( int(json/1000) )
        return msg

    def getWind(self, json):
        msg = ' _ ';
        msg += ' predkosc_wiatru ' 
        msg += ' ' + self.__language.read_speed( int(json['speed']) )
        msg += ' ' + self.__language.read_speed( int(json['speed']/1000*3600),'kmph')

        if 'deg' in json:
            msg += ' _ wiatr '
            if 0 <= json['deg'] <= 23:  msg += ' polnocny '
            if 23 <= json['deg'] <= 67:  msg += ' polnocno wschodni '
            if 67 <= json['deg'] <= 112:  msg += ' wschodni '
            if 112 <= json['deg'] <= 157:  msg += ' poludniowo wschodni '
            if 157 <= json['deg'] <= 202:  msg += ' poludniowy '
            if 202 <= json['deg'] <= 247:  msg += ' poludniowo zachodni '
            if 247 <= json['deg'] <= 292:  msg += ' zachodni '
            if 292 <= json['deg'] <= 337:  msg += ' polnocno zachodni '
            if 337 <= json['deg'] <= 360:  msg += ' polnocny '
            msg += self.__language.read_degrees( int(json['deg']) )
        return msg

    def get_data(self):
        
        self.__logger.info("::: Pobieram aktualne dane pogodowe...")
        
        weather_service_url = self.__service_url + 'weather?lat=' + str(self.__lat) + '&lon='+str(self.__lon) + '&units=metric&appid=' + self.__api_key
        self.__logger.info( weather_service_url )
        weatherJson = JSON.loads( self.downloadFile(weather_service_url) )

        self.__logger.info("::: Pobieram dane prognozy pogody...")
        
        forecast_service_url = self.__service_url + 'forecast?lat=' + str(self.__lat) + '&lon='+str(self.__lon) + '&units=metric&appid=' + self.__api_key
        self.__logger.info( forecast_service_url )
        forecastJsonAll = JSON.loads( self.downloadFile(forecast_service_url) )

        self.__logger.info("::: Przetwarzam dane...\n")

        message = "".join([ \
                        " stan_pogody_z_godziny ", 
                        self.getHour(), \
                        self.getWeather( weatherJson['weather'] ), \
                        self.getClouds( weatherJson['clouds'] ), \
                        self.getMainConditions( weatherJson['main'] ), \
                        #self.getVisibility( weatherJson['visibility'] ), \
                        self.getWind( weatherJson['wind'] ), \
                     ])

        forecastJson = forecastJsonAll['list'][1]
        message += "".join([ \
                        " _ prognoza_na_nastepne cztery godziny ", 
                        self.getWeather( forecastJson['weather'] ), \
                        self.getClouds( forecastJson['clouds'] ), \
                        self.getMainConditions( forecastJson['main'] ), \
                        self.getWind( forecastJson['wind'] ), \
                     ])

        forecastJson = forecastJsonAll['list'][4]
        message += "".join([ \
                        " _ prognoza_na_nastepne dwanascie godzin ", 
                        self.getWeather( forecastJson['weather'] ), \
                        self.getClouds( forecastJson['clouds'] ), \
                        self.getMainConditions( forecastJson['main'] ), \
                        self.getWind( forecastJson['wind'] ), \
                     ])

        self.__logger.info("::: Przetwarzam dane...\n")
                
        return {
            "message": message,
            "source": "open_weather_map",
        }
