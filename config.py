#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

# AKTUALNIE ZALECANE JEST UBUNTU 16.04 MATE
# Poniższy opis dotyczy tej dystrybucji

# WYMAGANE DODATKOWE PAKIETY:
#   sudo apt-get install git
#   sudo apt-get install python-pygame
#   sudo apt-get install python-tz
#   sudo apt-get install python-imaging
#   sudo apt-get install python-serial
#   sudo apt-get install curl
#   sudo apt-get install php7.0
#   sudo apt-get install php7.0-curl
#   sudo apt-get install ffmpeg
#
# LUB WSZYSTKO NA RAZ
#   sudo apt-get install git python-pygame python-tz python-imaging python-serial curl php7.0 php7.0-curl ffmpeg

# UPRAWNIENIA USERA DO PORTU COM
#   sudo gpasswd --add ${USER} dialout

# GENEROWANIE SAMPLI
# Będąc w katalogu audio_generator:
#   php index.php
#
# Generowane są sample z tablicy $słownik z pliku slownik.php. 
# Pozostałe tablice to tylko przechowalnia fraz go wygenerowania.






import logging, logging.handlers

log_line_format = '%(asctime)s %(name)s %(levelname)s: %(message)s'
log_handlers = [{
        'log_level': logging.INFO,
        'class': logging.StreamHandler,
        'config': {'stream': None},
	},{
        'log_level': logging.DEBUG,
        'class': logging.handlers.TimedRotatingFileHandler,
        'config': {
            'filename': 'sr0wx.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
            'delay': True,
            'utc': True,
        }
    }]

serial_port = '/dev/ttyS0'
serial_baud_rate = 9600
serial_signal = 'DTR' # lub 'RTS'


import pl_google.pl_google as pl_google
lang = "pl_google"
pygame_bug = 0

hello_msg = ['_','tu_eksperymentalna_automatyczna_stacja_pogodowa','sr0wx']
goodbye_msg = ['_','tu_sr0wx']
read_sources_msg = False

# -------------
# activity_map
# ------------
from activity_map import ActivityMap
activitymap = ActivityMap(
    service_url="http://wx.ostol.pl/map_requests?base=",
    callsign="TEST",
    latitude=54.655245,
    longitude=19.268097,
    hour_quarter=10,
    above_sea_level=225,
    above_ground_level=20,
    station_range=65,
    additional_info= "Eksperymentalna stacja pogodowa",
)

# ---------------
# openweather_sq9atk
# ---------------
# https://openweathermap.org/api pod tym adresem można uzyskac klucz API
# wystarczy sie zarejestrować
from openweather_sq9atk import OpenWeatherSq9atk
openweathersq9atk = OpenWeatherSq9atk(
    language = pl_google,
    api_key = 'ee78911a0fb560b58144230f46e0d4b2',
    lat = 50,
    lon = 20,
    service_url = 'http://api.openweathermap.org/data/2.5/'
)


# -----------------
# meteoalarm_sq9atk
# -----------------
from meteoalarm_sq9atk import MeteoalarmSq9atk
#meteoalarmsq9atk = MeteoalarmSq9atk(region="PL008")
meteoalarmsq9atk = MeteoalarmSq9atk(region="IT003") # testowo Lombardia
		# PL001-Mazowieckie
		# PL002-Lubuskie
		# PL003-Zachodniopomorskie
		# PL004-Pomorskie
		# PL005-Dolnośląskie
		# PL006-Opolskie
		# PL007-Śląskie
		# PL008-Małopolskie
		# PL009-Podkarpackie
		# PL010-Świętokrzyskie
		# PL011-Łódzkie
		# PL012-Wielkopolskie
		# PL013-Kujawsko-pomorskie
		# PL014-Warmińsko-mazurskie
		# PL015-Lubelskie
		# PL016-Podlaskie
		# PL801-Pomorze Wschodnie
		# PL802-Pomorze Zachodnie
		# IT003-Lombardia

