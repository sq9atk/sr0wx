#!/usr/bin/python
# -*- coding: utf-8 -*-

# Caution! I am not responsible for using these samples. Use at your own risk
# Google, Inc. is the copyright holder of samples downloaded with this tool.
#
# Unfortunatelly, Google gives no license text for these samples. I hope
# they're made with free (beer)/open source/free (freedom) software,
# but I have no idea.
#
# You'll have to copy this file into language catalogue in order to download
# samples you need.
#
# This file is ugly, dirty, and probably useless when downloading
# other samples than polish. But I will fix it one day.

import urllib
import os, sys
import subprocess

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

dictionary = my_import(sys.argv[1][0:-3]) # cut .py!

for word in dictionary.download_list:
    phrase = word[0]
    if len(word)==1:
        filename = phrase.replace(' ','_').replace("ą","a").replace("ć","c").replace("ę","e").\
		replace("ł","l").replace("ń","n").replace("ó","o").replace("ś","s").\
		replace("ź","z").replace("ż","z")
        if phrase[0:3]=="ę.":
            filename=filename[4:]
        if phrase[-1] == "k":
            filename = filename[0:-2]
    else:
        filename = word[1]

    if not os.path.exists("%s.ogg"%filename):
        start, end = (0,0.4575)
        if phrase[0:3]=="ę.":
            start = 0.5
        if phrase[-1] == "k":
            end = 0.73

        #url = "\"http://translate.google.com/translate_tts?tl=pl&q=%s\""%urllib.quote_plus(phrase+" .")
        #os.system("wget -q -U \"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6\" -O %s.mp3 %s"%(filename,url))
        url = u"\"http://translate.google.com/translate_tts?tl=%s&q=%s&total=1&idx=0&client=t\"" % (dictionary.LANGUAGE, urllib.quote_plus(phrase + " ."))
        os.system("wget -q -U 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36' -O %s.mp3 %s" % (filename, url))

        os.system("lame --decode %s.mp3 %s.wav"%(filename,filename))
        length = float(subprocess.Popen(["soxi", "-D", "%s.wav"%filename], stdout=subprocess.PIPE).communicate()[0])

        os.system("sox %s.wav %s.ogg trim %s %s"%(filename,filename, str(start), str(length-end)))

        #os.system("mplayer %s.ogg"%filename)
        os.remove(filename+".wav")
        os.remove(filename+".mp3")
