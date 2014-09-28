#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file FsSize.py
## \brief Metody pro kontroly velikosti klientského souborového systému

import os

class FsSize:
	""" \brief Metody pro kontroly velikosti klientského souborového systému	
	"""
	def __init__(self,pth="/NFSROOT"):
		""" Konstruktor
		\param self Ukazatel na objekt
		\param pth Cesta k měřenému souborovému systému
		"""
		if os.path.isdir(pth) == False:
			raise IOError(pth + " nenalezeno!")
		## Stav zkoumaného fs
		self.pth=pth
	def getSize(self):
		""" Metoda pro vrácení velikosti souborového systému
		\param self Ukazatel na objekt
		\return Velikost souborového systému
		"""
		self.statvfs = os.statvfs(self.pth)
		return (self.statvfs.f_frsize * self.statvfs.f_blocks)
	def getFull(self):
		""" Metoda pro vrácení velikosti zabraného souborového systému
		\param self Ukazatel na objekt
		\return Velikost zabraného souborového systému
		"""
		self.statvfs = os.statvfs(self.pth)
		return self.getSize() - (self.statvfs.f_frsize * self.statvfs.f_bfree)