# -------------
# imgw_podest_sq9atk
# ------------
from imgw_podest_sq9atk import ImgwPodestSq9atk
imgwpodestsq9atk = ImgwPodestSq9atk(
    wodowskazy = [

## MAPA WSZYSTKICH WODOWSKAZÓW W POLSCE Z NUMERAMI
## http://wx.ostol.pl/wodowskazy/

        '2.149180210',   # Nazwa: Zabrzeg, rzeka: Wisła             - zrypany wodowskaz / tylko do testów
        '2.149200360',   # Nazwa: Lipnica Murowana, rzeka: Uszwica  - zrypany wodowskaz / tylko do testów
        '2.149200370',   # Nazwa: Okocim, rzeka: Uszwica            - zrypany wodowskaz / tylko do testów
        '2.149190350',   # Nazwa: Krzczonów, rzeka: Krzczonówka     - zrypany wodowskaz / tylko do testów
        '2.150210200',   # Nazwa: Grebów, rzeka: Łęg                - zrypany wodowskaz / tylko do testów
        '2.149180080',   # Nazwa: Drogomyśl, rzeka: Wisła           - zrypany wodowskaz / tylko do testów

        '2.149210050',   # Nazwa: Krajowice, rzeka: Wisłoka
        '2.149200110',   # Nazwa: Trybsz, rzeka: Białka
        '2.149200290',   # Nazwa: Muszyna, rzeka: Poprad
        '2.149190230',   # Nazwa: Czernichów-Prom, rzeka: Wisła
        '2.149180090',   # Nazwa: Borki Mizerów, rzeka: Pszczynka
        '2.150200100',   # Nazwa: Popędzynka, rzeka: Wisła
        '2.150210100',   # Nazwa: Połaniec, rzeka: Czarna Staszowska
        '2.149180250',   # Nazwa: Czechowice Dziedzice, rzeka: Iłowica
        '2.149200050',   # Nazwa: Nowy Targ Kowaniec, rzeka: Dunajec
        '2.150210060',   # Nazwa: Staszów, rzeka: Czarna Staszowska
        '2.149190060',   # Nazwa: Jawiszowice, rzeka: Wisła
        '2.149200190',   # Nazwa: Gołkowice, rzeka: Dunajec
        '2.149190140',   # Nazwa: Łękawica, rzeka: Łękawka
        '2.150200060',   # Nazwa: Sierosławice, rzeka: Wisła
        '2.149180120',   # Nazwa: Górki Wielkie, rzeka: Brennica
        '2.149210040',   # Nazwa: Łabuzie, rzeka: Wisłoka
        '2.150210150',   # Nazwa: Koło, rzeka: Wisła
        '2.149200100',   # Nazwa: Łysa Polana, rzeka: Białka
        '2.150190120',   # Nazwa: Przeczyce, rzeka: Czarna Przemsza
        '2.150210110',   # Nazwa: Głowaczowa, rzeka: Grabinianka
        '2.150200070',   # Nazwa: Biskupice, rzeka: Szreniawa
        '2.149200020',   # Nazwa: Szaflary, rzeka: Biały Dunajec
        '2.149190070',   # Nazwa: Łodygowice, rzeka: Żylica
        '2.150200170',   # Nazwa: Żabno, rzeka: Dunajec
        '2.150210140',   # Nazwa: Brzeźnica, rzeka: Wielopolka
        '2.149190170',   # Nazwa: Zator, rzeka: Skawa
        '2.150190330',   # Nazwa: Ojców, rzeka: Prądnik
        '2.150200080',   # Nazwa: Pińczów, rzeka: Nida
        '2.150210120',   # Nazwa: Mielec, rzeka: Wisłoka
        '2.149200130',   # Nazwa: Stradomka, rzeka: Stradomka
        '2.149200220',   # Nazwa: Stary Sącz, rzeka: Poprad
        '2.149200230',   # Nazwa: Czchów, rzeka: Dunajec
        '2.149200030',   # Nazwa: Nowy Targ, rzeka: Czarny Dunajec
        '2.149200330',   # Nazwa: Ciężkowice, rzeka: Biała
        '2.150200160',   # Nazwa: Daleszyce, rzeka: Czarna Nida
        '2.149190390',   # Nazwa: Ludźmierz, rzeka: Wielki Rogoźnik
        '2.149210100',   # Nazwa: Zboiska, rzeka: Jasiołka
        '2.149200270',   # Nazwa: Łabowa, rzeka: Kamienica
        '2.150190340',   # Nazwa: Kraków-Bielany, rzeka: Wisła
        '2.149200080',   # Nazwa: Mszana Dolna, rzeka: Mszanka
        '2.149180100',   # Nazwa: Skoczów, rzeka: Wisła
        '2.149200120',   # Nazwa: Niedzica, rzeka: Niedziczanka
        '2.150190100',   # Nazwa: Niwka, rzeka: Biała Przemsza
        '2.150200090',   # Nazwa: Słowik, rzeka: Bobrza
        '2.150210130',   # Nazwa: Pustków, rzeka: Wisłoka
        '2.149180220',   # Nazwa: Pszczyna, rzeka: Pszczynka
        '2.149190050',   # Nazwa: Rajcza, rzeka: Soła
        '2.150210030',   # Nazwa: Mocha, rzeka: Łagowica
        '2.150190060',   # Nazwa: Bojszowy, rzeka: Gostynka
        '2.149190100',   # Nazwa: Żywiec, rzeka: Soła
        '2.150200010',   # Nazwa: Mniszek, rzeka: Biała Nida
        '2.149190260',   # Nazwa: Osielec, rzeka: Skawa
        '2.149200320',   # Nazwa: Koszyce Wielkie, rzeka: Biała
        '2.149190380',   # Nazwa: Zakopane Harenda, rzeka: Cicha Woda
        '2.150200150',   # Nazwa: Karsy, rzeka: Wisła
        '2.150190190',   # Nazwa: Piwoń, rzeka: Czarna Przemsza
        '2.150190210',   # Nazwa: Kuźnica Sulikowska, rzeka: Mitręga
        '2.149190300',   # Nazwa: Kościelisko-Kiry, rzeka: Potok Kościeliski
        '2.149210070',   # Nazwa: Żółków, rzeka: Wisłoka
        '2.149200090',   # Nazwa: Dobczyce, rzeka: Raba
        '2.149210010',   # Nazwa: Ropa, rzeka: Ropa
        '2.149200150',   # Nazwa: Tylmanowa, rzeka: Ochotnica
        '2.149190180',   # Nazwa: Wadowice, rzeka: Skawa
        '2.150190070',   # Nazwa: Szabelnia, rzeka: Brynica
        '2.149190340',   # Nazwa: Rabka, rzeka: Raba
        '2.149190270',   # Nazwa: Radziszów, rzeka: Skawinka
        '2.150190170',   # Nazwa: Pustynia, rzeka: Wisła
        '2.150200020',   # Nazwa: Bocheniec, rzeka: Łososina
        '2.149200010',   # Nazwa: Poronin, rzeka: Poroniec
        '2.150210020',   # Nazwa: Szczucin, rzeka: Wisła
        '2.150200140',   # Nazwa: Borzęcin, rzeka: Uszwica
        '2.149190370',   # Nazwa: Lubień, rzeka: Lubieńka
        '2.149200250',   # Nazwa: Nowy Sącz, rzeka: Kamienica
        '2.149190020',   # Nazwa: Kamesznica, rzeka: Bystra
        '2.149200310',   # Nazwa: Grybów, rzeka: Biała
        '2.150190180',   # Nazwa: Jeleń, rzeka: Przemsza
        '2.149180180',   # Nazwa: Wisła Czarne, rzeka: Biała Wisełka
        '2.149210060',   # Nazwa: Topoliny, rzeka: Ropa
        '2.150190260',   # Nazwa: Smolice, rzeka: Wisła
        '2.149180200',   # Nazwa: Wisła Czarne, rzeka: Czarna Wisełka
        '2.149200140',   # Nazwa: Sromowce Wyżne, rzeka: Dunajec
        '2.150210010',   # Nazwa: Raków, rzeka: Czarna Staszowska
        '2.150190160',   # Nazwa: Oświęcim, rzeka: Soła
        '2.149200260',   # Nazwa: Nowy Sącz, rzeka: Łubinka
        '2.150200030',   # Nazwa: Brzegi, rzeka: Nida
        '2.149190200',   # Nazwa: Sucha Beskidzka, rzeka: Stryszawka
        '2.149200240',   # Nazwa: Nowy Sącz, rzeka: Dunajec
        '2.149190360',   # Nazwa: Ludźmierz, rzeka: Lepietnica
        '2.149200060',   # Nazwa: Mszana Dolna, rzeka: Raba
        '2.149180160',   # Nazwa: Wisła Czarne, rzeka: Wisła
        '2.149210090',   # Nazwa: Krempna-Kotań, rzeka: Wisłoka
        '2.149190310',   # Nazwa: Stróża, rzeka: Raba
        '2.149190280',   # Nazwa: Koniówka, rzeka: Czarny Dunajec
        '2.149190150',   # Nazwa: Pewel Mała, rzeka: Koszarawa
        '2.149180110',   # Nazwa: Ustroń Obłaziec, rzeka: Wisła
        '2.149200170',   # Nazwa: Proszówki, rzeka: Raba
        '2.149210030',   # Nazwa: Klęczany, rzeka: Ropa
        '2.150190010',   # Nazwa: Brynica, rzeka: Brynica
        '2.149190080',   # Nazwa: Cięcina, rzeka: Soła
        '2.149190120',   # Nazwa: Czaniec (Kobiernice), rzeka: Soła
        '2.149190210',   # Nazwa: Sucha Beskidzka, rzeka: Skawa
        '2.149190040',   # Nazwa: Ujsoły, rzeka: Woda Ujsolska
        '2.150200120',   # Nazwa: Morawica, rzeka: Czarna Nida
        '2.150200040',   # Nazwa: Tokarnia, rzeka: Czarna Nida
        '2.149210080',   # Nazwa: Jasło, rzeka: Jasiołka
        '2.149190290',   # Nazwa: Jordanów, rzeka: Skawa
        '2.150190360',   # Nazwa: Gromiec, rzeka: Wisła
        '2.150190080',   # Nazwa: Radocha, rzeka: Czarna Przemsza
        '2.149190160',   # Nazwa: Rudze, rzeka: Wieprzówka
        '2.149200160',   # Nazwa: Krościenko, rzeka: Dunajec
        '2.149190090',   # Nazwa: Żabnica, rzeka: Żabniczanka
        '2.150190140',   # Nazwa: Nowy Bieruń, rzeka: Wisła
        '2.149200280',   # Nazwa: Zgłobice, rzeka: Dunajec
        '2.149190220',   # Nazwa: Skawica Dolna, rzeka: Skawica
        '2.150210170',   # Nazwa: Sandomierz, rzeka: Wisła
        '2.150180270',   # Nazwa: Kozłowa Góra, rzeka: Brynica
        '2.149190010',   # Nazwa: Czechowice-Bestwina, rzeka: Biała
        '2.150210070',   # Nazwa: Wampierzów, rzeka: Breń
        '2.149200200',   # Nazwa: Jakubkowice, rzeka: Łososina
        '2.150200050',   # Nazwa: Michałów, rzeka: Mierzawa
        '2.150210160',   # Nazwa: Koprzywnica, rzeka: Koprzywianka
        '2.149200040',   # Nazwa: Kasinka Mała, rzeka: Raba
        '2.150190310',   # Nazwa: Balice, rzeka: Rudawa
    ]
)

