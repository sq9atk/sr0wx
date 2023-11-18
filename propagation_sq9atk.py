#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import urllib
import logging
import socket

from PIL import Image
from pprint import pprint

from sr0wx_module import SR0WXModule

class PropagationSq9atk(SR0WXModule):
    """Klasa pobierająca dane kalendarzowe"""

    def __init__(self,language,service_url):
        self.__service_url = service_url
        self.__language = language
        self.__logger = logging.getLogger(__name__)
        self.__pixels = {
            # niepotrzebne pasma można zaremowac znakiem '#'
            160 : {'day' :{'x':50, 'y':60},  'night':{'x':100, 'y':60}},
            80 : {'day' :{'x':50, 'y':95},  'night':{'x':100, 'y':95}},
            40 : {'day' :{'x':50, 'y':140}, 'night':{'x':100, 'y':140}},
            20 : {'day' :{'x':50, 'y':185}, 'night':{'x':100, 'y':185}},
            10 : {'day' :{'x':50, 'y':230}, 'night':{'x':100, 'y':230}},
            6 : {'day' :{'x':50, 'y':270}, 'night':{'x':100, 'y':270}},
        }

        self.__levels = {
            '#17e624':'warunki_podwyzszone', # zielony
            '#e6bc17':'warunki_normalne', # żółty
            '#e61717':'warunki_obnizone', # czerwony
            '#5717e6':'pasmo_zamkniete', #fioletowy
        }

    def rgb2hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def downloadImage(self, url):
        try:
            self.__logger.info("::: Odpytuję adres: " + url)
            webFile = urllib.URLopener()
            webFile.retrieve(url, "propagacja.png")
            return Image.open("propagacja.png",'r')
        except socket.timeout:
            print "Timed out!\n"
        except:
            print "Data download error!\n"
        return

    def collectBandConditionsFromImage(self, image, dayTime):
        try:
            imageData = image.load()
            data = list()
            for band in sorted(self.__pixels):
                x = self.__pixels[band][dayTime]['x']
                y = self.__pixels[band][dayTime]['y']
                rgba = imageData[x,y]
                color = self.rgb2hex(( rgba[0],rgba[1],rgba[2] ));

                # można zaremowac wybraną grupę aby nie podawać info o konkretnych warunkach
                if self.__levels[color] == 'warunki_podwyzszone':
                    string = str(band) + '_metrow' + ' ' + self.__levels[color]
                    data[:0] = [string]

                if self.__levels[color] == 'warunki_normalne':
                    string = str(band) + '_metrow' + ' ' + self.__levels[color]
                    data[:0] = [string]

                if self.__levels[color] == 'warunki_obnizone':
                    string = str(band) + '_metrow' + ' ' + self.__levels[color]
                    data[:0] = [string]

                if self.__levels[color] == 'pasmo_zamkniete':
                    string = str(band) + '_metrow' + ' ' + self.__levels[color]
                    data[:0] = [string]

            return data
        except:
            return list()


    def get_data(self):
        image = self.downloadImage(self.__service_url)

        message = '';
        if image:
            self.__logger.info("::: Przetwarzam dane...\n")

            day = self.collectBandConditionsFromImage(image, 'day')
            night = self.collectBandConditionsFromImage(image, 'night')

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







