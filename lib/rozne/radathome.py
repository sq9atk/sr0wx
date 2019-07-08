#!/usr/env/python -tt
# -*- encoding=utf8 -*-
#
#   Copyright 2009-2013 Michal Sadowski (sq6jnx at hamradio dot pl)
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

import urllib
import datetime
from config import radAtHome as config
import datetime
import csv
import debug
import sqlite3

lang=None

# Documentation of some kind:
# http://www.boincatpoland.org/smf/radioactivehome/dostep-do-danych-radh/
# http://radioactiveathome.org/boinc/forum_thread.php?id=60#574
# you can find ticks to uS formula under second link.

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def parse_csv():
    added, not_added = 0,0

    db=sqlite3.connect(config.database)
    
    db.execute("""
    create table if not exists radathome(
        id int,
        ticks int,
        timestamp int primary key,
        sensor_rev int,
        status char(1),
        column_A text,
        parent_timestamp);""")
    db.commit()

    with open(config.file_path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            row[2]=datetime.datetime.strptime(row[2],"%Y-%m-%d %H:%M:%S").\
                    strftime('%s')
            try:
                db.execute("""
                    insert into radathome(
                            id, ticks, timestamp, sensor_rev,status, column_A, parent_timestamp) 
                    values (?,?,?,?,?,?, (select max(timestamp) from radathome))""", row)
                added+=1
            except sqlite3.IntegrityError:
                not_added+=1
                pass

    db.commit()
    debug.log("RADATHOME", 'Added %d, not added %d measurements'%(added,not_added,))

def get_radiation_level():

    db=sqlite3.connect(config.database)
    c=db.execute("""
        select
        	/*
        	 * long story here:
        	r1.timestamp, r1.ticks, r2.timestamp, r2.ticks,
        	r1.timestamp-r2.timestamp as d_timestamp,
        	r1.status, r2.status,
        	r1.ticks-r2.ticks as d_ticks,
        	(r1.ticks-r2.ticks)/((r1.timestamp-r2.timestamp)/60.0)/171.232876 as radiation	
        	*/
        	avg((r1.ticks-r2.ticks)/((r1.timestamp-r2.timestamp)/60.0)/171.232876)	
        from radathome as r1 
        	inner join radathome as r2 on r1.parent_timestamp=r2.timestamp
        where 
            r1.status='n' /* "newer" measurement must be normal, not "first" or "restarted" */	
            /* for sanity: we substract "older" measurement from "newer" */
            and r1.timestamp>r2.timestamp
            and r1.ticks>r2.ticks
            and datetime(r1.timestamp,'unixepoch')>=datetime('now','utc',?)
            """, ['-%d hours'%config.n_hours])
    
    try:
        return c.fetchone()[0]
    except TypeError:
        return None
        pass
    

def getData(l):
    global lang
    lang = my_import(l+"."+l)
    data = {"data":"", "needCTCSS":False, "debug":None, 
            "source":"", "allOK":True}

    rlevel = get_radiation_level()
    if rlevel is not None:
        if rlevel<config.medium_tresh:
            lvl=lang.radiation_levels[0]
        elif rlevel<config.high_tresh:
            lvl=lang.radiation_levels[1]
            data['needCTCSS']=True
        else:
            lvl=lang.radiation_levels[2]
            data['needCTCSS']=True
        
        data['data']=lang.removeDiacritics(' '.join( (lang.radiation_level, lvl, 
                lang.readFraction(rlevel, 3), lang.uSiph) ))

    return data

if __name__=='__main__':
    parse_csv()
