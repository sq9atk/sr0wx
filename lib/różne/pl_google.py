# -*- coding: utf-8 -*-
# 
#   Copyright 2009-2012 Michal Sadowski (sq6jnx at hamradio dot pl)
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
 
# *********
# pl_google/pl_google.py
# *********
#
# This file defines language dependent functions and variables. Probably
# this is the most important file in whole package.
#
# ============
# Requirements
# ============
#
# This package *may* import some other packages, it is up to you (and your
# needs).
#
# BUT: this packahe **must** define the following functions:
# * ``direction()`` which "translates" direction given by letters into
#    its word representation
# * ``removeDiacritics()`` which removes diacritics
# * ``readISODT()`` "translates" date and time into its word representation
# * ``cardinal()``  which changes numbers into words (1 -> one)
#
# As you probably can see all of these functions are language-dependant.
#
# ======================
# Implementation example
# ======================
#
# Here is implementation example for Polish language. Polish is interresting
# because it uses diacritics and 7 (seven) gramatical cases[#]_ (among many
# other features ;)
#
# .. [*] http://pl.wikipedia.org/wiki/Przypadek#Przypadki_w_j.C4.99zyku_polskim
#
# There *may* be some issues with diacritics because there are many
# implementations [#]. For example, Windows uses its own coding system while
# Linux uses UTF-8 (I think). And, when moving files (which are named with
# diacritics) from one platform to another results may (will) be
# unexpectable.
#
# .. [#] http://pl.wikipedia.org/wiki/Kodowanie_polskich_znak%C3%B3w
#
# =====================
# Polish dictionary
# =====================
#
# Concept: to make things clear, easy to debug and to
# internationalize. Program *doesn't use words* but *filenames*.
# So, if somewhere in programme variable's value or function returnes 
# ie. *windy* it should be regarded as a *filename*, ``windy.ogg``.
#
# Beware too short words, it will be like machine gun rapid fire or
# will sound like a cyborg from old, cheap sci-fi movie. IMO the good way
# is to record longer phrases, like *"the temperature is"*, save it as
# ``the_temperature_is.ogg`` and use it's filename (``the_temperature_is``)
# as a return value.
#
# This dictionary is used by all SR0WX modules.

fake_gettext = lambda(s): s
_ = fake_gettext

# Units and grammar cases
hrs = ["","godziny","godzin"]
hPa = ["hektopaskal", "hektopaskale", "hektopaskali"]
percent = [u"procent",u"procent",u"procent"]
mPs    = ["metr_na_sekunde", "metry_na_sekunde", "metrow_na_sekunde"]
kmPh   = ["kilometr_na_godzine", "kilometry_na_godzine", "kilometrow_na_godzine"]
MiPh   = ["", "", ""] # miles per hour -- not used
windStrength  = "sila_wiatru"
deg = [u"stopien","stopnie","stopni"]
C   = ["stopien_celsjusza", "stopnie_celsjusza", "stopni_celsjusza"]
km  = ["kilometr", "kilometry", u"kilometrow"]
mns = ["minuta","minuty","minut"]
tendention = ['tendencja_spadkowa','', 'tendencja_wzrostowa']


# We need also local names for directions to convert two- or three letters
# long wind direction into words (first is used as prefix, second as suffix):
directions = { "N": ("północno ",   "północny"),
               "E": ("wschodnio ",  "wschodni"),
               "W": ("zachodnio ",  "zachodni"),
               "S": ("południowo ", "południowy") }

# numbers
jednostkiM = [u""] + u"jeden dwa trzy cztery pięć sześć siedem osiem dziewięć".split()
jednostkiF = [u""] + u"jedną dwie trzy cztery pięć sześć siedem osiem dziewięć".split()
dziesiatki = [u""] + u"""dziesięć dwadzieścia  trzydzieści czterdzieści
     pięćdziesiąt sześćdziesiąt siedemdziesiąt osiemdziesiąt dziewięćdziesiąt""".split()
nastki = u"""dziesięć jedenaście dwanaście trzynaście czternaście piętnaście
        szesnaście siedemnaście osiemnaście dziewiętnaście""".split()
setki = [u""]+ u"""sto dwieście trzysta czterysta pięćset sześćset siedemset osiemset
              dziewięćset""".split()

ws=u"""x x x
   tysiąc tysiące tysięcy
   milion miliony milionów
   miliard miliardy miliardów
   bilion biliony bilionów"""
