#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
#import subprocess
#import urllib

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

dictionary = my_import(sys.argv[1][0:-3]) # cut .py!

for word in dictionary.download_list:
    filename=word[-1]

    if filename[0:2]=='ę':
        filename=filename[5:]
    if filename[-1] == 'k':
        filename = filename[0:-2]

    filename=filename.replace(' ','_').replace("ą","a").\
            replace("ć","c").replace("ę","e").replace("ł","l").\
            replace("ń","n").replace("ó","o").replace("ś","s").\
            replace("ź","z").replace("ż","z")

    if not os.path.exists("%s.ogg"%filename):
        print "%s;%s"%(filename,word[0])

