#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import re
import logging
import socket
import requests

from PIL import Image
from pprint import pprint

from sr0wx_module import SR0WXModule

class VhfTropoSq9atk(SR0WXModule):
    """Klasa pobierająca dane kalendarzowe"""

    def __init__(self, language, service_url, qthLon, qthLat):
        self.__service_url = service_url
        self.__language = language
        self.__logger = logging.getLogger(__name__)

        self.__areaSize = 70
        self.__colorSampleScatter = 5

        self.__qthLon = float(qthLon)
        self.__qthLat = float(qthLat)

        self.__mapLonStart = float(-10)
        self.__mapLonEnd = float(40)

        self.__mapLatStart = float(56)
        self.__mapLatEnd = float(27)

    def getHtmlFromUrl(self, url):
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                return resp.content
            else:
                print("HTML response error")
                return None

        except requests.exceptions.RequestException as e:
            print("HTML download error: %s" % e)
            return None

    def findMapUrlInHtml(self, html, target_id):
        pattern = r'<img\s+(?:[^>]*\s+)?id="' + re.escape(target_id) + r'"(?:[^>]*)\s+src="([^"]+)"'
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            mapUrl = match.group(1)
            return mapUrl
        else:
            return None

    def downloadMapFile(self, mapUrl, targetFileName):
        try:
            self.__logger.info("::: Odpytuję adres: " + mapUrl)
            response = requests.get(mapUrl, timeout=30)

            with open(targetFileName, "wb") as mapFile:
                mapFile.write(response.content)

        except requests.exceptions.Timeout:
            print("Przekroczono czas oczekiwania")
        except Exception as e:
            print("Błąd pobierania mapy: %s" % e)
        return


    def readMapImageFile(self, fileName):

        mapImg = Image.open(fileName, 'r')
        mapRgbImg = mapImg.convert('RGB')
        mapCropped = mapRgbImg.crop((43, 67, 888, 654))
        try:
            mapCropped.save(fileName)

        except Exception as e:
            print("Błąd odczytu pliku z mapą: %s" % e)
        return mapCropped

    def lonLatToMapXY(self, lon, lat, imgWidth, imgHeight):
        self.__logger.info("::: Przetwarzam dane...")
        imgWidth = float(imgWidth)
        imgHeight = float(imgHeight)
        lonRange =  self.__mapLonEnd - self.__mapLonStart
        latRange =  self.__mapLatEnd - self.__mapLatStart
        lonMod = (imgWidth / lonRange)
        latMod = (imgHeight / latRange)
        pixelY = round(latMod * (lat - self.__mapLatStart))
        pixelX = round(lonMod * (lon - self.__mapLonStart))

        return int(pixelX), int(pixelY)

    def prepareSamplesCoordinates(self, x_center, y_center, size, maxWidth, maxHeight):
        half_size = size // 2

        if y_center + half_size > maxHeight:
            y_center = maxHeight - half_size

        if y_center - half_size < 0:
            y_center = half_size

        if x_center + half_size > maxWidth:
            x_center = maxWidth - half_size

        if x_center - half_size < 0:
            x_center = half_size

        coordinates = []
        for dx in range(-half_size, half_size + 1):
            for dy in range(-half_size, half_size + 1):
                coordinates.append((x_center + dx, y_center + dy))

        return coordinates[::self.__colorSampleScatter]

    def collectSamplesColors(self, image, coordinates):
        colors = []
        for x, y in coordinates:
            pixel_value = image.getpixel((x, y))
            colorHex = '#%02x%02x%02x' % pixel_value
            if colorHex != '#ffffff' and colorHex != '#000000':
                colors.append(colorHex)

        return colors

    def calculateColorsOccurence(self, input_array):
        total_elements = len(input_array)
        frequency_dict = {}

        for value in input_array:
            if value in frequency_dict:
                frequency_dict[value] += 1
            else:
                frequency_dict[value] = 1

        percentage_frequencies = {}
        for key, value in frequency_dict.items():
            percentage = (value / float(total_elements)) * 100
            percentage_frequencies[key] = percentage

        return sorted(percentage_frequencies.items(), key=lambda item: item[1], reverse=True)

    def getColorPunctation(self, colorHex):
        colors = {
            '#141414' : 0.00,  #czarny
            '#8200dc' : 1.00,  #fioletowy
            '#3377ff' : 2.00,  #błękitny
            '#02d0a1' : 3.00,  #pistacjowy
            '#a0e632' : 4.00,  #cytrynowy
            '#e6dc32' : 5.00,  #żółty
            '#e6af2d' : 6.00,  #musztardowy
            '#f08228' : 7.00,  #pomarańczowy
            '#fa3c3c' : 8.00,  #czerwony
            '#ff80c0' : 9.00,  #różowy
            '#ffb4dc' : 10.00, #różowy pastelowy
            '#cc86cc' : 11.00, #różowy szary
            '#c0c0c0' : 12.00  #szary
        }

        result = False
        for color, value in colors.iteritems():
            if color == colorHex:
                result = value
        return result

    def countVHFCondition(self, colorsPercentage):
        divider = 0.00
        score = 0.00
        for row in colorsPercentage:
            colorHex = row[0]
            percentage = row[1]
            colorPunctation = self.getColorPunctation(colorHex)
            divider += percentage
            score += percentage * colorPunctation
        conditionValue = score / divider

        return conditionValue

    def getLocationCondition(self, mapImg, x, y):
        maxWidth, maxHeight = mapImg.size

        samplesCoordinates = self.prepareSamplesCoordinates(x, y, self.__areaSize, maxWidth, maxHeight)
        samples = self.collectSamplesColors(mapImg, samplesCoordinates)

        occurences = self.calculateColorsOccurence(samples)
        locationConditionValue = self.countVHFCondition(occurences)

        return locationConditionValue

    def getDirectionalConditions(self, mapImg, x, y):
        shift = self.__areaSize/2
        shift = self.__areaSize

        return {
            'N' :    self.getLocationCondition(mapImg, x, y-shift),
            'NE' :   self.getLocationCondition(mapImg, x+shift, y-shift),
            'E' :    self.getLocationCondition(mapImg, x+shift, y),
            'SE' :    self.getLocationCondition(mapImg, x+shift, y+shift),
            'S' :    self.getLocationCondition(mapImg, x, y+shift),
            'SW' :    self.getLocationCondition(mapImg, x-shift, y+shift),
            'W' :    self.getLocationCondition(mapImg, x-shift, y),
            'NW' :    self.getLocationCondition(mapImg, x-shift, y-shift),
        }


    def getTopDirectionsValues(self, input_table):
        filtered_rows = []
        for key, value in input_table.iteritems():
            filtered_rows.append((key, value))

        filtered_rows.sort(key=lambda x: x[1], reverse=True)

        keys = ['vhf_' + row[0].lower() for row in filtered_rows[:2]]

        if len(keys) == 2:
            keys.insert(1, 'vhf_oraz')

        return keys

    def prepareMessage(self, mainConditionValue, directionalConditionsValues):
        message = 'vhf_brak_szans_na_lacznosc_troposferyczna'

        if mainConditionValue > 0.3:
            message = 'vhf_minimalne_szanse_na_lacznosc_troposferyczna'
        if mainConditionValue > 0.5:
            message = 'vhf_niewielkie_szanse_na_lacznosc_troposferyczna'
        if mainConditionValue > 1:
            message = 'vhf_spore_szanse_na_lacznosc_troposferyczna'
        if mainConditionValue > 2:
            message = 'vhf_duze_szanse_na_lacznosc_troposferyczna'
        if mainConditionValue > 5:
            message = 'vhf_bardzo_duze_szanse_na_lacznosc_troposferyczna'
        if mainConditionValue > 8:
            message = 'vhf_wyjatkowo_duze_szanse_na_lacznosc_troposferyczna'
        if mainConditionValue > 3:
            message = ' vhf_uwaga vhf_warunki_podwyzszone _ ' + message
        if mainConditionValue > 0.5:
            message += ' vhf_najlepsze_warunki_w_kierunku '
            message += " _ ".join( self.getTopDirectionsValues(directionalConditionsValues))

        return message


    def get_data(self):
        html = self.getHtmlFromUrl(self.__service_url)
        mapUrl = self.findMapUrlInHtml(html, "imgClickAndChange")

        self.downloadMapFile(mapUrl, 'vhf_map.png')

        mapImg = self.readMapImageFile('vhf_map.png')

        mapWidth, mapHeight = mapImg.size

        x, y = self.lonLatToMapXY(self.__qthLon, self.__qthLat, mapWidth, mapHeight)

        mainConditionValue = self.getLocationCondition(mapImg, x, y)
        directionalConditionsValues = self.getDirectionalConditions(mapImg, x, y)

        message = " ".join([
            " _ vhf_propagacja_w_pasmie_vhf _ ",
            "   " . join([ self.prepareMessage(mainConditionValue, directionalConditionsValues) ]),
            " _ "
        ])

        return {
            "message": message,
            "source": "vhf_dx_info_center",
        }
