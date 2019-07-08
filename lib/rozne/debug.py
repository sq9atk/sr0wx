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
# *********
# debug.py
# *********
#
# Special module for showing/storing debug informations. Log is saved in
# debug.path (stored in config) as yy-mm-dd.log. 

from config import debug as config
import datetime, os


# When module wants to log something it should give its name, message 
# to be logged and buglevel. debug.log() will "make decision" (basing
# config) if this message should be shown on screen and saved or just
# saved. Default buglevel is 0 (verbose).

def log(moduleName, message, buglevel=0):
    dt = datetime.datetime.utcnow()
    prefix = "%s [%s]:\t"%(dt.strftime("%y-%m-%d %X UTC"),moduleName )
    message = prefix + message.replace("\n","".join( ("\r\n",prefix) ))

    if buglevel>=config.showLevel:
        print message
    if buglevel>=config.writeLevel:
        filename = dt.strftime("%y-%m-%d")+".log"
        if not os.path.exists(filename):
            logfile = open(filename, 'w')
        else:
            logfile = open(filename, 'a+')
        try:
            logfile.write(message + '\n')
        except:
            print dt.strftime("%x %X UTC")+" [DEBUG]:\tCan't write to file!"
        finally:
            logfile.close()