wielkie = [ l.split() for l in ws.split('\n') ]

##zlotowki=u"""złoty złote złotych""".split()
##grosze=u"""grosz grosze groszy""".split()

# There are also some functions, by dowgird, so I haven't even looked into
# them.

def _slownie3cyfry(liczba, plec='M'):
    if plec=='M':
        jednostki = jednostkiM
    else:
        jednostki = jednostkiF

    je = liczba % 10
    dz = (liczba//10) % 10
    se = (liczba//100) % 10
    slowa=[]

    if se>0:
        slowa.append(setki[se])
    if dz==1:
        slowa.append(nastki[je])
    else:
        if dz>0:
            slowa.append(dziesiatki[dz])
        if je>0:
            slowa.append(jednostki[je])
    retval = " ".join(slowa)
    return retval

def _przypadek(liczba):
    je = liczba % 10
    dz = (liczba//10)  % 10

    if liczba == 1:
        typ = 0       #jeden tysiąc"
    elif dz==1 and je>1:  # naście tysięcy
        typ = 2
    elif  2<=je<=4:
        typ = 1       # [k-dziesiąt/set] [dwa/trzy/czery] tysiące
    else:
        typ = 2       # x tysięcy

    return typ

def lslownie(liczba, plec='M'):
    """Liczba całkowita słownie"""
    trojki = []
    if liczba==0:
        return u'zero'
    while liczba>0:
        trojki.append(liczba % 1000)
        liczba = liczba // 1000
    slowa = []
    for i,n in enumerate(trojki):
        if n>0:
            if i>0:
                p = _przypadek(n)
                w = wielkie[i][p]
                slowa.append(_slownie3cyfry(n, plec)+u" "+w)
            else:
                slowa.append(_slownie3cyfry(n, plec))
    slowa.reverse()
    return ' '.join(slowa)

def cosslownie(liczba,cos, plec='M'):
    """Słownie "ileś cosiów"

    liczba - int
    cos - tablica przypadków [coś, cosie, cosiów]"""
    #print liczba
    #print cos[_przypadek(liczba)]
    return lslownie(liczba, plec)+" " + cos[_przypadek(liczba)]

##def kwotaslownie(liczba, format = 0):
##    """Słownie złotych, groszy.
##
##    liczba - float, liczba złotych z groszami po przecinku
##    format - jesli 0, to grosze w postaci xx/100, słownie w p. przypadku
##    """
##    lzlotych = int(liczba)
##    lgroszy = int (liczba * 100 + 0.5 ) % 100
##    if format!=0:
##        groszslownie = cosslownie(lgroszy, grosze)
##    else:
##        groszslownie = '%d/100' % lgroszy
##    return cosslownie(lzlotych, przypzl) + u" " +  groszslownie
##

# As you remember, ``cardinal()`` must be defined, this is the function which
# will be used by SR0WX modules. This functions was also written by dowgrid,
# modified by me. (Is function's name proper?)
def cardinal(no, units=[u"",u"",u""], gender='M'):
    """Zamienia liczbę zapisaną cyframi na zapis słowny, opcjonalnie z jednostkami
w odpowiednim przypadku. Obsługuje liczby ujemne."""
    if no<0:
        return (u"minus " + cosslownie(-no, units, plec=gender)).replace(u"jeden tysiąc", u"tysiąc",1).encode("utf-8")
    else:
        return cosslownie(no, units, plec=gender).replace(u"jeden tysiąc", u"tysiąc",1).encode("utf-8")

# This one tiny simply removes diactrics (lower case only). This function
# must be defined even if your language doesn't use diactrics (like English),
# for example as a simple ``return text``.
def removeDiacritics(text, remove_spaces=False):
    rv= text.replace("ą","a").replace("ć","c").replace("ę","e").\
        replace("ł","l").replace("ń","n").replace("ó","o").replace("ś","s").\
        replace("ź","z").replace("ż","z")
    if remove_spaces==False:
        return rv
    else:
        return rv.replace(' ','_')

# The last one changes ISO structured date time into word representation.
# It doesn't return year value.
def readISODT(ISODT):
    _rv=() # return value
    y,m,d,hh,mm,ss= ( int(ISODT[0:4]),   int(ISODT[5:7]),   int(ISODT[8:10]),
                      int(ISODT[11:13]), int(ISODT[14:16]), int(ISODT[17:19]) )

    # miesiąc
    _M = ["","stycznia","lutego","marca","kwietnia","maja","czerwca","lipca",
         "sierpnia","września","października","listopada","grudnia"]
    Mslownie = _M[m]
    # dzień
    _j = ["","pierwszego","drugiego","trzeciego","czwartego","piątego","szóstego",
        "siódmego","ósmego","dziewiątego","dziesiątego","jedenastego",
        "dwunastego","trzynastego","czternastego","piętnastego","szesnastego",
        "siedemnastego","osiemnastego","dziewiętnastego"]
    _d = ["","","dwudziestego","trzydziestego"]

    if d<20: Dslownie = _j[d]
    else: Dslownie = " ".join( (_d[d/10], _j[d%10]) )

    _j = ["zero","pierwsza","druga","trzecia","czwarta","piąta","szósta",
          "siódma","ósma","dziewiąta","dziesiąta","jedenasta","dwunasta",
          "trzynasta","czternasta","piętnasta","szesnasta","siedemnasta",
          "osiemnasta","dziewiętnasta"]

    if hh<20: HHslownie = _j[hh]
    elif hh==20: HHslownie="dwudziesta"
    else: HHslownie = " ".join( ("dwudziesta", _j[hh%10]) )

    MMslownie = cardinal(mm).replace("zero","zero_zero")

    #return " ".join( (Dslownie, Mslownie, "godzina", HHslownie, MMslownie) )
    return " ".join( (Dslownie, Mslownie, "z_godziny", HHslownie, MMslownie) )

def readISODate(ISODate):
    _rv=() # return value
    y,m,d,hh,mm,ss= ( int(ISODate[0:4]),   int(ISODate[5:7]),   int(ISODate[8:10]),
                      int(ISODate[11:13]), int(ISODate[14:16]), int(ISODate[17:19]) )

    # miesiąc
    _M = ["","stycznia","lutego","marca","kwietnia","maja","czerwca","lipca",
         "sierpnia","września","października","listopada","grudnia"]
    Mslownie = _M[m]
    # dzień
    _j = ["","pierwszego","drugiego","trzeciego","czwartego","piątego","szóstego",
        "siódmego","ósmego","dziewiątego","dziesiątego","jedenastego",
        "dwunastego","trzynastego","czternastego","piętnastego","szesnastego",
        "siedemnastego","osiemnastego","dziewiętnastego"]
    _d = ["","","dwudziestego","trzydziestego"]

    if d<20: Dslownie = _j[d]
    else: Dslownie = " ".join( (_d[d/10], _j[d%10]) )

    return " ".join( (Dslownie, Mslownie) )


def readHour(dt):
    return removeDiacritics(readISODT('0000-00-00 '+str(dt.hour).rjust(2, '0')+':'+str(dt.minute).rjust(2, '0')+':00'))

def readHourLen(hour):
    ss = hour.seconds
    hh = ss/3600
    mm = (ss-hh*3600)/60
    return removeDiacritics(" ".join( (cardinal(hh, hrs, gender='F'), cardinal(mm, mns, gender='F')) ))

def readCallsign(call):
    rv = ''
    for c in call.lower():
        if c in 'abcdefghijklmnopqrstuvwxyz':
            rv=rv+c+' '
        elif c in '0123456789':
            rv=rv+removeDiacritics(cardinal(int(c)))+' '
        elif c=='/':
            rv=rv+'lamane '
    
    return rv

def readFraction(number, precision):
    try:
        integer, fraction = str(round(number,precision)).split('.')
    except TypeError:
        return None
        pass
    
    rv= ' '.join( (cardinal(int(integer)), comma) )
    
    while fraction[0]=='0':
        rv=' '.join( (rv, cardinal(0)), )
        fraction.pop(0)
        
    rv=' '.join( (rv, cardinal(int(fraction)),) )
    return rv

# ##########################################
#
# module dependant words
# #############################################

class m:
    pass

y_weather = m()
y_weather.conditions = {
    '0':  'tornado',                     # tornado
    '1':  'burza tropikalna',            # tropical storm
    '2':  'huragan',                     # hurricane
    '3':  'silne burze',                 # severe thunderstorms
    '4':  'burza',                       # thunderstorms
    '5':  'deszcz ze śniegiem',          # mixed rain and snow
    '6':  'deszcz i deszcz ze śniegiem', # mixed rain and sleet
    '7':  'śnieg i deszcz ze śniegiem',  # mixed snow and sleet
    '8':  'marznąca mżawka',             # freezing drizzle
    '9':  'mżawka',                      # drizzle
    '10': 'marznący deszcz',             # freezing rain
    '11': 'deszcz',                      # showers
    '12': 'deszcz',                      # showers
    '13': 'śnieg',                       # snow flurries
    '14': 'słaby śnieg',                 # light snow showers
    '15': 'zawieje śnieżne',             # blowing snow
    '16': 'śnieg',                       # snow
    '17': 'grad',                        # hail
    '18': 'deszcz ze śniegiem',          # sleet
    '19': 'pył',                         # dust
    '20': 'zamglenia',                   # foggy
    '21': 'mgła',                        # haze
    '22': 'smog',                        # smoky
    '23': 'silny wiatr',                 # blustery
    '24': 'wietrznie',                   # windy
    '25': 'przymrozki',                  # cold
    '26': 'pochmurno',                   # cloudy
    '27': 'pochmurno',                   # mostly cloudy (night)
    '28': 'pochmurno',                   # mostly cloudy (day)
    '29': 'częściowe zachmurzenie',      # partly cloudy (night)
    '30': 'częściowe zachmurzenie',      # partly cloudy (day)
    '31': 'bezchmurnie',                 # clear (night)
    '32': 'bezchmurnie',                 # sunny
    '33': 'słabe zachmurzenie',          # fair (night)
    '34': 'słabe zachmurzenie',          # fair (day)
    '35': 'deszcz i grad',               # mixed rain and hail
    '36': 'wysokie temperatury',         # hot
    '37': 'burza',                       # isolated thunderstorms
    '38': 'burza',                       # scattered thunderstorms
    '39': 'burza',                       # scattered thunderstorms
    '40': 'przelotne opady',             # scattered showers
    '41': 'intensywne opady śniegu',     # heavy snow
    '42': 'przelotne opady śniegu',      # scattered snow showers
    '43': 'intensywne opady śniegu',     # heavy snow
    '44': 'częściowe zachmurzenie',      # partly cloudy
    '45': 'burza',                       # thundershowers
    '46': 'śnieg',                       # snow showers
    '47': 'burza',                       # isolated thundershowers
    '3200': '',                          # not available
}


# These dictionaries are used by meteoalarm module.
meteoalarmAwarenesses = [
    "",
    "silny_wiatr",
    "snieg_lub_oblodzenie",
    "burze",
    "mgly",
    "wysokie_temperatury",
    "niskie_temperatury",
    "zjawiska_strefy_brzegowej",
    "pozary_lasow",
    "lawiny",
    "intensywne_opady_deszczu",
    "inne_zagrozenia"]
meteoalarmAwarenessLvl = [
    "nieokreslony",
    "",
    "niski",
    "sredni",
    "wysoki"]

meteoalarmAwarenessLevel = "poziom_zagrozenia"
meteoalarmRegions = {
    'PL001':"mazowieckiego", 
    'PL002':"lubuskiego", 
    'PL003':"zachodniopomorskiego",
    'PL004':"pomorskiego", 
    'PL005':"dolnoslaskiego", 
    'PL006':"opolskiego",
    'PL007':"śląskiego", 
    'PL008':"malopolskiego", 
    'PL009':"podkarpackiego", 
    'PL010':"świętokrzyskiego",
    'PL011':"łódzkiego", 
    'PL012':"wielkopolskiego", 
    'PL013':"kujawsko_pomorskiego", 
    'PL014':"warminsko_mazurskiego", 
    'PL015':"lubelskiego",
    'PL016':"podlaskiego",
    'IE003':"dolnoslaskiego",
}

meteoalarmAwareness   = "zagrozenia_meteorologiczne_dla_wojewodztwa"
today    = "dzis"
tomorrow = "jutro"


# World Weather Online


wwo_weather_codes = {
    '113':'bezchmurnie', # Clear/Sunny
    '116':'częściowe zachmurzenie', # Partly Cloudy
    '119':'pochmurno', # Cloudy
    '122':'zachmurzenie całkowite', # Overcast
    '143':'zamglenia', # Mist
    '176':'lokalne przelotne opady deszczu', # Patchy rain nearby
    '179':'śnieg', # Patchy snow nearby
    '182':'śnieg z deszczem', # Patchy sleet nearby
    '185':'lokalna przelotna marznąca mżawka', # Patchy freezing drizzle nearby
    '200':'lokalne burze', # Thundery outbreaks in nearby
    '227':'zamieć śnieżna', # Blowing snow
    '230':'zamieć śnieżna', # Blizzard
    '248':'mgła', # Fog
    '260':'marznąca mgła', # Freezing fog
    '263':'mżawka', # Patchy light drizzle
    '266':'mżawka', # Light drizzle
    '281':'marznąca mżawka', # Freezing drizzle
    '284':'marznąca mżawka', # Heavy freezing drizzle
    '293':'lokalny słaby deszcz', # Patchy light rain
    '296':'słaby deszcz', # Light rain
    '299':'przelotne opady deszczu', # Moderate rain at times
    '302':'umiarkowane opady deszczu', # Moderate rain
    '305':'przelotne ulewy', # Heavy rain at times
    '308':'ulewy', # Heavy rain
    '311':'słabe opady marznącego deszczu', # Light freezing rain
    '314':'umiarkowane opady marznącego deszczu', # Moderate or Heavy freezing rain
    '317':'słabe opady śniegu z deszczem', # Light sleet
    '320':'umiarkowane lub ciężkie opady śniegu z deszczem', # Moderate or heavy sleet
    '323':'słabe opady śniegu', # Patchy light snow
    '326':'słabe opady śniegu', # Light snow
    '329':'umiarkowane opady śniegu', # Patchy moderate snow
    '332':'umiarkowane opady śniegu', # Moderate snow
    '335':'opady śniegu', # Patchy heavy snow
    '338':'intensywne_opady_sniegu', # Heavy snow
    '350':'grad', # Ice pellets
    '353':'słabe przelotne opady deszczu', # Light rain shower
    '356':'przelotne opady deszczu', # Moderate or heavy rain shower
    '359':'ulewny deszcz', # Torrential rain shower
    '362':'słabe opady śniegu z deszczem', # Light sleet showers
    '365':'umiarkowane opady śniegu z deszczem', # Moderate or heavy sleet showers
    '368':'słabe opady śniegu', # Light snow showers
    '371':'umiarkowane opady śniegu', # Moderate or heavy snow showers
    '374':'słabe opady śniegu ziarnistego', # Light showers of ice pellets
    '377':'umiarkowane opady śniegu ziarnistego', # Moderate or heavy showers of ice pellets
    '386':'burza', # Patchy light rain in area with thunder
    '389':'burza', # Moderate or heavy rain in area with thunder
    '392':'burza śnieżna', # Patchy light snow in area with thunder
    '395':'burza śnieżna', # Moderate or heavy snow in area with thunder
}

# HSCR_laviny
hscr_welcome = "komunikat_czeskiej_sluzby_ratownictwa_gorskiego"
hscr_region = {"K": "w_karkonoszach obowiazuje", "J": "w_jesionikach_i_masywie_snieznika obowiazuje"}
avalancheLevel = ['']+[i+' stopien_zagrozenia_lawinowego' for i in ['pierwszy', 'drugi', 'trzeci', 'czwarty', 'piaty_najwyzszy'] ]
hscr_tendention = ['', '', 'tendencja_spadkowa', 'tendencja_wzrostowa']

# GOPR_lawiny
gopr_welcome = 'komunikat_gorskiego_ochotniczego_pogotowia_ratunkowego'
gopr_region = ["", "w_karkonoszach obowiazuje", "", "w_regionie_babiej_gory obowiazuje", "w_pieninach obowiazuje", "w_bieszczadach obowiazuje"]
avalancheLevel = ['']+[i+' stopien_zagrozenia_lawinowego' for i in ['pierwszy', 'drugi', 'trzeci', 'czwarty', 'piaty najwyzszy'] ]
gopr_tendention = ['', '', 'tendencja_spadkowa', 'tendencja_wzrostowa']

# povodi_cz

# awareness levels for povodi_cz
povodi_cz_welcome = 'komunikat_czeskiego_instytutu_hydrometeorologicznego'
awalvls = ['',
    'stopien_czuwania',              # bdelosť            State of Alert
    'stopien_gotowosci',             # pohotovosť         State of Emergency
    'stopien_zagrozenia',            # ohrozenie          State of Danger
    'stopien_ekstremalnych_powodzi'  # extrémna povodeň   extreme flood
    ]

river = 'rzeka'
station = 'wodowskaz'

comma = 'przecinek'
uSiph  = 'mikrosiwerta_na_godzine'
radiation_level = 'promieniowanie_tla'
radiation_levels = ['w_normie', 'podwyzszone', 'wysokie']

source='zrodlo'
