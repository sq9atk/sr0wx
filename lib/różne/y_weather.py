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

fake_gettext = lambda(s): s
_ = fake_gettext

from config import y_weather as config

# For debugging purposes:

import debug
import urllib2

lang = None

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

# Taken from http://developer.yahoo.com/python/python-xml.html (SLIGHTLY modified)
# simple and elegant, but I HATE XML!

import urllib
from xml.dom import minidom

import datetime

format_date_time = lambda s: datetime.datetime.strptime(s, '%a, %d %b %Y %I:%M %p %Z')
format_date= lambda s: datetime.datetime.strptime(s, '%d %b %Y')
kmph2mps = lambda s: round(float(s)*(5.0/18.0))

def weather_for_zip(zip_code):
    WEATHER_URL = 'http://weather.yahooapis.com/forecastrss?w=%s&u=c'
    #WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss?p=%s'
    WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'

    url = WEATHER_URL % zip_code
    dom = minidom.parse(urllib.urlopen(url))
    forecasts = []
    for node in dom.getElementsByTagNameNS(WEATHER_NS, 'forecast'):
        forecasts.append({
            'date': format_date(node.getAttribute('date')),
            'low': int(node.getAttribute('low')),
            'high': int(node.getAttribute('high')),
            #'condition': node.getAttribute('text')
            'condition': int(node.getAttribute('code'))
        })
    ycondition = dom.getElementsByTagNameNS(WEATHER_NS, 'condition')[0]
    wind = dom.getElementsByTagNameNS(WEATHER_NS, 'wind')[0]
    atmosphere = dom.getElementsByTagNameNS(WEATHER_NS, 'atmosphere')[0]

    return {
        #'current_condition': ycondition.getAttribute('text'),
        'pub_date': format_date_time(dom.getElementsByTagName('pubDate')[0].firstChild.data),
        'current_conditions': int(ycondition.getAttribute('code')),
        'current_temp': int(ycondition.getAttribute('temp')),
	'wind_chill': int(wind.getAttribute('chill')),
        'wind_direction': int(wind.getAttribute('direction')),
        'wind_speed': float(kmph2mps(wind.getAttribute('speed'))),
        'humidity': atmosphere.getAttribute('humidity'),
        'visibility': atmosphere.getAttribute('visibility'),
        'pressure': float(atmosphere.getAttribute('pressure')),
        'tendention': atmosphere.getAttribute('rising'),
        'forecasts': forecasts,
        #'title': dom.getElementsByTagName('title')[0].firstChild.data
    }


def getData(l):
    rv = {'data':'', "needCTCSS":False,"source":"y_weather" }

    lang = my_import(l+"."+l)
    conditions = lang.y_weather.conditions

    w = weather_for_zip(config.zipcode)

    data = {
	'PUB_DATE_HOUR':  lang.readISODT(str(w['pub_date'])),
	'CURR_TEMP': lang.cardinal(w['current_temp'], lang.C),
	'HUMIDITY': lang.cardinal(int(float(w['humidity'])), lang.percent), 
	'CURRENT_CONDITION': conditions[str(w['current_conditions'])].replace(' ','_'), 
	'WIND_DIR_NEWS': '', 
	'WIN_DIR_DEG': lang.cardinal(w['wind_direction'], lang.deg),
	'WIND_SPEED': lang.cardinal(int(w['wind_speed']), lang.mPs),
	'VISIBILITY_KM': '', #lang.cardinal(w['visibility'], lang.km),                     '' =>  None == nieograniczona
	'PRESSURE': lang.cardinal(int(w['pressure']), lang.hPa),
	'PRESSURE_TENDENTION': lang.tendention[int(w['tendention'])],
	'TEMP_WIND_CHILL': lang.cardinal(w['wind_chill'], lang.C),

	'FORECAST0_CONDITION': '',
	'FORECAST0_MIN_TEMP': lang.cardinal(w['forecasts'][0]['low'], lang.C),
	'FORECAST0_MIN_TEMP_SHORT': lang.cardinal(w['forecasts'][0]['low']),
	'FORECAST0_MAX_TEMP': lang.cardinal(w['forecasts'][0]['high'], lang.C),

	'FORECAST1_CONDITION': '',
	'FORECAST1_MIN_TEMP': lang.cardinal(w['forecasts'][1]['low'], lang.C),
	'FORECAST1_MIN_TEMP_SHORT': lang.cardinal(w['forecasts'][1]['low']),
	'FORECAST1_MAX_TEMP': lang.cardinal(w['forecasts'][1]['high'], lang.C),
}

    rv['data']=lang.removeDiacritics(config.template.format(**data))
    return rv
