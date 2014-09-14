#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file DhcpCheck.py
## \brief Třída pro kontrolu dhcp serveru
import time
import os
import sys
from optparse import OptionParser

class DhcpCheck:
	"""\brief Třída pro práci se souborem vypujčených IP adres
	"""
	def __init__(self,pthLs="/var/lib/dhcp/dhcpd.leases"):
		""" Konstruktor třídy okna
		\param self Ukazatel na objekt
		\param pthLs Cesta k souboru vypujčených adres
		"""
		## Cesta k propůjčeným adresám
		self.pathLease=pthLs
		## Obsah souboru propůjčených adres
		self.leasCont=""
		if os.path.isfile(pthLs) == False:
			return
		try:
			with open(pthLs,'r') as cont:
				self.leasCont=cont.read()
		except:
			return
	def chcNew(self):
		""" Kontroluje nově propůjčené IP adresy
		\param self Ukazatel na objekt
		"""
		try:
			with open(self.pathLease,'r') as cont:
				local=cont.read()
		except:
			local=""
		olcltns=[]
		clients=[]
		if local != self.leasCont:
			for line in self.leasCont.split("\n"):
				if line.split(" ")[0] == "lease":
					olcltns.append(line.split(" ")[1])
			for line in local.split("\n"):
				if line.split(" ")[0] == "lease" and line.split(" ")[1] not in olcltns:
					clients.append(line.split(" ")[1])
		try:
			with open(self.pathLease,'r') as cont:
				self.leasCont=cont.read()
		except:
			self.leasCont=""
		return clients
	def getClList(self):
		""" Načítá list klientů na DHCP serveru
		\param self Ukazatel na objekt
		"""
		clients=[]
		for line in self.leasCont.split("\n"):
			if line.split(" ")[0] == "lease":
				clients.append(line.split(" ")[1])
		return clients
	def getMacByIpDh(self,ip):
		""" Vrátí MAC adresu k IP adrese z tabulky propůjčených adres
		\param self Ukazatel na objekt
		\param ip Ip adresa pro vyhledání MAC adresy
		"""
		if ip=="":
			return
		lf=False
		for line in self.leasCont.split("\n"):
			if line.split(" ")[0] == "lease" and line.split(" ")[1] == ip:
				lf=True
			if lf == True:
				if "}" in line:
					lf = False
					continue
				if "hardware" in line:
					nln=" ".join(line.split())
					return nln.split(" ")[2].replace(";","")
if __name__ == "__main__":
	## Parser argumentů a parametrů
	parser = OptionParser(usage="usage: %prog [args]\n Serve for DHCP lists checks")
	parser.add_option("-p", "--print-list", action="store_true", dest="prDh", default=False, help="Says klients in DHCP list")
	parser.add_option("-m", "--get-mac", action="store", type="string", dest="mac", help="Says MAC from IP adress in DHCP lease file")
	## Argumenty a parametry z parseru
	(args, opts) = parser.parse_args()
	## Instance objektu
	dh=DhcpCheck()
	if args.prDh == True:
		for i in dh.getClList():
			print i
	if args.mac != "":
		## IP adresa z argumentu
		m=args.mac.split(".")
		if len(m) != 4:
			print "Error in IP given"
			sys.exit(2)
		for i in m:
			try:
				## Dekadické číslo IP adresy
				n=int(i)
			except:
				print "Error in IP given"
				sys.exit(2)				
			if n > 255 or n < 0:
				print "Error in IP given"
				sys.exit(2)
		print dh.getMacByIpDh(args.mac)