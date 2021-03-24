# -*- coding: utf-8 -*-

import unittest
from six import u
from kwotaslownie import kwotaslownie


class TestKwotaSlownie(unittest.TestCase):
    """Klasa testów jednostkowych pakietu pyliczba"""
    def test_jednosci_bez_groszy(self):
        """Test wartości jednostkowych złotych"""
        jednosci_bez_groszy = {
            0.00: u("zero złotych 0/100"),
            1.00: u("jeden złoty 0/100"),
            2.00: u("dwa złote 0/100"),
            3.00: u("trzy złote 0/100"),
            4.00: u("cztery złote 0/100"),
            5.00: u("pięć złotych 0/100"),
            6.00: u("sześć złotych 0/100"),
            7.00: u("siedem złotych 0/100"),
            8.00: u("osiem złotych 0/100"),
            9.00: u("dziewięć złotych 0/100"),
        }
        for kwota, spodziewana in jednosci_bez_groszy.items():
            self.assertEqual(kwotaslownie(kwota), spodziewana)

    def test_nastki_bez_groszy(self):
        """Test wartości nastu (10-19) złotych"""
        nastki_bez_groszy = {
            10.00: u("dziesięć złotych 0/100"),
            11.00: u("jedenaście złotych 0/100"),
            12.00: u("dwanaście złotych 0/100"),
            13.00: u("trzynaście złotych 0/100"),
            14.00: u("czternaście złotych 0/100"),
            15.00: u("piętnaście złotych 0/100"),
            16.00: u("szesnaście złotych 0/100"),
            17.00: u("siedemnaście złotych 0/100"),
            18.00: u("osiemnaście złotych 0/100"),
            19.00: u("dziewiętnaście złotych 0/100"),
        }
        for kwota, spodziewana in nastki_bez_groszy.items():
            self.assertEqual(kwotaslownie(kwota), spodziewana)

    def test_dziesiatki_bez_groszy(self):
        """Test dziesiątek złotych"""
        dziesiatki_bez_groszy = {
            20.00: u("dwadzieścia złotych 0/100"),
            30.00: u("trzydzieści złotych 0/100"),
            40.00: u("czterdzieści złotych 0/100"),
            50.00: u("pięćdziesiąt złotych 0/100"),
            60.00: u("sześćdziesiąt złotych 0/100"),
            70.00: u("siedemdziesiąt złotych 0/100"),
            80.00: u("osiemdziesiąt złotych 0/100"),
            90.00: u("dziewięćdziesiąt złotych 0/100"),
        }
        for kwota, spodziewana in dziesiatki_bez_groszy.items():
            self.assertEqual(kwotaslownie(kwota), spodziewana)

    def test_setki_bez_groszy(self):
        """Test setek złotych"""
        setki_bez_groszy = {
            100.00: u("sto złotych 0/100"),
            200.00: u("dwieście złotych 0/100"),
            300.00: u("trzysta złotych 0/100"),
            400.00: u("czterysta złotych 0/100"),
            500.00: u("pięćset złotych 0/100"),
            600.00: u("sześćset złotych 0/100"),
            700.00: u("siedemset złotych 0/100"),
            800.00: u("osiemset złotych 0/100"),
            900.00: u("dziewięćset złotych 0/100"),
        }
        for kwota, spodziewana in setki_bez_groszy.items():
            self.assertEqual(kwotaslownie(kwota), spodziewana)

    def test_tysiace_bez_groszy(self):
        """Test tysięcy złotych"""
        tysiace_bez_groszy = {
            1000.00: u("jeden tysiąc złotych 0/100"),
            2000.00: u("dwa tysiące złotych 0/100"),
            3000.00: u("trzy tysiące złotych 0/100"),
            4000.00: u("cztery tysiące złotych 0/100"),
            5000.00: u("pięć tysięcy złotych 0/100"),
            6000.00: u("sześć tysięcy złotych 0/100"),
            7000.00: u("siedem tysięcy złotych 0/100"),
            8000.00: u("osiem tysięcy złotych 0/100"),
            9000.00: u("dziewięć tysięcy złotych 0/100"),
            11000.00: u("jedenaście tysięcy złotych 0/100"),
            30000.00: u("trzydzieści tysięcy złotych 0/100"),
            100000.00: u("sto tysięcy złotych 0/100"),
            300000.00: u("trzysta tysięcy złotych 0/100"),
        }
        for kwota, spodziewana in tysiace_bez_groszy.items():
            self.assertEqual(kwotaslownie(kwota), spodziewana)

    def test_miliony_bez_groszy(self):
        """Test milionów złotych"""
        miliony_bez_groszy = {
            1000000.00: u("jeden milion złotych 0/100"),
            2000000.00: u("dwa miliony złotych 0/100"),
            5000000.00: u("pięć milionów złotych 0/100"),
            11000000.00: u("jedenaście milionów złotych 0/100"),
            30000000.00: u("trzydzieści milionów złotych 0/100"),
            100000000.00: u("sto milionów złotych 0/100"),
        }
        for kwota, spodziewana in miliony_bez_groszy.items():
            self.assertEqual(kwotaslownie(kwota), spodziewana)

    def test_jeden_na_koncu_bez_groszy(self):
        """Test kwot z jedynką na końcu, bez groszy"""
        jeden_na_koncu_bez_groszy = {
            31.00: u("trzydzieści jeden złotych 0/100"),
            71.00: u("siedemdziesiąt jeden złotych 0/100"),
            101.00: u("sto jeden złotych 0/100"),
            301.00: u("trzysta jeden złotych 0/100"),
            701.00: u("siedemset jeden złotych 0/100"),
            1001.00: u("jeden tysiąc jeden złotych 0/100"),
            3001.00: u("trzy tysiące jeden złotych 0/100"),
            7001.00: u("siedem tysięcy jeden złotych 0/100"),
            14001.00: u("czternaście tysięcy jeden złotych 0/100"),
            1000001.00: u("jeden milion jeden złotych 0/100"),
        }
        for kwota, spodziewana in jeden_na_koncu_bez_groszy.items():
            self.assertEqual(kwotaslownie(kwota), spodziewana)

    def test_trzy_na_koncu_bez_groszy(self):
        """Test kwot z trójką na końcu, bez groszy"""
        trzy_na_koncu_bez_groszy = {
            33.00: u("trzydzieści trzy złote 0/100"),
            73.00: u("siedemdziesiąt trzy złote 0/100"),
            103.00: u("sto trzy złote 0/100"),
            303.00: u("trzysta trzy złote 0/100"),
            703.00: u("siedemset trzy złote 0/100"),
            1003.00: u("jeden tysiąc trzy złote 0/100"),
            3003.00: u("trzy tysiące trzy złote 0/100"),
            7003.00: u("siedem tysięcy trzy złote 0/100"),
            14003.00: u("czternaście tysięcy trzy złote 0/100"),
            1000003.00: u("jeden milion trzy złote 0/100"),
        }
        for kwota, spodziewana in trzy_na_koncu_bez_groszy.items():
            self.assertEqual(kwotaslownie(kwota), spodziewana)

    def test_siedem_na_koncu_bez_groszy(self):
        """Test kwot z siódemką na końcu, bez groszy"""
        siedem_na_koncu_bez_groszy = {
            37.00: u("trzydzieści siedem złotych 0/100"),
            77.00: u("siedemdziesiąt siedem złotych 0/100"),
            107.00: u("sto siedem złotych 0/100"),
            307.00: u("trzysta siedem złotych 0/100"),
            707.00: u("siedemset siedem złotych 0/100"),
            1007.00: u("jeden tysiąc siedem złotych 0/100"),
            3007.00: u("trzy tysiące siedem złotych 0/100"),
            7007.00: u("siedem tysięcy siedem złotych 0/100"),
            14007.00: u("czternaście tysięcy siedem złotych 0/100"),
            1000007.00: u("jeden milion siedem złotych 0/100"),
        }
        for kwota, spodziewana in siedem_na_koncu_bez_groszy.items():
            self.assertEqual(kwotaslownie(kwota), spodziewana)

    def test_czternascie_na_koncu_bez_groszy(self):
        """Test kwot z czternastką na końcu, bez groszy"""
        czternascie_na_koncu_bez_groszy = {
            114.00: u("sto czternaście złotych 0/100"),
            314.00: u("trzysta czternaście złotych 0/100"),
            714.00: u("siedemset czternaście złotych 0/100"),
            1014.00: u("jeden tysiąc czternaście złotych 0/100"),
            3014.00: u("trzy tysiące czternaście złotych 0/100"),
            7014.00: u("siedem tysięcy czternaście złotych 0/100"),
            14014.00: u("czternaście tysięcy czternaście złotych 0/100"),
            1000014.00: u("jeden milion czternaście złotych 0/100"),
        }
        for kwota, spodziewana in czternascie_na_koncu_bez_groszy.items():
            self.assertEqual(kwotaslownie(kwota), spodziewana)

    def test_liczba_groszy_bez_odmiany(self):
        """Test kilku losowych kwot z groszami w formacie gr/100"""
        liczba_groszy_bez_odmiany = {
            0.01: u("zero złotych 1/100"),
            0.11: u("zero złotych 11/100"),
            1.11: u("jeden złoty 11/100"),
            1.95: u("jeden złoty 95/100"),
            0.25: u("zero złotych 25/100"),
            0.48: u("zero złotych 48/100"),
        }
        for kwota, spodziewana in liczba_groszy_bez_odmiany.items():
            self.assertEqual(kwotaslownie(kwota), spodziewana)

    def test_z_groszami(self):
        """Test przykładowych kwot z groszami słownie"""
        z_groszami = {
            1.00: u("jeden złoty zero groszy"),
            1.01: u("jeden złoty jeden grosz"),
            1.02: u("jeden złoty dwa grosze"),
            1.03: u("jeden złoty trzy grosze"),
            1.04: u("jeden złoty cztery grosze"),
            1.05: u("jeden złoty pięć groszy"),
            1.06: u("jeden złoty sześć groszy"),
            1.07: u("jeden złoty siedem groszy"),
            1.08: u("jeden złoty osiem groszy"),
            1.09: u("jeden złoty dziewięć groszy"),
            1.10: u("jeden złoty dziesięć groszy"),
            1.11: u("jeden złoty jedenaście groszy"),
            1.12: u("jeden złoty dwanaście groszy"),
            1.13: u("jeden złoty trzynaście groszy"),
            1.14: u("jeden złoty czternaście groszy"),
            1.15: u("jeden złoty piętnaście groszy"),
            1.16: u("jeden złoty szesnaście groszy"),
            1.17: u("jeden złoty siedemnaście groszy"),
            1.18: u("jeden złoty osiemnaście groszy"),
            1.19: u("jeden złoty dziewiętnaście groszy"),
            2.20: u("dwa złote dwadzieścia groszy"),
            2.30: u("dwa złote trzydzieści groszy"),
            2.31: u("dwa złote trzydzieści jeden groszy"),
            2.33: u("dwa złote trzydzieści trzy grosze"),
            2.40: u("dwa złote czterdzieści groszy"),
            2.50: u("dwa złote pięćdziesiąt groszy"),
            2.60: u("dwa złote sześćdziesiąt groszy"),
            2.70: u("dwa złote siedemdziesiąt groszy"),
            2.71: u("dwa złote siedemdziesiąt jeden groszy"),
            2.73: u("dwa złote siedemdziesiąt trzy grosze"),
            2.77: u("dwa złote siedemdziesiąt siedem groszy"),
            2.80: u("dwa złote osiemdziesiąt groszy"),
            2.90: u("dwa złote dziewięćdziesiąt groszy"),
        }

        for kwota, spodziewana in z_groszami.items():
            self.assertEqual(kwotaslownie(kwota, fmt=1), spodziewana)

if __name__ == '__main__':
    unittest.main()
