# -*- coding: utf-8 -*-
#
#   Copyright 2009-2014 Michal Sadowski (sq6jnx at hamradio dot pl)
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

from six import u
import datetime
from functools import wraps

# #################
# CAUTION!
# DIRTY HACK BELOW
# #################
#
# for now `pyliczba` is not a Python module in terms like you can `pip` it or
# something. It's even impossibru to import it, because it does not have an
# `__init__  file. And the main file isn't even called `pyliczba`!
#
# ... so we create one...

import os

pyliczba_init = os.sep.join(('pl_google', 'pyliczba', '__init__.py'))
with open(pyliczba_init, 'w') as f:
    f.write("from .kwotaslownie import *")

# It works!

import pyliczba

def rmv_pl_chars(string):
    return ''.join([i if ord(i) < 128 else '_' for i in string]).lower()
        
def ra(value):
    return value\
        .replace(u("ą"), "a").replace(u("Ą"), "a")\
        .replace(u("ć"), "c").replace(u("Ć"), "c")\
        .replace(u("ę"), "e").replace(u("Ę"), "e")\
        .replace(u("ł"), "l").replace(u("Ł"), "l")\
        .replace(u("ń"), "n").replace(u("Ń"), "n")\
        .replace(u("ó"), "o").replace(u("Ó"), "o")\
        .replace(u("ś"), "s").replace(u("Ś"), "s")\
        .replace(u("ź"), "z").replace(u("Ź"), "z")\
        .replace(u("ż"), "z").replace(u("Ż"), "z")\
        .lower()