# --------------------
# air_pollution_sq9atk
# --------------------
from datetime import datetime
from air_pollution_sq9atk import AirPollutionSq9atk
airpollutionsq9atk = AirPollutionSq9atk(
    language=pl_google,
    service_url="http://api.gios.gov.pl/pjp-api/rest/",
    station_id = 402,

        # LISTA STACJI Z NUMERAMI Z CAŁEJ POLSKI
        # http://api.gios.gov.pl/pjp-api/rest/station/findAll

        # poniższe TYLKO DLA KRAKOWA!!!!!
        # do station_id wpada co 20 minut inna cyfra z przedziału 0,1,2
        # dzięki czemu za każdym razem wybieramy inną stację pomiarową
        # station_id = 400 + (int(datetime.now().strftime('%M')))/20,
        # 400 Kraków, Aleja Krasińskiego
        # 401 Kraków, ul. Bujaka
        # 402 Kraków, ul. Bulwarowa
        # 10121 Kraków, ul. Dietla
        # 10123 Kraków, ul. Złoty Róg
        # 10139 Kraków, os. Piastów
        # 10435 Kraków, ul. Telimeny
        # 10447 Kraków, os. Wadów
)

# ---------------
# airly_sq9atk
# ---------------
# https://developer.airly.org/ pod tym adresem można uzyskac klucz API
# wystarczy sie zarejestrować
from airly_sq9atk import AirlySq9atk
airlysq9atk = AirlySq9atk(
    language = pl_google,
    api_key = '02b3a79363c3497dbb992093cd9d7779',
    service_url = 'https://airapi.airly.eu/v2/measurements', #location
    mode = 'nearest',  # point|nearest|installationId
    lat = 50.079242,
    lon = 18.516138,
    maxDistanceKM = 5,
    installationId = 8077, # Mikołajska Kraków
)

