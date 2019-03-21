#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

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

import re, urllib


def between(a,b,c):
    if (a<=b and b<=c) or (c<=b and b<=a):
        return True
    else:
        return False

class taf:
    tafData = []

    weather = None

# Borrowed from pymetar.py, "slightly" modified. If element had not be translated type "%", ie.:
#
# "VC" : "%"
    _WeatherConditions = {
                      "DZ" : {
                               "" :   ["", "mzawka", ""],
                               "-" :  ["slaba", "",""],
                               "+" :  ["silna", "",""],
                               "VC" : ["", "", "w_poblizu"],
                               "MI" : ["niska", "",""],
                               "BC" : ["","mzawka",""],
                               "PR" : ["czesciowa", "",""],
                               "TS" : ["", "mzawka burza",""],
                               "BL" : ["", "", "z_zawieja"],
                               "SH" : ["przelotna", "",""],
                               "DR" : ["niska", "zamiec", ""],
                               "FZ" : ["marznaca","",""]
                             },
                      "RA" : {
                               "" :   ["", "deszcz", ""],
                               "-" :  ["lekki", "", ""],
                               "+" :  ["silny", "", ""],
                               "VC" : ["", "", "w_poblizu"],
                               "MI" : ["niski", "", ""],
                               "BC" : ["", "deszcz", ""],
                               "PR" : ["czesciowy","", ""],
                               "TS" : ["","burza",""],
                               "BL" : ["","","z_zawieja"],
                               "SH" : ["przelotny", "", ""],
                               "DR" : ["niski","", ""],
                               "FZ" : ["marznacy","",""]
                             },
                      "SN" : {
                               "" :   ["","snieg", ""],
                               "-" :  ["lekki", "", ""],
                               "+" :  ["silny", "", ""],
                               "VC" : ["", "", "w_poblizu"],
                               "MI" : ["niski", "",""],
                               "BC" : ["", "platy_sniegu", ""],
                               "PR" : ["","czesciowe_opady śniegu",""],
                               "TS" : ["", "burza_sniezna", ""],
                               "BL" : ["","zamiec_sniezna",""],
                               "SH" : ["", "przelotne opady sniegu", ""],
                               "DR" : ["","niska zamiec_sniezna",""],
                               "FZ" : ["","marznacy snieg",""]
                             },
                      "SG" : {
                               "" :   ["","opady sniegu ziarnistego",""],
                               "-" :  ["slabe", "",""],
                               "+" :  ["silne", "",""],
                               "VC" : ["", "", "w_poblizu"],
                               "MI" : ["niskie", "",""],
                               "BC" : ["","opady platow sniegu_ziarnistego",""],
                               "PR" : ["","czesciowe opady sniegu_ziarnistego",""],
                               "TS" : ["","burza_sniezna",""],
                               "BL" : ["","","z_zawieją"],
                               "SH" : ["przelotne","",""],
                               "DR" : ["","niska zamiec_sniezna",""],
                               "FZ" : ["marznace","",""]
                             },
                     "IC" : {
                              "" :   "%",
                              "-" :  "%",
                              "+" :  "%", 
                              "BC" : "%", #"Patches of ice crystals",
                              "PR" : "%", #"Partial ice crystals",
                              "TS" : "%", #("Ice crystal storm", "storm"),
                              "BL" : "%", #"Blowing ice crystals",
                              "SH" : "%", #"Showers of ice crystals",
                              "DR" : "%", #"Drifting ice crystals",
                              "FZ" : "%"  #"Freezing ice crystals",
                            },
                     "PE" : {
                              "" :   "%", #"Moderate ice pellets",
                              "-" :  "%", 
                              "+" :  "%",
                              "VC" : "%",
                              "MI" : "%",
                              "BC" : "%", #"Patches of ice pellets",
                              "PR" : "%", #"Partial ice pellets",
                              "TS" : "%", #("Ice pellets storm", "storm"),
                              "BL" : "%", #"Blowing ice pellets",
                              "SH" : "%", #"Showers of ice pellets",
                              "DR" : "%", #"Drifting ice pellets",
                              "FZ" : "%"  #"Freezing ice pellets",
                            },
                      "GR" : {
                               "" :   ["","grad",""], 
                               "-" :  ["slaby","",""], 
                               "+" :  ["silny","",""], 
                               "VC" : ["","","w poblizu"], 
                               "MI" : ["niski","",""], 
                               "BC" : "%", #"Patches of hail",
                               "PR" : "%", #"Partial hail",
                               "TS" : ["","burza_gradowa",""], 
                               "BL" : "%",
                               "SH" : ["","przelotne_opady gradu",""],
                               "DR" : "%", #"Drifting hail",
                               "FZ" : ["marznacy","grad",""] 
                             },
                      "GS" : {
                               "" :   "%",#"Moderate small hail",
                               "-" :  "%", #["słaba", "",""],
                               "+" :  "%", #["silna", "",""],
                               "VC" : "%", #["", "", "w pobliżu"],
                               "MI" : "%", #["niska", "",""],
                               "BC" : "%", #"Patches of small hail",
                               "PR" : "%", #"Partial small hail",
                               "TS" : "%", #("Small hailstorm", "storm"),
                               "BL" : "%", #"Blowing small hail",
                               "SH" : "%", #"Showers of small hail",
                               "DR" : "%", #"Drifting small hail",
                               "FZ" : "%", #"Freezing small hail",
                             },
                      "UP" : {
                               "" :   "%",  #"Moderate precipitation",
                               "-" :  "%", #["słaba", "",""],
                               "+" :  "%",  #["silna", "",""],
                               "VC" : "%", #["", "", "w pobliżu"],
                               "MI" : "%", #["niska", "",""],
                               "BC" : "%", #"Patches of precipitation",
                               "PR" : "%", #"Partial precipitation",
                               "TS" : "%", #("Unknown thunderstorm", "storm"),
                               "BL" : "%", #"Blowing precipitation",
                               "SH" : "%", #"Showers, type unknown",
                               "DR" : "%", #"Drifting precipitation",
                               "FZ" : "%", #"Freezing precipitation",
                             },
                      "BR" : {
                               "" :  ["","zamglenie",""],
                               "-" :  ["lekkie","",""],
                               "+" :  ["silne","",""],
                               "VC" : ["","","w_poblizu"],
                               "MI" : ["niskie","",""],
                               "BL" : ["","","z_wiatrem"],
                               "FZ" : ["marznace","",""], 
                             },
                      "FG" : {
                               "" :   ["","mgla",""], 
                               "-" :  ["lekka","",""],
                               "+" :  ["silna","",""],
                               "VC" : ["","","w_poblizu"],
                               "MI" : ["niska","",""],
                               "BL" : ["","","z_wiatrem"], 
                               "FZ" : ["marznaca","",""],
                             },
                      "SQ" : {
                               "" :  ["","nawalnica",""],
                               "-" : ["slaba", "",""],
                               "+" : ["silna", "",""],
                               "VC" :["", "", "w_poblizu"],
                             }
                    }


    knots2mps= 0.5144444444444445
    kmh2mps  = 0.2777777777777778
    mi2km    = 1.609344

    rawTAF=None
    ICAO = None

    def __init__(self, ICAO=None, at=(0,0,0), taf=None, address=None):
        # taf variable will be used for debug purposes.
        if taf is not None:
            report = taf.split("\n")
            header=report[0].split()
            originDate = header[1]
            self.rawTAF = taf

        if address== None:
           #address = "http://140.90.128.70/pub/data/forecasts/taf/stations/%ICAO%.TXT"
           #address = "http://204.227.127.33/metars/index.php?station_ids=%ICAO%&std_trans=standard&hoursStr=most+recent+only&chk_tafs=on&submitmet=Submit"
           address = "http://aviationweather.gov/adds/tafs/index.php?station_ids=%ICAO%&std_trans=standard&hoursStr=most+recent+only&chk_tafs=on&submitmet=Submit"

        if ICAO is not None:
            self.ICAO=ICAO
            url = address.replace("%ICAO%",str.upper(ICAO))
            taf = self.getFile(url)
            self.rawTAF = taf
            report = taf.split("\n")

        # ICAO = "EPWR"   # <--------------------------------- delete me
        dd,hh,mm=at

        _period  = re.compile('\d{4}/\d{4}')
        _wind= re.compile('(VRB|\d{3})(\d{2,3})(?:(G)(\d{2,3}))?(KT|MPS|KMH)(?:(\d{3})(V)(\d{3}))?')
        _vis     = re.compile('(?:^|\s)\d\d\d\d(?:$|\s)|P?\dSM')
        _weather  = re.compile('^(?:\+|-|VC)?(?:MI|BC|DR|BL|SH|TS|FZ)?(?:(?:DZ|RA|SN|SG|IC|PE|GR|GS)|(?:BR|FG|FU|VA|DU|SA|HZ)|(?:PO|SQ|FC|SS|DS))$')
        _skyCnd  = re.compile("(SKC|FEW|SCT|BKN|OVC|NSC)(\d\d\d(VV\d\d\d)?)?(CB|TCU)?")
        _temp    = re.compile("""\s(M)?\d\d/(M)?\d\d\s| # METAR
                                 T(M)?\d\d/?\d\dG # TAF""")
        _press   = re.compile("Q\d\d\d\d")
        _cavok   = re.compile("CAVOK")
        _nsw     = re.compile("NSW")

        _valid = re.compile('^TAF\ |TEMPO|B(E)?CMG|PROB|GRADU|RAPID|%s'%ICAO)
        for line in report:
            if _valid.search(line) is not None:
                TAFFound = True
                tl = {"period":"", "wind":"", "vis":"", "weather":"",
                    "skyCnd":"", "temp":"", "press":"", "cavok":"", "nsw":""} #, "change":None}
                for word in line.split(" "):
                    tl["period"] = (tl["period"] + " " + " ".join((self.flatten(_period.findall(word)) or "" ))).strip()
                    tl["wind"]	 = (tl["wind"]   + " " +  " ".join((self.flatten(_wind.findall(word)) or "" ))).strip()
                    tl["vis"]    = (tl["vis"]    + " " +  " ".join((self.flatten(_vis.findall(word)) or ""  ))).strip()
                    tl["weather"]= (tl["weather"]+ " " +  " ".join((self.flatten(_weather.findall(word)) or ""  ))).strip()
                    tl["temp"]   = (tl["temp"]  + " " +  " ".join((self.flatten(_temp.findall(word)) or ""  ))).strip()
                    tl["press"]  = (tl["press"] + " " +  " ".join((self.flatten(_press.findall(word)) or ""  ))).strip()
                    tl["skyCnd"] = (tl["skyCnd"]+ " " +  " ".join((self.flatten(_skyCnd.findall(word)) or "" ))).strip()
                    tl["cavok"]  = (tl["cavok"] + " " +  " ".join((self.flatten(_cavok.findall(word)) or ""  ))).strip()
                    tl["nsw"]    = (tl["nsw"]   + " " +  " ".join((self.flatten(_nsw.findall(word)) or "" ))).strip()

                    # tl["skyCnd"]= tl["skyCnd"]+ " ".join( (_skyCnd.findall(word)) )
					
                self.tafData.append(tl)

        TAF0 = self.tafData[0]
        keys = ["period", "wind", "vis", "weather", "skyCnd", "temp", "press","cavok","nsw"]
        for i in range(0,len(self.tafData)):
            for elem in keys:
                if self.tafData[i][elem].strip() == "":
                    self.tafData[i][elem] = TAF0[elem]
            if self.tafData[i]["cavok"]== "CAVOK" and "".join( 
                    (self.tafData[i]["vis"], self.tafData[i]["weather"], self.tafData[i]["skyCnd"]) ) == "":
                self.tafData[i]["vis"] = "P6SM"
                self.tafData[i]["weather"] = "NSW"
                self.tafData[i]["skyCnd"]= "SKC"
            elif self.tafData[i]["nsw"]=="NSW" and self.tafData[i]["weather"]:
                self.tafData[i]["weather"]="NSW"

        self.weather = self.prepare(dd,hh,mm)


    def flatten(self,x): # http://kogs-www.informatik.uni-hamburg.de/~meine/python_tricks
        """flatten(sequence) -> list

        Returns a single, flat list which contains all elements retrieved
        from the sequence and all recursively contained sub-sequences
        (iterables).

        Examples:
        >>> [1, 2, [3,4], (5,6)]
        [1, 2, [3, 4], (5, 6)]
        >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, MyVector(8,9,10)])
        [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

        result = []
        for el in x:
            #if isinstance(el, (list, tuple)):
            if hasattr(el, "__iter__") and not isinstance(el, basestring):
                result.extend(self.flatten(el))
            else:
                result.append(el)
        return result

    def getFile(self, url):
        webFile = urllib.urlopen(url)
        contents = webFile.read()
        webFile.close()
        return contents

    def changeMoment(self,dd,hh,mm):
        self.weather = self.prepare(dd,hh,mm)

    def prepare(self,dd,hh,mm=0): # prepareForecast
# Finding proper forecast may be a difficult task. Consider following TAF:
#
# EPWR 212000Z 2121/2206 18005KT SCT040   (1)
#     BECMG 2122/2224 29008KT             (2)
#     TEMPO 2121/2206 8000 SHRA BKN026CB  (3)
#     PROB30                              
#     TEMPO 2121/2203 23012G30KT TSRA     (4)
#
#   +-----------------------+
#   |         (4)           |
#   +-----------------------------------+
#   |   +-------+                       |
#   |   | (2)   |    (3)                |
#   +---+-------+-----------------------+
#   |                (1)                |
#  -+---+---+---+---+---+---+---+---+---+----------------------------------->
#  21  22  23  24   1   2   3   4   5   6                          time (hr)
#
#
# Lets say we want to know the forecast for 21st of this month at 23 UTC.
# It' easy to see that we can use *every line* from this TAF message, but
# it seems that the 2nd one (2) should be the most appropriate one.
#
# I'll use the following algorithm to find proper "region":
# If we want to find a forecast for the moment t_0 we should:
# 1. chceck if forecastStart <= t_0 <= forecastEnd
# 2. If yes, "rating" number R = (t0 - forecastStart) + (forecastEnd - t0) =
#    = forecastEnd-forecastStart, R --> 0.
# 3. If there is a forecast with the same R as before it wins
#    (i.e. forecast (3) is better than "general" forecast (1) @ 4 UTC and
#    forecast (4) is the best one @ 2 UTC.
#
# This algorithm does not use BECMG, PROB or TEMPO markers. 
        weather=None 
        R = 44640 # one month in minutes
        t0= dd*24*60+hh*60+mm
        for line in self.tafData:
            if "/" in line["period"].strip():
                l = line["period"].strip()
                fromDD, fromHH, toDD, toHH = (int(l[0:2]), int(l[2:4]), int(l[5:7]), int(l[7:9]))
                fs, fe = (fromDD*24*60+fromHH*60, toDD*24*60+toHH*60)
                if between(fs, t0, fe) and R >= abs(fe-fs):
                    weather = line
                    R = abs(fe-fs)
        return weather

    def compact(self, list):
# Quite useful, from http://mail.python.org/pipermail/python-list/2007-May/613113.html
        return " ".join(list).strip().replace("  "," ").split()

    def getWindSpeed(self):
        """
        Return the wind speed in meters per second.
        """
        if self.weather == None:
            return False

        wind =  self.weather["wind"].split()[1:]
       
        if "KT" in wind:
            u, c = ("KT", self.knots2mps)
        elif "MPS" in wind:
            u, c = ("MPS", 1)
        elif "KMH" in wind:
            u, c = ("KMH", self.kmh2mps)
        else:
            return None 

        if "G" in wind:
            windSpeed = [ int(round(int(wind[wind.index('G')-1])*c)),
                          int(round(int(wind[wind.index('G')+1])*c)) ]
        else:
            windSpeed = [ int(round(int(wind[wind.index(u)  -1])*c)) ]
        return windSpeed

    def getWindDirection(self):
        if self.weather == None:
            return False

        direction = self.weather["wind"].split()
        
        if 'V' in direction:
            return [ int(direction[0]),
                     int(wind[wind.index('V')-1]),
                     int(wind[wind.index('V')+1]) ]
        else:
            if direction<>[] and direction[0]<>"VRB":
                return ([int(direction[0])] or [None])
            else:
                return ["VRB"]

    def getVisibility(self): # in kilometers, only simple examples
        if self.weather == None:
            return False

        vis = self.weather["vis"].strip()

        try:
            if vis == 'P6SM' or vis=='9999':
                return 10 # 10 km or more
            elif 'SM' in vis :
                return int(vis[-3])*self.mi2km
            else:
                return int(vis)/1000.0 # or None
        except:
            pass
            return None


    def getTemperature(self):
        print "---> lib/taf.py: temperature not supported", self.weather["temp"]
        return None

    def getSkyConditions(self):
        if self.weather["skyCnd"] is None:
            return None
        
        clouds = ['OVC','BKN','SCT','FEW','SKC','NSC']
        for cloud in clouds:
            if cloud in self.weather["skyCnd"]:
                return cloud        

        return None
    
    def getPressure(self):
        print "---> lib/taf.py: pressure not supported", self.weather["press"]
        return None

    def getWeather(self):
        if self.weather == None:
            return False
        
        wx = ["","",""]
        rv = ""

        for w in self.weather["weather"].strip().split():
            wx = ["", "", ""]
            for k in self._WeatherConditions.keys():
                if k in w:
                    for elem in self._WeatherConditions[k]: 
                        if elem in w:
                            if self._WeatherConditions[k][elem] == "%":
                                print " ".join( ("---> lib/taf.py: couldn't interpret",elem,"in",self.weather["weather"].strip().split()) )
                            else:
                                if self._WeatherConditions[k][elem][1]!="":
                                    wx = self._WeatherConditions[k][elem]
                                elif self._WeatherConditions[k][elem][2]!="": 
                                    wx[2] = self._WeatherConditions[k][elem][2]
                                elif self._WeatherConditions[k][elem][0]!="" and self._WeatherConditions[k][elem][0] not in wx[0]:
                                    wx[0] = " ".join( (wx[0], self._WeatherConditions[k][elem][0]) )

            rv= " ".join( ( rv, " ".join( (wx) ) ) )
        return rv




#a="""EPWR 282300Z 2900/2909 31004KT 6000 BKN015
#         PROB40
#         TEMPO 2900/2903 3000 SHRA SCT002 BKN010CB
#         PROB30 2900/2907 1500 BR BKN001"""
#         
#myTAF = taf(taf=a)
#
## nie zapomnij o linii 199
#
#print myTAF.rawTAF
#
#for hh in range(0,4):
#    print myTAF.tafData
#    myTAF.changeMoment(29,hh,00)
#    print myTAF.weather
#    print "godzina ", (hh,0)
#    print "predkosc wiatru ", myTAF.getWindSpeed(), "m/s"
#    print "kierunek wiatru ", myTAF.getWindDirection(), " st."
#    print "widocznosc ", myTAF.getVisibility(), " km"
#    print "pogoda ", myTAF.getWeather()
#    print "---------------------------"
