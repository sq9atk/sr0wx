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

import numpy.oldnumeric as Numeric

morse = { "A": ".-", "B": "-...", "C": "-.-.","D": "-..","E": ".","F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",

    "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....",
    "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----",

# I have plans with special characters, ie make them sound like _SK_,
# _AR_, etc ...

    ".": ".-.-.-",", ": "--..--", "'": ".----.", "_": "..--.-", ":": "---...",
    "?": "..--..", "-": "-....-", "/": "-..-.", "(": "-.--.",")": "-.--.-",
    "=": "-...-", "@": ".--.-.",

    "^": "........" # error = 8 dits

# ... or with these little creatures ;)

##    "znak rozdziału": 	".-..-",
##    "początek kontaktu (VVV)": "...-...-...-",
##    "początek nadawania": "-.-.-",
##    "koniec nadawania": ".-.-.",
##    "błąd (8 kropek)": "........",
##    "prośba o powtórzenie": "..--..",
##    "zrozumiano": "...-.",
##    "czekaj": "--...",
##    "wezwanie": "-.-",
##    "koniec kontaktu": "...-.-",
##    "międzynarodowy sygnał alarmowy (SOS)": "...---..."
    }

def cw(text, wpm=25, farnsworth=None, weight=None, pitch=600, volume=0.1, sampleRate=44100):
# Would be nice to cope with farnsworth<0 ==> slow down by ... WPM
# Would be nice to implement weight

    text = text.upper()
    if farnsworth is not None:
        try:
            farnsworth = abs(farnsworth)
            if farnsworth>wpm: farnsworth=wpm
        except:
            farnsworth=wpm
            pass
    else: farnsworth=wpm

    volume=abs(volume)
    if volume>1.0: volume=1.0

    if sampleRate not in (11025,22050,44100):
        sampleRate = 44100

# First of all we have to count lengths of pauses, "dits" and "dahs".
# There are three kinds of pauses: between dits and dahs (interBeep),
# between letters (interLetter) and between words (interWord).
#
# Normally (standard weight) "dit" is 1 unit long, "dah" is 3 units long,
# interBeep, interLetter and interword are 1, 3 and 7 units long.
#
# Note, that:
# * interLetter = interBeep + 2 units,
# * interWord = interBeep + interLetter + 3 units.
# We'll use this fact to simplify the code (I hope it will be clear).
#
# Last fact: how long (in seconds) is one unit? For further informations
# see http://www.ac6v.com/morseaids.htm, or belive me that typical word
# "PARIS" is 50 units long (incl. *all* interWord pauses). If we want to
# play it with 5 WPM (Words per Minute) we have to play 250 units, so...
#
# >>> 60.0/250
# 0.23999999999999999
#
# 1 unit is 0.24 seconds long.
#
# This function returns ``pygame.sndarray`` compatible data (``Numeric.aray``).
    unit = 60.0/(50*wpm)

    interBeep   = Numeric.zeros( (int(unit*sampleRate)) )
# Farnsworth (after Farnsworth method, see Google) lest us to make interLetter
# and interWord pauses longer, but we need to recalculate ``unit``'s length:

    fUnit = 60.0/(50*farnsworth)
    interLetter = Numeric.zeros( (int(2*fUnit*sampleRate)) )
    interWord   = Numeric.zeros( (int(3*fUnit*sampleRate)) )


    dit = Numeric.concatenate( (sine_array(pitch,volume,sampleRate,1*unit), interBeep) )
    dah = Numeric.concatenate( (sine_array(pitch,volume,sampleRate,3*unit), interBeep) )

    letters = {}

    for letter in set(text.replace(" ","")):
        if letter in morse:
            for beep in morse[letter]:
                if beep==".":
                    if letters.has_key(letter):
                        letters[letter]=Numeric.concatenate( (letters[letter],dit) )
                    else: letters[letter]=dit
                else:
                    if letters.has_key(letter):
                        letters[letter]=Numeric.concatenate( (letters[letter],dah) )
                    else: letters[letter]=dah
            letters[letter]=Numeric.concatenate( (letters[letter],interLetter) )

    message = interBeep
    for letter in text:
        if letter != " " and letter in morse:
            message = Numeric.concatenate( (message, letters[letter]) )
        else:
            message = Numeric.concatenate( (message, interWord) )


    return Numeric.transpose(Numeric.array((message,message)))


# http://www.nabble.com/Chord-player-td21350708.html
def sine_array_onecycle(hz, peak=0.9,sampleRate=44100):
# Compute one cycle of an N-Hz sine wave with given peak amplitude
    length = sampleRate / float(hz)
    omega = Numeric.pi * 2 / length
    xvalues = Numeric.arange(int(length)) * omega
    return ((peak * 32767) * Numeric.sin(xvalues)).astype(Numeric.Int16)

def sine_array(hz, peak, sampleRate=44100,length=1.0):
#Compute N samples of a sine wave with given frequency and peak amplitude (defaults to one second).
    return Numeric.resize(sine_array_onecycle(hz, peak), (int(sampleRate*length),))


def play(text, wpm=25, farnsworth=None, weight=None, pitch=800, volume=1, sampleRate=44100):
    s= pygame.sndarray.make_sound( cw(text, wpm, farnsworth, weight, pitch, volume, sampleRate) )
    # uncomment this line if you hear cw playing twice.
    s = pygame.sndarray.make_sound(pygame.sndarray.array(s)[:len(pygame.sndarray.array(s))/2])
    c = s.play()
    while c.get_busy() == True:
        pygame.time.wait(25)

if __name__ == '__main__':
    import pygame
    pygame.mixer.pre_init(44100,-16,2,1024)
    pygame.mixer.init(44100,-16,2,1024)
    #pygame.init()
    play("vvv= test")