# --------------------
# geomagnetic_sq9atk
# --------------------
from geo_magnetic_sq9atk import GeoMagneticSq9atk
geomagneticsq9atk = GeoMagneticSq9atk(
    language=pl_google,
    service_url="https://www.gismeteo.pl/weather-krakow-3212/gm/",
)
        # https://www.gismeteo.pl/weather-warsaw-3196/gm/
        # https://www.gismeteo.pl/weather-gdansk-3046/gm/
        # https://www.gismeteo.pl/weather-szczecin-3101/gm/
        # https://www.gismeteo.pl/weather-krakow-3212/gm/
        # https://www.gismeteo.pl/weather-rzeszow-3215/gm/
        # https://www.gismeteo.pl/weather-suwaki-269290/gm/
        # https://www.gismeteo.pl/weather-jelenia-gora-3206/gm/
        # https://www.gismeteo.pl/weather-poznan-3194/gm/
        # https://www.gismeteo.pl/weather-lublin-3205/gm/
        # https://www.gismeteo.pl/weather-gorzow-wielkopolski-3192/gm/
        # https://www.gismeteo.pl/weather-tarnowskie-gory-3152/gm/
        # https://www.gismeteo.pl/weather-ptakowice-280575/gm/
        # więcej miejscowości po wejściu na dowolny z powyższych adresów w przeglądarce...

