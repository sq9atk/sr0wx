# -*- coding: utf-8 -*-

from six import u

"""Liczba słownie.

kwotaslownie - kwota słownie ("sto pięć złotych 3 grosze")
lslownie - liczba slownie ("dwieście dwadzieścia trzy")
cosslownie - rzecz słownie, odmiana jako argument ("dwadzieścia niedźwiedzi")
"""

JEDNOSTKI = [u(""), u("jeden"), u("dwa"), u("trzy"), u("cztery"), u("pięć"),
        u("sześć"), u("siedem"), u("osiem"), u("dziewięć")]
DZIESIATKI = [u(""), u("dziesięć"), u("dwadzieścia"), u("trzydzieści"),
        u("czterdzieści"), u("pięćdziesiąt"), u("sześćdziesiąt"),
        u("siedemdziesiąt"), u("osiemdziesiąt"), u("dziewięćdziesiąt")]
NASTKI = [u("dziesięć"), u("jedenaście"), u("dwanaście"), u("trzynaście"),
        u("czternaście"), u("piętnaście"), u("szesnaście"), u("siedemnaście"),
        u("osiemnaście"), u("dziewiętnaście")]
SETKI = [u(""), u("sto"), u("dwieście"), u("trzysta"), u("czterysta"),
        u("pięćset"), u("sześćset"), u("siedemset"), u("osiemset"),
        u("dziewięćset")]

WIELKIE = [
        [u("x"), u("x"), u("x")],
        [u("tysiąc"), u("tysiące"), u("tysięcy")],
        [u("milion"), u("miliony"), u("milionów")],
        [u("miliard"), u("miliardy"), u("miliardów")],
        [u("bilion"), u("biliony"), u("bilionów")],
    ]

ZLOTOWKI = [u("złoty"), u("złote"), u("złotych")]
GROSZE = [u("grosz"), u("grosze"), u("groszy")]


def _slownie3cyfry(liczba):
    je = liczba % 10
    dz = (liczba // 10) % 10
    se = (liczba // 100) % 10
    slowa = []

    if se > 0:
        slowa.append(SETKI[se])
    if dz == 1:
        slowa.append(NASTKI[je])
    else:
        if dz > 0:
            slowa.append(DZIESIATKI[dz])
        if je > 0:
            slowa.append(JEDNOSTKI[je])
    retval = u(" ").join(slowa)
    return retval


def _przypadek(liczba):
    je = liczba % 10
    dz = (liczba // 10) % 10

    if liczba == 1:
        typ = 0  # jeden tysiąc"
    elif dz == 1 and je > 1:  # naście tysięcy
        typ = 2
    elif 2 <= je <= 4:
        typ = 1  # [k-dziesiąt/set] [dwa/trzy/czery] tysiące
    else:
        typ = 2  # x tysięcy

    return typ


def lslownie(liczba):
    """Liczba całkowita słownie"""
    trojki = []
    if liczba == 0:
        return u("zero")
    while liczba > 0:
        trojki.append(liczba % 1000)
        liczba = liczba // 1000
    slowa = []
    for i, n in enumerate(trojki):
        if n > 0:
            if i > 0:
                p = _przypadek(n)
                w = WIELKIE[i][p]
                slowa.append(_slownie3cyfry(n) + u(" ") + w)
            else:
                slowa.append(_slownie3cyfry(n))
    slowa.reverse()
    return u(" ").join(slowa)


def cosslownie(liczba, cos):
    """Słownie "ileś cosiów"

    liczba - int
    cos - tablica przypadków [coś, cosie, cosiów]"""

    return lslownie(liczba) + u(" ") + cos[_przypadek(liczba)]


def kwotaslownie(liczba, fmt=0):
    """Słownie złotych, groszy.

    liczba - float, liczba złotych z groszami po przecinku
    fmt - (format) jesli 0, to grosze w postaci xx/100, słownie w p. przypadku
    """
    lzlotych = int(liczba)
    lgroszy = int(liczba * 100 + 0.5) % 100
    if fmt != 0:
        groszslownie = cosslownie(lgroszy, GROSZE)
    else:
        groszslownie = u("%d/100") % lgroszy
    return cosslownie(lzlotych, ZLOTOWKI) + u(" ") + groszslownie
