#!/usr/bin/python
# -*- coding: utf-8 -*-
# \file main.py
# \brief Spouštěč pro aplikaci, testuje, zdali je nainstalován python-tk a pokud ano, spustí

import os.path
import subprocess


def runProcess(exe):
    """ Metoda spouštějící vnější příkazy systému
    \param exe String obsahující příkaz
    \return Yielduje postupně řádek po řádku vykonávaného příkazu
    """
    exe = exe.split()
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while(True):
        retcode = p.poll()
        line = p.stdout.readline()
        yield line
        if(retcode is not None):
            break


class Chdir:

    """ \brief Třída sloužící pro přepínání pracovní cesty aplikace
    """

    def __init__(self, newPath):
        """ Konstruktor třídy pro změnu cesty
        \param self Ukazatel na objekt
        \param newPath Nová cesta
        """
        # Uložená cesta
        self.savedPath = os.getcwd()
        os.chdir(newPath)

    def __del__(self):
        """ Destruktor třídy pro změnu cesty, změní jí zpátky na uloženou cestu
        \param self Ukazatel na objekt
        """
        os.chdir(self.savedPath)

if __name__ == "__main__":
    # Instance změny cesty
    cd = Chdir("/opt/gnuClassConf/")
    if os.path.isfile("/usr/share/doc/python-tk/README.Tk"):
        # Výsledek subprocesu
        bc = subprocess.call("./mnWindow.py", shell=True)
    else:
        print("Zřejmě chybí Python-TK, mám jej zkusit nainstalovat...")
        # Výsledek volby uživatele
        var = raw_input("Zvolte ano(a)/ne(n): ")
        # Oseknutí na jedno písmeno
        d = str(var)[0]
        if d == "a":
            for line in runProcess("apt-get install python-tk -y"):
                print line,
            bc = subprocess.call("./mnWindow.py", shell=True)
        else:
            exit(2)
    exit(bc)


##
# \mainpage Úvod k dokumentaci
# Tato dokumentace slouží k popisu zdrojového kódu "GNUškola konfigurační prostředí".
# Obsahuje soupis tříd a souborů třídy obsahující.
# Pomocí této dokumentace by mělo být možné zorientovat se v kódu a dále jej rozšiřovat.
# U každé třídy jsou zapsány její metody a veřejné atributy. Metoda má popsanou hlavičku vstupních proměnných.
##
# \section Spuštění
# Řádné spuštění aplikace probíhá pomocí spuštění skriptu ./main.py.
# Aplikace spoléhá, že její umístění je v /opt/gnuClassConf/, pokud tomu tak není, může dojít k problémům.
##
# \section Požadavky
# Pro vývoj je potřeba jakékoliv textové IDE. Pokud spuštíte projekt z obrazu, nalézá se v systému Scite.
# Vývoj je určen pro systém Debian verze 7 s instalací Python verze 2.7.3.
##
# \section Doxypy
# Projekt používá pro Doxygen nástavbu Doxypy. jako filtr načítání součástí Pythonu do Doxygenu.
# Doxypy se nachází ve složce ./doxypy.
##
# \section Dodatek
# Projekt je vyvíjen pod licencí GNU/GPL. Toto je nultá vývojová verze.
##
# \section Kontakt
# Vývoj je ve správě martin.beranek112@gmail.com
##
