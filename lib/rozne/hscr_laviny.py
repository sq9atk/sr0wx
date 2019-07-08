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

from config import hscr_laviny as config
import datetime
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

def last(list):
	if len(list)==0:
		return None
	else:
		return list[-1]

def getAwareness(region):
	# This is the main page of avalanche awareness system of HS CR:
	url = "http://www.horskasluzba.cz/laviny/"

	# We'll have to find link to the most actual info for the specified region:
	r = u'id\=(\d{4,}).{10,}Lavinov.{5,}'+region # UGLY, but \" doesn't work...
	_id = re.compile(r)
	
	for line in downloadFile(url).split('\n'):
		id = _id.findall(line)
		if id != []:
			id = int(id[0])
			break

	# Now we have the proper URL:
	url = "http://www.horskasluzba.cz/laviny/showlavina.php?id=%d"%(id,)

	# We'll now parse html looking for these:
	_level      = re.compile('/gfx/stupen(\d).gif')
	_tendention = re.compile('/gfx/tendence(\d).gif')
	_exposition = re.compile('/gfx/expozice(\d).gif')
	_date       = re.compile('Datum:\ (\d{1,2})\.\ (\d{1,2})\.\ (\d{4})')

	level, tendention, exposition, date = False,False,False,False

	for line in downloadFile(url).split('\n'):
		line = unicode(line, "cp1250")
		level      = level      or last(_level.findall(line))
		tendention = tendention or last(_tendention.findall(line))
		exposition = exposition or last(_exposition.findall(line))
		if _date.findall(line)!=[]:
			dt       = _date.findall(line)[0]
			now      = datetime.datetime.now()
			delta    = datetime.timedelta(hours=24)
			infoDT = datetime.datetime(int(dt[2]), int(dt[1]), int(dt[0]), 12, 00)
			if infoDT+datetime.timedelta(hours=48)<now:
				isActual = None
			elif infoDT+datetime.timedelta(hours=24)<now:
				isActual = False
			else:
				isActual=True

	return (int(level), int(tendention), int(exposition), isActual, infoDT)

def getData(l):
    global lang
    lang = my_import(l+"."+l)

    data = {"data":"", "needCTCSS":False, "debug":None, "allOK":True,
            "source":""} # given by welcome message

    level, tendention, exposition, isActual, infoDT = getAwareness(config.region)

    if isActual == None:
	    return data
    else:
        data["needCTCSS"]=True

    data["data"] = " ".join( (data["data"], lang.hscr_region[config.region[0]], lang.avalancheLevel[level]) )

    if config.giveTendention==1:
        data["data"] = " ".join( (data["data"], lang.hscr_tendention[tendention]) )

    if isActual==False:
        data["data"] = " ".join( (data["data"], lang.info_at, lang.readISODate(infoDT.isoformat(' '))) )

    # Profile i szczególnie niebezpieczne wystawy niezaimplementowane.

    data["data"] = lang.removeDiacritics(lang.hscr_welcome+' _ '+data["data"])

    return data	

if __name__ == '__main__':
    lang = 'pl'
    print getData('pl')

