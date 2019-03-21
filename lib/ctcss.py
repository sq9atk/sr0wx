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
 
# This is list of IARU Region I CTCSS tones
# (http://hamradio.pl/sq9jdo/_Kurs/Kurs%20operatora/CTCSS/system_ctcss.html).
# Please, do not modify this if you're living in Region I.

CTCSSTones = {'A': 67.0, 'T': 131.8, 'B': 71.9, 'U': 136.5, 'C': 74.4,
    'V': 141.3, 'D': 77.0, 'W': 146.2, 'E': 79.7, 'X': 151.4, 'F': 82.5,
    'Y': 156.7, 'G': 85.4, 'Z': 162.2, 'H': 88.5, 'AA':167.9, 'I': 91.5,
    'AB': 173.8, 'J': 94.8, 'AC': 179.9, 'K': 97.4, 'AD': 186.2, 'L': 100.0,
    'AE': 192.8, 'M': 103.5, 'AF': 203.5, 'N': 107.2, 'AG': 210.7, 'O': 110.9,
    'AH': 218.1, 'P': 114.8, 'AI': 225.7, 'Q': 118.8, 'AJ': 233.6, 'R': 123.0,
    'AK': 241.8, 'S': 127.3, 'AL': 250.3}

import numpy.oldnumeric as Numeric

# http://www.nabble.com/Chord-player-td21350708.html
def getCTCSS(tone, sampleRate=44100, peak=0.9):
    if tone in CTCSSTones:
        tone = CTCSSTones[tone]
    length = sampleRate / float(tone)
    omega = Numeric.pi * 2 / length
    xvalues = Numeric.arange(int(length)) * omega
    oneCycle =  ((peak * 32767) * Numeric.sin(xvalues)).astype(Numeric.Int16)
    return Numeric.transpose(Numeric.array((oneCycle,oneCycle)))


def main():
    import pygame
    pygame.mixer.pre_init(44100,-16,2,1024)
    pygame.mixer.init(44100,-16,2,1024)
    #pygame.init()
    print "Testing CTCSS capability"
    for tone in sorted(CTCSSTones.keys()):
        print "Tone %s, %s Hz..."%(tone,CTCSSTones[tone])
        s= pygame.sndarray.make_sound(getCTCSS(CTCSSTones[tone]))
        c=s.play(300)
        while c.get_busy():
            pygame.time.wait(25)

if __name__ == '__main__': main()