# ---------------
# radioactive_sq9atk
# ---------------
from radioactive_sq9atk import RadioactiveSq9atk
radioactivesq9atk = RadioactiveSq9atk(
    language=pl_google,
    service_url="http://radioactiveathome.org/map/",
    sensor_id=35167 #czujnik w centrum Krakowa
    ## więcej czujników na stronie http://radioactiveathome.org/map/
)

# ---------------
# propagation_sq9atk
# ---------------
from propagation_sq9atk import PropagationSq9atk
propagationsq9atk = PropagationSq9atk(
    language=pl_google,
    service_url="https://rigreference.com/solar/img/tall",
)

# ---------------
# calendar_sq9atk
# ---------------
from calendar_sq9atk import CalendarSq9atk
calendarsq9atk = CalendarSq9atk(
    language=pl_google,
    service_url="http://calendar.zoznam.sk/sunset-pl.php?city=",
    city_id=3094802, # Kraków
)
        # 776069 Białystok
        # 3102014 Bydgoszcz
        # 3100946 Częstochowa
        # 3099434 Gdańsk
        # 3099424 Gdynia
        # 3096472 Katowice
        # 3094802 Kraków
        # 3093133 Lodz
        # 765876 Lublin
        # 3088171 Poznań
        # 760778 Radom
        # 3085128 Sosnowiec
        # 3083829 Szczecin
        # 756135 Warsaw
        # 3081368 Wrocław

# WŁĄCZONE MODUŁY
modules = [
	activitymap,            # marker na mapie wx.ostol.pl
    #openweathersq9atk,      # prognoza pogody
	#meteoalarmsq9atk,       # zagrożenia meteo
	#imgwpodestsq9atk,       # wodowskazy
	#airpollutionsq9atk,     # zanieczyszczenia powietrza z GIOŚ
    #airlysq9atk,            # zanieczyszczenia powietrza z Airly
    #propagationsq9atk,      # propagacja KF
	#geomagneticsq9atk,      # zaburzenia geomagnetyczne
	#radioactivesq9atk,      # promieniowanie jonizujące
    calendarsq9atk,         # wschód słońca
]
