#!/usr/env/python -tt
# -*- encoding=utf8 -*-
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

from config import sunriset as config
import pytz, datetime
import lib.Sun
lang=None


# This tiny function is used to convert from UTC to local time. Code inspired
# by ``pytz`` manual, http://pytz.sourceforge.net/#example-usage .
def getLocalTimeFromISO(isoDT, timeZone=config.timeZone):
    y,m,d,hh,mm,ss= ( int(isoDT[0:4]),   int(isoDT[5:7]),   int(isoDT[8:10]),
                      int(isoDT[11:13]), int(isoDT[14:16]), int(isoDT[17:19]) )

    utc = datetime.datetime(y, m, d, hh, mm, ss, tzinfo=pytz.timezone("UTC"))
    loc = utc.astimezone(pytz.timezone(timeZone))

# Returning simple str(loc) should be safe, but in case something will go
# wrong someday we do it another way:

    return loc.strftime("%Y-%m-%d %H:%M:%S %Z%z")

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def float2datetime(time, date=datetime.datetime.utcnow()):
	hh = int(time)

	time = (time-hh)*60
	mm = int(time)

	time = (time-mm)*60
	ss = int(time)

	time = (time-ss)*1000000
	ms = int(time)

	return datetime.datetime(date.year, date.month, date.day, hh, mm, ss, ms, tzinfo=pytz.timezone("UTC"))

def getData(l):
        global lang
        lang = my_import(l+"."+l)

        data = {"data":"", "needCTCSS":False, "debug":None, "allOK":True}
        
        
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.timezone("UTC"))

        sun = lib.Sun.Sun()
        sunrise, sunset = sun.sunRiseSet(now.year, now.month, now.day, config.location[0], config.location[1])

        sunrise, sunset = float2datetime(sunrise), float2datetime(sunset)

	if (now>sunrise and (config.hoursBeforeSunRise==-1 or (now-sunrise).seconds/3600.0<=config.hoursBeforeSunRise)) or config.giveSunRiseAfterSunRise == 1:
		data["data"] = " ".join( (data["data"], lang.sunrise, lang.readHour(sunrise.astimezone(pytz.timezone(config.timeZone)))) )


	if (sunset>now and (config.hoursBeforeSunSet ==-1 or (sunset-now).seconds/3600.0<=config.hoursBeforeSunSet)) or config.giveSunSetAfterSunSet == 1:
		data["data"] = " ".join( (data["data"], lang.sunset, lang.readHour(sunset.astimezone(pytz.timezone(config.timeZone)))) )

	if config.giveDayLength==1:
		data["data"] = " ".join( (data["data"], lang.dayLength, lang.readHourLen(sunset-sunrise)) )

	return data

if __name__ == '__main__':
	print getData('pl')["data"]
