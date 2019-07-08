#!/usr/bin/python
# -*- coding: utf-8 -*-

# Caution! I am not responsible for using these samples. Use at your own risk
# Google, Inc. is the copyright holder of samples downloaded with this tool.
#
# Unfortunatelly, Google gives no license text for these samples. I hope
# they're made with free (beer)/open source/free (freedom) software,
# but I have no idea.

# This is the GENERAL download list and settings for polish language

LANGUAGE = 'pl'

CUT_START = 0.9
CUT_END=0.7

CUT_PREFIX = 'ę. '
CUT_SUFFIX = ' k'

download_list = [
# welcome and goodbye messages
["tu eksperymentalna automatyczna stacja pogodowa k",],
["tu automatyczna stacja pogodowa powiatu brzeskiego"],
["tu automatyczna stacja pogodowa powiatu prudnickiego"],


["tu automatyczna stacja pogodowa powiatu olsztyniskiego",
    "tu_automatyczna_stacja_pogodowa_powiatu_olsztynskiego",],

["ę. Stanisław Paweł 6 Jokohama - Roman, Ewa", "sp6yre"],
["ę. stanisław kłebek 6 jadwiga natalia kłebek ", "sq6jnq"],
["ę. stanisław kłebek 6 adam cezary maria", "sq6acm"],
["ę. stanisław paweł 6 karol ewa olga", "sp6keo"],


["tu Stanisław Paweł 6 Jokohama, Roman, Ewa", 'tu_sp6yre'],
["tu stanisław kłebek 6 jadwiga natalia kłebek k", 'tu_sq6jnq'],
["tu stanisław kłebek 6 adam cezary maria", 'tu_sq6acm'],
["tu stanisław paweł 6 karol ewa olga", "tu_sp6keo"],

["stan pogody z dnia ",],
["stan pogody z godziny",],

["pierwszego"], ["drugiego"], ["trzeciego"], ["czwartego"],
["piątego"], ["szóstego"], ["siódmego"],
["ę. ósmego", 'osmego'], ["dziewiątego"], ["dziesiątego"],
["jedenastego"], ["dwunastego"],
["trzynastego"], ["czternastego"], ["piętnastego"],
["szesnastego"], ["siedemnastego"], ["osiemnastego"],
["dziewiętnastego"], ["dwudziestego"], ["trzydziestego"],

["stycznia"],
["lutego"], ["marca"], ["kwietnia"], ["maja"], ["czerwca"],
["lipca"], ["sierpnia"], ["września"], ["października"],
["listopada"], ["grudnia"],

["zero"],
["zero zero"], ["jeden"],
["dwa"], ["trzy"], ["cztery"], ["pięć"], ["sześć"],
["siedem"], ["osiem"], ["dziewięć"], ["dziesięć"],
["jedenaście"], ["dwanaście"], ["trzynaście"],
["czternaście"], ["piętnaście"], ["szesnaście"],
["siedemnaście"], ["osiemnaście"], ["dziewiętnaście"],
["dwadzieścia"], ["trzydzieści"], ["czterdzieści"],
["pięćdziesiąt"], ["sześćdziesiąt"], ["siedemdziesiąt"],
["osiemdziesiąt"], ["dziewięćdziesiąt"], ["sto"],
["dwieście"], ["trzysta"], ["czterysta"], ["pięćset"],
["sześćset"], ["siedemset"], ["osiemset"], ["dziewięćset"],
["tysiąc"],

["źródło"],

# nazwy zjawisk pogodowych (dla Yahoo! Weather)
['bezchmurnie'], ['burza'], ['burza tropikalna'], ['częściowe zachmurzenie'],
['deszcz'], ['deszcz i deszcz ze śniegiem'], ['deszcz i grad'],
['deszcz ze śniegiem'], ['grad'], ['huragan'], ['intensywne opady śniegu'],
['marznąca mżawka'], ['marznący deszcz'], ['mgła'], ['mżawka'], ['pochmurno'],
['przelotne opady'], ['przelotne opady śniegu'], ['przymrozki'],
['pył'], ['silne burze'], ['silny wiatr'], ['słabe zachmurzenie'],
['słaby śnieg'], ['smog'], ['śnieg'], ['śnieg i deszcz ze śniegiem'],
['tornado'], ['wietrznie'], ['wysokie temperatury'], ['zamglenia'],
['zawieje śnieżne'], ["jahu łeder","y_weather"],


#
## różne
["temperatura"], ["stopień celsjusza"],
["minus"], ["stopnie celsjusza"], ["stopni celsjusza"],
["kierunek wiatr"], ["północny"], ["północno"], ["wschodni"],
["wschodnio"], ["zachodni"], ["zachodnio"], ["południowy"],
["południowo"], ["wilgotność"], ["procent"], ["prędkość wiatru"],
["metr na sekundę"], ["metrów na sekundę"],
["stopień"],["stopnie"],["stopni"],
["widoczność"], ["kilometr"], ["kilometry"],
["kilometrów"], ["temperatura odczuwalna"],
["prognoza na następne"], ["godzin"],["godzina"],
["godziny"], ["temperatura od"],

["pierwsza"], ["druga"], ["trzecia"], ["czwarta"], ["piąta"],
["szósta"], ["siódma"], ["ósma","osma"], ["dziewiąta"], ["dziesiąta"],
["jedenasta"], ["dwunasta"], ["trzynasta"], ["czternasta"],
["piętnasta"], ["szesnasta"], ["siedemnasta"], ["osiemnasta"],
["dziewiętnasta"], ["dwudziesta"],

["kierunek wiatru"], ["metr na sekundę"], ["metry na sekundę"],
["metrów na sekunde"],
["kilometr na godzinę"], ["kilometry na godzinę"], ["kilometrów na godzinę"],

["ciśnienie"], ["hektopaskal"],
["hektopaskale"], ["hektopaskali"], ["tendencja spadkowa"],
["tendencja wzrostowa"], ["temperatura odczuwalna"],
["temperatura minimalna"], ["maksymalna"],
["następnie"],

# sms_qst

['komunikat specjalny od'],
['powtarzam komunikat'],

# literowanie polskie wg. "Krótkofalarstwo i radiokomunikacja - poradnik",
# Łukasz Komsta SQ8QED, Wydawnictwa Komunikacji i Łączności Warszawa, 2001,
# str. 130 (z drobnymi modyfikacjami fonetycznymi)

['adam', 'a'],
['barbara', 'b'],
['celina', 'c'],
['dorota', 'd'],
['edward', 'e'],
['franciszek k', 'f'],
['gustaw', 'g'],
['henryk k', 'h'],
['irena', 'i'],
['józef', 'j'],
['karol', 'k'],
['ludwik k', 'l'],
['marek k', 'm'],
['natalia', 'n'],
['olga', 'o'],
['paweł', 'p'],
['kłebek k', 'q'], # wł. Quebec
['roman', 'r'],
['stefan', 's'],
['tadeusz', 't'],
['urszula', 'u'],
['violetta', 'v'],
['wacław', 'w'],
['xawery', 'x'],
['ypsylon', 'y'], # wł. Ypsilon
['zygmunt', 'z'],
['łamane'],

# Sample potrzebne dla modułu meteoalarm (cała Polska)

["ę.  zagrożenia meteorologiczne dla województwa", 'zagrozenia_meteorologiczne_dla_wojewodztwa'],
["ę.  mazowieckiego"],
["ę.  lubuskiego"],
["ę.  zachodniopomorskiego"],
["ę.  pomorskiego"],
["ę.  dolnośląskiego"],
["ę.  opolskiego"],
["ę.  śląskiego"],
["ę.  małopolskiego"],
["ę.  podkarpackiego"],
["ę.  świętokrzyskiego"],
["ę.  łódzkiego"],
["ę.  wielkopolskiego"],
["ę.  kujawsko-pomorskiego"],
["ę.  warminsko-mazurskiego"],
["ę.  lubelskiego"],
["ę.  podlaskiego"],
["ę.  dziś"],
["ę.  jutro"],
["ę.  silny wiatr"],
["ę.  śnieg lub oblodzenie"],
["ę.  burze"],
["ę.  mgły"],
["ę.  wysokie temperatury"],
["ę.  niskie temperatury"],
["ę.  zjawiska strefy brzegowej"],
["ę.  pożary lasów"],
["ę.  lawiny"],
["ę.  intensywne opady deszczu"],
["ę.  inne zagrożenia"],
["ę.  poziom zagrożenia"],
["ę.  nieokreślony"],
["ę.  niski"],
["ę.  średni"],
["ę.  wysoki"],

["meteoalarm eeuu","meteoalarm_eu"],

# Sample dla WorldWeatherOnline

['bezchmurnie'], ['burza'], ['burza śnieżna'], ['częściowe zachmurzenie'],
['grad'], ['Intensywne opady śniegu'], ['lokalna przelotna marznąca mżawka'],
['lokalne burze'], ['lokalne przelotne opady deszczu'],
['lokalny słaby deszcz'], ['marznąca mgła'], ['marznąca mżawka'], ['mgła'],
['mżawka'], ['opady śniegu'], ['pochmurno'], ['przelotne opady deszczu'],
['przelotne ulewy'], ['słabe opady marznącego deszczu'],
['słabe opady śniegu'], ['słabe opady śniegu z deszczem'],
['słabe opady śniegu ziarnistego'], ['słabe przelotne opady deszczu'],
['słaby deszcz'], ['śnieg'], ['śnieg z deszczem'],
['ulewny deszcz'], ['ulewy'],
['umiarkowane lub ciężkie opady śniegu z deszczem'],
['umiarkowane opady deszczu'], ['umiarkowane opady marznącego deszczu'],
['umiarkowane opady śniegu'], ['umiarkowane opady śniegu z deszczem'],
['umiarkowane opady śniegu ziarnistego'], ['zachmurzenie całkowite'],
['zamglenia'], ['zamieć śnieżna'], ['pokrywa chmur'],
['łorld łeder onlajn',"worldweatheronline"],

# Sample dla hscr_laviny

['komunikat czeskiej służby ratownictwa górskiego'],
['w karkonoszach'],['w jesionikach i masywie śnieżnika'], ['obowiązuje'],
["pierwszy"],["drugi"],["trzeci"],["czwarty"],
["piąty, najwyższy", 'piaty_najwyzszy'], ['stopień zagrożenia lawinowego'],
['tendencja wzrostowa'],['tendencja spadkowa'],
['służba górska republiki czeskiej','hscr'],

# Sample dla gopr_laviny

['ę.  komunikat górskiego ochotniczego pogotowia ratunkowego'],
["ę.  w karkonoszach"], ["w regionie babiej góry"],
["w pieninach"], ["w bieszczadach"], ["ę.  obowiązuje"],
["pierwszy"],["drugi"],["trzeci"],["czwarty"],
["ę. piąty, najwyższy", 'piaty_najwyzszy'],
['ę.  stopień zagrożenia lawinowego'],
['tendencja wzrostowa'],['tendencja spadkowa'],['gopr'],

# Sample dla povodi_cz

['komunikat czeskiego instytutu hydrometeorologicznego'],
['rzeka'], ['wodowskaz'],
['ę. stopień czuwania',             'stopien_czuwania',],
['ę. stopień gotowości',            'stopien_gotowosci',],
['ę. stopień zagrożenia',           'stopien_zagrozenia',],
['ę. stopień ekstremalnych powodzi','stopien_ekstremalnych_powodzi'],
['czeski instytut hydrometeorologiczny'],

# niektóre czeskie nazwy dla povodi_cz (głównie przygraniczne) na potrzeby
# SP6TPW i przez niego przetłumaczone. Dzięki, Grzegorz!

# Sample dla radioactive@Home

['promieniowanie tła'],
['przecinek', 'przecinek'],
['mikrosjiwerta na godzinę', 'mikrosiwerta_na_godzine'],
['w normie'],
['podwyższone'],
['wysokie'],

]
