#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file ParConfFl.py
## \brief Třída pro načítání konfiguračních souborů

import os

class ParConfFl:
	""" \brief Třída obsahující metody s prací s načítáním konfiguračních souborů
	"""
	def getInterfaces(self):
		""" Metoda vrací slovník obsahující vstupní a výstupní zařízení
		\param self Ukazatel na objekt
		\return Slovník s in rozhraním a out rozhraním
		"""
		if os.path.isfile("./configuration/interfaces") == False:
			return None
		ret=dict()
		fii=open("./configuration/interfaces","r").readlines()
		for ln in fii:
			crs=ln.find("#")
			line=ln[0:crs]
			ln=line.replace(" ","")
			fl=ln.split("=")
			if fl[0] == "in":
				ret['inti'] = fl[1]
			if fl[0] == "out":
				ret['outi'] = fl[1]
		return ret
	def setInterfaces(self,inti,outi):
		""" Metoda nastavující vstupní a výstupní zažízení v conf souboru
		\param self Ukazatel na objekt
		\param inti Vstupní zařízení
		\param outi Výstupní zařízení
		\return True pokud vše proběhlo v pořádku, False pokud ne
		"""
		if inti == "" or outi == "":
			return False
		if os.path.isfile("./configuration/interfaces") == False:
			return False
		fii=open("./configuration/interfaces","r").readlines()
		tmp=""
		for ln in fii:
			ln=ln.replace("\n","")
			line=ln.replace(" ","")
			fl=line.split("=")
			if fl[0] == "in":
				tmp = tmp + "in=" + inti + "\n"
			elif fl[0] == "out":
				tmp = tmp + "out=" + outi + "\n"
			else:
				tmp = tmp + ln + "\n"
		open("./configuration/interfaces","w").write(tmp)
		return True
if __name__ == "__main__":
	print("Jen pro import")