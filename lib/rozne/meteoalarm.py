#!/usr/env/python -tt
# -*- encoding=utf8 -*-
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

import re
import urllib

from config import meteoalarm as config
lang=None

def downloadFile(url):
    webFile = urllib.urlopen(url)
    return webFile.read()

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def getData(l):
    global lang
    lang = my_import(l+"."+l)

    data = {"data":"", "needCTCSS":False, "debug":None, "allOK":True,
            "source":"meteoalarm_eu"}

    today=tomorrow=""
    if config.showToday == True:
        today    = getAwareness(config.region, tomorrow=False)
    if config.showTomorrow == True:
        tomorrow = getAwareness(config.region, tomorrow=True)

    if today== "" and tomorrow== "":
        #data["data"] = " ".join( (lang.meteoalarmNoAwareness, lang.meteoalarmRegions[config.region]) )
        pass # silence is golden
    elif today!= "" and tomorrow=="":
        data["data"] =  " ".join( (lang.meteoalarmAwareness, lang.meteoalarmRegions[config.region], lang.today, today) )
        data["needCTCSS"] = True
    elif today== "" and tomorrow!="":
        data["data"] =  " ".join( (lang.meteoalarmAwareness, lang.meteoalarmRegions[config.region], lang.tomorrow, tomorrow) )
        data["needCTCSS"]= True
    else:
        data["data"] = " ".join( (lang.meteoalarmAwareness, lang.meteoalarmRegions[config.region], lang.today, today, lang.tomorrow,tomorrow) )
        data["needCTCSS"]= True

    return data

def getAwareness(region, tomorrow=False):
# tommorow = False -- awareness for today
# tommorow = True  -- awareness for tommorow
    r =   re.compile('pictures/aw(\d[01]?)([0234]).jpg')
    url = "http://www.meteoalarm.eu/index3.php?area=%s&day=%s&lang=EN"\ %(str(region),str(int(tomorrow)))


    a = ""

    for line in downloadFile(url).split('\n'):
        f = r.findall(line)
        if len(f) is not 0 and int(f[0][0])!=0:
            a = " ".join( (a, lang.meteoalarmAwarenesses[int(f[0][0])],\
                lang.meteoalarmAwarenessLevel, lang.meteoalarmAwarenessLvl[int(f[0][1])]) )

    return a
