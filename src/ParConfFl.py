#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file ParConfFl.py
## \brief Třída pro načítání konfiguračních souborů

import os
from optparse import OptionParser

class ParConfFl:
	""" \brief Třída obsahující metody s prací s načítáním konfiguračních souborů
	"""
	def getTftp(self):
		""" Metoda vrací string obsahující cestu k pxelinux.0 v konfigruaci DHCP
		Cesta se mění pokud je ve virtualboxu či v reálu
		\param self Ukazatel na objekt
		\return String obsahující cestu
		"""
		if os.path.isfile("./configuration/tftpath") == False:
			return None
		ret=""
		fii=open("./configuration/tftpath","r").readlines()
		for ln in fii:
			crs=ln.find("#")
			line=ln[0:crs]
			ln=line.replace(" ","")
			fl=ln.split("=")
			if len(fl) == 2:
				if fl[0] == "path":
					ret = fl[1]
		return ret
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
			if len(fl) == 2:
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
	## Parser argumentů a parametrů
	parser = OptionParser(usage="usage: %prog [args]\n Parser for configuration file talking about interfaces")
	parser.add_option("-l", "--class-interfaces", action="store_true", dest="inn", default=False, help="Showing which interface is for class and which for outer connections")
	parser.add_option("-i", "--inner-interface", action="store", type="string", dest="inner", default="", help="Settting up for interface inside of class")
	parser.add_option("-o", "--outer-interface", action="store", type="string", dest="outer", default="", help="Settting up for interface outside of class")
	parser.add_option("-t", "--tft-path", action="store_true",  default=False, dest="tftp", help="Getting TFTP path for DHCP which is going to be used")
	## Argumenty a parametry z parseru
	(args, opts) = parser.parse_args()
	## Instance objektu
	pr=ParConfFl()
	if args.inn == True:
		print "Inner interface: " + pr.getInterfaces()['inti']
		print "Outer interface: " + pr.getInterfaces()['outi']
	if args.inner != "":
		pr.setInterfaces(args.inner,pr.getInterfaces()['outi'])
	if args.outer != "":
		pr.setInterfaces(pr.getInterfaces()['inti'],args.outer)
	if args.tftp == True:
		print pr.getTftp()
