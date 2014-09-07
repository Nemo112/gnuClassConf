#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file DhcpCheck.py
## \brief Třída pro kontrolu dhcp serveru
import time
import os

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
	print("Jen pro import")