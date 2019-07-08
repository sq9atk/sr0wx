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

import debug
import urllib2
import json
import datetime
import pytz
from config import world_weather_online as config

# TODO: need to find better place for this function
def wind_direction(dir, short=False):
    global lang
  
    _dir = ""
    if len(dir)==3 and short==True:
        dir = dir[1:3]
    for i in range(0,len(dir)-1):
        _dir = _dir + lang.directions[dir[i]][0]
    _dir = _dir + lang.directions[dir[-1]][1]

    return _dir

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

kmph2mps = lambda s: int(round(float(s)*(5.0/18.0)))

def getData(l):
    global lang
    lang = my_import(l+"."+l)
    rv = {'data':'', "needCTCSS":False, "source":"worldweatheronline"}

    REQ_URL='http://free.worldweatheronline.com/feed/weather.ashx?q={LAT},{LON}&format=json&num_of_days=2&key={API_KEY}'
    params = {'LAT':str(config.latitude), 'LON':str(config.longitude),\
        'API_KEY':config.api_key}

    weather= json.loads(urllib2.urlopen(REQ_URL.format(**params)).read())
    
    # `w`, `f0` and `f1` are parts of big weather dictionary; we have to unpack it for further
    # formatting.
    w = weather['data']['current_condition'][0]
    f0 = weather['data']['weather'][0]
    f1 = weather['data']['weather'][1]
    wc = lang.wwo_weather_codes

    # observation time gives us time in UTC, like '09:50 PM', but it gives no date.
    # Since we want it as a whole datetime, like '2011-12-28 21:50' we have to make
    # some transformations. We assume that the observation was made today, but if
    # resulting timestamp is in future we substract 1 day and convert it to
    # local time.

    #data = {
    OBSERVATION_TIME = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    OBSERVATION_TIME = ' '.join( (OBSERVATION_TIME, w['observation_time']) )
    OBSERVATION_TIME = datetime.datetime.strptime(OBSERVATION_TIME,'%Y-%m-%d %I:%M %p')
    if OBSERVATION_TIME>datetime.datetime.utcnow():
        OBSERVATION_TIME=OBSERVATION_TIME-datetime.timedelta(hours=24)
    utc = pytz.utc
    local=pytz.timezone('Europe/Warsaw')
    utc_dt = utc.localize(OBSERVATION_TIME)


    data = {
        'OBSERVATION_TIME':lang.readISODT(utc_dt.astimezone(local).strftime('%Y-%m-%d %H:%M:%S')),

        'CURRENT_CLOUDCOVER':lang.cardinal(int(w['cloudcover']),lang.percent),
        'CURRENT_HUMIDITY':lang.cardinal(int(w['humidity']), lang.percent),
        #'CURRENT_PRECIP_MM':float(w['precipMM']),
        'CURRENT_PRESSURE':lang.cardinal(int(w['pressure']), lang.hPa),
        'CURRENT_TEMP_C':lang.cardinal(int(w['temp_C']), lang.C),
        #'CURRENT_TEMP_F':int(w['temp_F']),
        'CURRENT_WEATHER':lang.removeDiacritics(wc[w['weatherCode']], remove_spaces=True),
        'CURRENT_WIND_DIR':wind_direction(w['winddir16Point'], short=True),
        'CURRENT_WIND_DIR_DEG':lang.cardinal(int(w['winddirDegree']), lang.deg),
        'CURRENT_WIND_SPEED_KMPH':lang.cardinal(int(w['windspeedKmph']),lang.kmPh),
        'CURRENT_WIND_SPEED_MPS':lang.cardinal(kmph2mps(int(w['windspeedKmph'])),lang.mPs),
        'CURRENT_WIND_SPEED_MI':lang.cardinal(int(w['windspeedMiles']),lang.MiPh),

        #'FCAST0_PRECIP_MM':float(f0['precipMM']),
        'FCAST0_TEMP_MIN_C':lang.cardinal(int(f0['tempMinC'])),
        'FCAST0_TEMP_MAX_C':lang.cardinal(int(f0['tempMaxC']),lang.C),
        #'FCAST0_TEMP_MIN_F':int(f0['tempMinF']),
        #'FCAST0_TEMP_MAX_F':int(f0['tempMaxF']),
        'FCAST0_WEATHER':lang.removeDiacritics(wc[f0['weatherCode']], remove_spaces=True),
        'FCAST0_WIND_DIR':wind_direction(f0['winddir16Point']),
        'FCAST0_WIND_DIR_DEG':lang.cardinal(int(f0['winddirDegree']),lang.deg),
        'FCAST0_WIND_SPEED_KMPH':lang.cardinal(int(f0['windspeedKmph']),lang.kmPh),
        'FCAST0_WIND_SPEED_MPS':lang.cardinal(kmph2mps(int(f0['windspeedKmph'])),lang.mPs),
        'FCAST0_WIND_SPEED_MI':int(f0['windspeedMiles']),

        #'FCAST1_PRECIP_MM':float(f1['precipMM']),
        'FCAST1_TEMP_MIN_C':lang.cardinal(int(f1['tempMinC'])),
        'FCAST1_TEMP_MAX_C':lang.cardinal(int(f1['tempMaxC']),lang.C),
        #'FCAST1_TEMP_MIN_F':int(f1['tempMinF']),
        #'FCAST1_TEMP_MAX_F':int(f1['tempMaxF']),
        'FCAST1_WEATHER':lang.removeDiacritics(wc[f1['weatherCode']], remove_spaces=True),
        'FCAST1_WIND_DIR':wind_direction(f1['winddir16Point']),
        'FCAST1_WIND_DIR_DEG':lang.cardinal(int(f1['winddirDegree']),lang.deg),
        'FCAST1_WIND_SPEED_KMPH':lang.cardinal(int(f1['windspeedKmph']),lang.kmPh),
        'FCAST1_WIND_SPEED_MPS':lang.cardinal(kmph2mps(int(f1['windspeedKmph'])),lang.mPs),
        'FCAST1_WIND_SPEED_MI':int(f1['windspeedMiles']),
    }

    rv['data']=lang.removeDiacritics(config.template.format(**data))

    return rv

