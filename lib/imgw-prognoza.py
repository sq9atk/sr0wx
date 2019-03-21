#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
#
#   Copyright 2009-2011 Michal Sadowski (sq6jnx at hamradio dot pl)
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

import urllib
import re
import datetime


class imgw_prognoza:
    
    poczatek = """:00"""
    koniec   = """Noc"""



    def downloadFile(self, url):
        webFile = urllib.urlopen(url)
        return webFile.read()

    

# Sa dwa sposoby na okreslenie zachmurzenia i zjawisk. Pierwszy to sprawdzenie
# po numerkach obrazka, drugi to przeparsowanie slownego komentarza.
#
# Krzyżykami oznaczam co zgadłem:

    zachmurzenie = {
        0: "bezchmurnie",
        1: "pogodnie",
        2: "slabe zachmurzenie", #
        3: "pogodnie, okresami wzrost zachmurzenia do umiarkowanego",
        4: "zachmurzenie umiarkowane", #
        5: "pochmurno", #
        6: "Pochmurno, okresami przejaśnienia",
        7: "niemal całkowite zachmurzenie", #
        8: "zachmurzenie calkowite" }

    zjawiska ={
        00: "brak zjawisk", #
        60: "slabe opady deszczu",
        61: "deszcz", #
        68: "deszcz ze śniegiem",#
        70: "slabe opady sniegu",
        90: "burze" } #

    prognozy = {}
    prognoza = {}

    def __init__(self, url, datetime=None):
        file = self.downloadFile(url).split("\r\n")
        _data = re.compile("\((\d{1,2})\.(\d{1,2})\.(\d\d\d\d)\)")

        for i in range(0,len(file)):
            if len(_data.findall(file[i]))>0:
                data = _data.findall(file[i])
                self.prognozy["-".join((data[0]))]={}

            elif ":00" in file[i]: 
                godzina  = int("".join(file[i].split(">")).split("<")[2].split("\"")[2].split(":")[0])

                zachm    = "".join(file[i+1].split(">")).split("<")[2].split("\"")[1]

                temp     = "".join(file[i+2].split(">")).split("<")[2].split("\"")[2]
                tempOdcz = "".join(file[i+2].split(">")).split("<")[4].split("(")[1].split(")")[0]
                cisn     = "".join(file[i+2].split(">")).split("<")[7].split("\"")[8].split(" hPa")[0]

                silaWiatru    = "".join(file[i+3].split(">")).split("<")[1].split("\"")[8].split(" m/s")[0]
                kierWiatru     = "".join(file[i+3].split(">")).split("<")[2].split("\"")[1]
                kierWiatruSl   = "".join(file[i+3].split(">")).split("<")[2].split("\"")[3].replace("-"," ")

                koment   = "".join(file[i+4].split(">")).split("<")[1].split("\"")[8]

                self.prognozy["-".join((data[0]))][godzina]={'zachm':zachm, 'temp':float(temp), 'tempOdcz':float(tempOdcz), 'cisn':int(cisn), 'silaWiatru':float(silaWiatru), 'kierWiatru':kierWiatru, 'kierWiatruSl':kierWiatruSl, 'koment':koment}

        self.przygotujPrognoze()

    def przygotujPrognoze(self,datetime):
        deltaT=31*24*60 # 1 month in minutes

url = """http://www.pogodynka.pl/miasto.php?miasto=Wroc%B3aw&gmina=Wroc%B3aw&powiat=Wroc%B3aw&wojewodztwo=dolno%B6l%B1skie&czas=&model="""

imgw = imgw_prognoza(url, "44")