def remove_accents(function):
    """unicodedata.normalize() doesn't work with ł and Ł"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        return ra(function(*args, **kwargs))
    return wrapper

def _(text):
    return text.replace(' ', '_')


class SR0WXLanguage(object):
    def __init__(self):
        """Nothing here for now."""
        pass


class PLGoogle(SR0WXLanguage):
    def __init__(self):
        pass

    @remove_accents
    def read_number(self, value, units=None):
        """Converts numbers to text."""
        if units is None:
            retval = pyliczba.lslownie(abs(value))
        else:
            retval = pyliczba.cosslownie(abs(value), units)

        if retval.startswith(u("jeden tysiąc")):
            retval = retval.replace(u("jeden tysiąc"), u("tysiąc"))
        if value < 0:
            retval = " ".join(("minus", retval))
        return retval

    @remove_accents
    def read_pressure(self, value):
        hPa = ["hektopaskal", "hektopaskale", "hektopaskali"]
        return self.read_number(value, hPa)
     
    @remove_accents
    def read_distance(self, value):
        hPa = ["kilometr", "kilometry", "kilometrow"]
        return self.read_number(value, hPa)
     

    @remove_accents
    def read_percent(self, value):
        percent = ["procent", "procent", "procent"]
        return self.read_number(value, percent)

    @remove_accents
    def read_temperature(self, value):
        C = [_(u("stopień Celsjusza")), _("stopnie Celsjusza"), _("stopni Celsjusza")]
        return read_number(value, C)

    @remove_accents
    def read_speed(self, no, unit='mps'):
        units = {
            'mps': [
                    _(u("metr na sekundę")), 
                    _(u("metry na sekundę")),
                    _(u("metrów na sekundę"))
                ],
            'kmph': [_(u("kilometr na godzinę")), _(u("kilometry na godzinę")),_(u("kilometrów na godzinę"))]
        }
        return read_number(no, units[unit])

    
    @remove_accents
    def read_degrees(self, value):
        deg = [u("stopień"), u("stopnie"), u("stopni")]
        return read_number(value, deg)

    
    @remove_accents
    def read_micrograms(self, value):
        deg = [
                u("mikrogram na_metr_szes_cienny"),
                u("mikrogramy na_metr_szes_cienny"), 
                u("mikrogramo_w na_metr_szes_cienny"), 
            ]
        return read_number(value, deg)

    @remove_accents
    def read_decimal(self, value):
        deg100 = [
                u("setna"),
                u("setne"), 
                u("setnych"), 
            ]
            
        deg10 = [
                u("dziesia_ta"),
                u("dziesia_te"), 
                u("dziesia_tych"), 
            ]
        if value >= 10:
            return read_number(value, deg100)
        else:
            return read_number(value, deg10)
    
    @remove_accents
    def read_direction(self, value, short=False):
        directions = {
            "N": (u("północno"),   u("północny")),
            "E": (u("wschodnio"),  u("wschodni")),
            "W": (u("zachodnio"),  u("zachodni")),
            "S": (u("południowo"), u("południowy")),
        }
        if short:
            value = value[-2:]
        return '-'.join([directions[d][0 if i < 0 else 1]
                         for i, d in enumerate(value, -len(value)+1)])


    @remove_accents
    def read_datetime(self, value, out_fmt, in_fmt=None):

        if type(value) != datetime.datetime and in_fmt is not None:
            value = datetime.datetime.strptime(value, in_fmt)
        elif type(value) == datetime.datetime:
            pass
        else:
            raise TypeError('Either datetime must be supplied or both '
                            'value and in_fmt')

        MONTHS = [u(""),
                  u("stycznia"), u("lutego"), u("marca"), u("kwietnia"), u("maja"),
                  u("czerwca"), u("lipca"), u("sierpnia"), u("września"),
                  u("października"), u("listopada"), u("grudnia"),
        ]

        DAYS_N0 = [u(""), u(""), u("dwudziestego"), u("trzydziestego"),]
        DAYS_N = [u(""),
                  u("pierwszego"), u("drugiego"), u("trzeciego"), u("czwartego"),
                  u("piątego"), u("szóstego"), u("siódmego"), u("ósmego"),
                  u("dziewiątego"), u("dziesiątego"), u("jedenastego"),
                  u("dwunastego"), u("trzynastego"), u("czternastego"),
                  u("piętnastego"), u("szesnastego"), u("siedemnastego"),
                  u("osiemnastego"), u("dziewiętnastego"),
        ]
        HOURS = [u("zero"), u("pierwsza"), u("druga"), u("trzecia"), u("czwarta"),
                 u("piąta"), u("szósta"), u("siódma"), u("ósma"), u("dziewiąta"),
                 u("dziesiąta"), u("jedenasta"), u("dwunasta"), u("trzynasta"),
                 u("czternasta"), u("piętnasta"), u("szesnasta"),
                 u("siedemnasta"), u("osiemnasta"), u("dziewiętnasta"),
                 u("dwudziesta"),
        ]


        _, tm_mon, tm_mday, tm_hour, tm_min, _, _, _, _ = value.timetuple()
        retval = []
        for word in out_fmt.split(" "):
            if word == '%d':  # Day of the month
                if tm_mday <= 20:
                    retval.append(DAYS_N[tm_mday])
                else:
                    retval.append(DAYS_N0[tm_mday //10])
                    retval.append(DAYS_N[tm_mday % 10])
            elif word == '%B':  # Month as locale’s full name
                retval.append(MONTHS[tm_mon])
            elif word == '%H':  # Hour (24-hour clock) as a decimal number
                if tm_hour <= 20:
                    retval.append(HOURS[tm_hour])
                elif tm_hour > 20:
                    retval.append(HOURS[20])
                    retval.append(HOURS[tm_hour - 20])
            elif word == '%M':  # Minute as a decimal number
                if tm_min == 0:
                    retval.append(u('zero-zero'))
                else:
                    retval.append(read_number(tm_min))
            elif word.startswith('%'):
                raise ValueError("Token %s' is not supported!", word)
            else:
                retval.append(word)
        return ' '.join((w for w in retval if w != ''))

    @remove_accents
    def read_callsign(self, value):
        # literowanie polskie wg. "Krótkofalarstwo i radiokomunikacja - poradnik",
        # Łukasz Komsta SQ8QED, Wydawnictwa Komunikacji i Łączności Warszawa, 2001,
        # str. 130
        LETTERS = {
            'a': u('adam'), 'b': u('barbara'), 'c': u('celina'), 'd': u('dorota'),
            'e': u('edward'), 'f': u('franciszek'), 'g': u('gustaw'),
            'h': u('henryk'), 'i': u('irena'), 'j': u('józef'), 'k': u('karol'),
            'l': u('ludwik'), 'm': u('marek'), 'n': u('natalia'), 'o': u('olga'),
            'p': u('paweł'), 'q': u('quebec'), 'r': u('roman'), 's': u('stefan'),
            't': u('tadeusz'), 'u': u('urszula'), 'v': u('violetta'),
            'w': u('wacław'), 'x': u('xawery'), 'y': u('ypsilon'), 'z': u('zygmunt'),
            '/': u('łamane'),
        }
        retval = []
        for char in value.lower():
            try:
                retval.append(LETTERS[char])
            except KeyError:
                try:
                    retval.append(read_number(int(char)))
                except ValueError:
                    raise ValueError("\"%s\" is not a element of callsign", char)
        return ' '.join(retval)


# ##########################################
#
# module dependant words
# #############################################


# World Weather Online

wwo_weather_codes = {
    '113': _(ra(u('bezchmurnie'))),                                      # Clear/Sunny
    '116': _(ra(u('częściowe zachmurzenie'))),                           # Partly Cloudy
    '119': _(ra(u('pochmurno'))),                                        # Cloudy
    '122': _(ra(u('zachmurzenie całkowite'))),                           # Overcast
    '143': _(ra(u('zamglenia'))),                                        # Mist
    '176': _(ra(u('lokalne przelotne opady deszczu'))),                  # Patchy rain nearby
    '179': _(ra(u('śnieg'))),                                            # Patchy snow nearby
    '182': _(ra(u('śnieg z deszczem'))),                                 # Patchy sleet nearby
    '185': _(ra(u('lokalna przelotna marznąca mżawka'))),                # Patchy freezing drizzle nearby
    '200': _(ra(u('lokalne burze'))),                                    # Thundery outbreaks in nearby
    '227': _(ra(u('zamieć śnieżna'))),                                   # Blowing snow
    '230': _(ra(u('zamieć śnieżna'))),                                   # Blizzard
    '248': _(ra(u('mgła'))),                                             # Fog
    '260': _(ra(u('marznąca mgła'))),                                    # Freezing fog
    '263': _(ra(u('mżawka'))),                                           # Patchy light drizzle
    '266': _(ra(u('mżawka'))),                                           # Light drizzle
    '281': _(ra(u('marznąca mżawka'))),                                  # Freezing drizzle
    '284': _(ra(u('marznąca mżawka'))),                                  # Heavy freezing drizzle
    '293': _(ra(u('lokalny słaby deszcz'))),                             # Patchy light rain
    '296': _(ra(u('słaby deszcz'))),                                     # Light rain
    '299': _(ra(u('przelotne opady deszczu'))),                          # Moderate rain at times
    '302': _(ra(u('umiarkowane opady deszczu'))),                        # Moderate rain
    '305': _(ra(u('przelotne ulewy'))),                                  # Heavy rain at times
    '308': _(ra(u('ulewy'))),                                            # Heavy rain
    '311': _(ra(u('słabe opady marznącego deszczu'))),                   # Light freezing rain
    '314': _(ra(u('umiarkowane opady marznącego deszczu'))),             # Moderate or Heavy freezing rain
    '317': _(ra(u('słabe opady śniegu z deszczem'))),                    # Light sleet
    '320': _(ra(u('umiarkowane lub ciężkie opady śniegu z deszczem'))),  # Moderate or heavy sleet
    '323': _(ra(u('słabe opady śniegu'))),                               # Patchy light snow
    '326': _(ra(u('słabe opady śniegu'))),                               # Light snow
    '329': _(ra(u('umiarkowane opady śniegu'))),                         # Patchy moderate snow
    '332': _(ra(u('umiarkowane opady śniegu'))),                         # Moderate snow
    '335': _(ra(u('opady śniegu'))),                                     # Patchy heavy snow
    '338': _(ra(u('intensywne_opady_sniegu'))),                          # Heavy snow
    '350': _(ra(u('grad'))),                                             # Ice pellets
    '353': _(ra(u('słabe przelotne opady deszczu'))),                    # Light rain shower
    '356': _(ra(u('przelotne opady deszczu'))),                          # Moderate or heavy rain shower
    '359': _(ra(u('ulewny deszcz'))),                                    # Torrential rain shower
    '362': _(ra(u('słabe opady śniegu z deszczem'))),                    # Light sleet showers
    '365': _(ra(u('umiarkowane opady śniegu z deszczem'))),              # Moderate or heavy sleet showers
    '368': _(ra(u('słabe opady śniegu'))),                               # Light snow showers
    '371': _(ra(u('umiarkowane opady śniegu'))),                         # Moderate or heavy snow showers
    '374': _(ra(u('słabe opady śniegu ziarnistego'))),                   # Light showers of ice pellets
    '377': _(ra(u('umiarkowane opady śniegu ziarnistego'))),             # Moderate or heavy showers of ice pellets
    '386': _(ra(u('burza'))),                                            # Patchy light rain in area with thunder
    '389': _(ra(u('burza'))),                                            # Moderate or heavy rain in area with thunder
    '392': _(ra(u('burza śnieżna'))),                                    # Patchy light snow in area with thunder
    '395': _(ra(u('burza śnieżna'))),                                    # Moderate or heavy snow in area with thunder
}


# to be removed from code
source = 'zrodlo'

pl = PLGoogle()

read_number = pl.read_number
read_pressure = pl.read_pressure
read_distance = pl.read_distance
read_percent = pl.read_percent
read_temperature = pl.read_temperature
read_speed = pl.read_speed
read_degrees = pl.read_degrees
read_micrograms = pl.read_micrograms
read_decimal = pl.read_decimal
read_direction = pl.read_direction
read_datetime = pl.read_datetime
read_callsign = pl.read_callsign

