#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import logging
import requests
import xml.etree.ElementTree as ET

from sr0wx_module import SR0WXModule

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
}

TEXT_TYPES = (str, type(u""))


class CosmosWeatherSq9atk(SR0WXModule):

    def __init__(self, language, service_url, muf_url=None):
        self.__language = language
        self.__service_url = service_url
        self.__muf_url = muf_url
        self.__logger = logging.getLogger(__name__)
        self.__solar_xml = None   # cache sparsowanego XML-a hamqsl

    # ---------- Kp ----------

    def _extractKp(self, data):
        # od końca szukamy ostatniego wpisu z poprawną wartością
        for entry in reversed(data):
            try:
                if isinstance(entry, dict):      # aktualny format: lista obiektów
                    raw = entry.get("Kp", entry.get("kp"))
                else:                            # stary format: lista list (+ nagłówek)
                    raw = entry[1]
                return float(raw)
            except (TypeError, ValueError, KeyError, IndexError):
                continue                         # nagłówek / null / śmieci
        raise ValueError("Brak Kp w odpowiedzi")

    def getKp(self):
        self.__logger.info("::: Pobieram dane o pogodzie kosmicznej (Kp)...")
        try:
            resp = requests.get(self.__service_url, timeout=8, headers=HEADERS)
            if resp.status_code != 200:
                self.__logger.error("::: Błąd odpowiedzi HTTP (Kp) - %s" % resp.status_code)
                return None

            kp = int(round(self._extractKp(resp.json())))
            return kp

        except Exception as e:
            self.__logger.exception("::: Błąd pobierania Kp - %r" % e)
            return None

    # ---------- hamqsl (jeden request) ----------

    def _getSolarXml(self):
        if self.__solar_xml is not None:
            return self.__solar_xml
        if not self.__muf_url:
            return None

        self.__logger.info("::: Pobieram dane solardata (MUF/SFI)...")
        try:
            resp = requests.get(self.__muf_url, timeout=8, headers=HEADERS)
            if resp.status_code != 200:
                self.__logger.error("::: Błąd odpowiedzi HTTP (solardata) - %s" % resp.status_code)
                return None

            solar = ET.fromstring(resp.content).find("solardata")
            if solar is None:
                self.__logger.warning("::: Błąd pobranych danych")
                return None

            self.__solar_xml = solar
            return solar

        except Exception as e:
            self.__logger.exception("::: Błąd pobierania solardata - %r" % e)
            return None

    def _parseSolarValue(self, tag, min_val, max_val):
        solar = self._getSolarXml()
        if solar is None:
            return None

        raw = solar.findtext(tag)
        ##self.__logger.info("::: Surowa wartość %s: %r" % (tag, raw))

        try:
            value = int(round(float(raw.strip())))
        except (AttributeError, ValueError):  # brak pola, "NoRpt", "N/A", puste
            self.__logger.warning("::: Brak poprawnej wartości %s" % tag)
            return None

        if not min_val <= value <= max_val:   # 0, śmieci
            return None
        return value

    def getMuf(self):
        return self._parseSolarValue("muf", 1, 99)

    def getSolarflux(self):
        return self._parseSolarValue("solarflux", 30, 400)



    def readMuf(self, muf):
        """Liczba jako ciąg próbek. Jednostka siedzi w osobnej próbce,
        więc nie trzeba odmieniać."""
        reader = getattr(self.__language, 'read_number', None)
        if reader is not None:
            try:
                result = reader(muf)
                if isinstance(result, TEXT_TYPES) and result.strip():
                    return result
            except Exception as e:
                self.__logger.warning("::: read_number nie zadziałało - %r" % e)


        return " ".join(str(muf))

    # ---------- komunikat ----------

    def get_data(self):
        kp = self.getKp()

        muf = self.getMuf()
        sfi = self.getSolarflux()
        self.__solar_xml = None

        self.__logger.info("::: Przetwarzam dane...\n")

        parts = []
        if kp is not None:
            parts += ["indeks_ka_pe", str(kp), " _ "]
        if sfi is not None:
            parts += ["indeks_solar_flux", self.readMuf(sfi), " _ "]
        if muf is not None:
            parts += ["muf_w_megahercach", self.readMuf(muf), " _ "]

        message = ""
        if parts:
            message = " ".join([" _ ", "pogoda_kosmiczna", " _ "] + parts)

        return {
            "message": message,
            "source": "noaa_swpc",
        }
