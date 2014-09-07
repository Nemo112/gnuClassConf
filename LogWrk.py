#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file LogWrk.py
## \brief Třída sloužící k zápisu do logu prostředí

import os
import datetime
import time

class LogWrk:
	""" \brief Třída obsahující metody s prací s logovacím souborem
	"""
	def __init__(self,path="./data/work_logs.log",timestp="[%H:%M:%S %d.%m.%Y]"):
		""" Konstruktor 
		\param self Ukazatel na objekt
		\param path Cesta k logu
		\param timestp Formát timestamp
		"""
		## Cesta k souboru logů
		self.path=path
		## Časové razítko bloků
		self.tmst=timestp
	def write(self,input):
		""" Konstruktor 
		\param self Ukazatel na objekt
		\param input Text do logu
		"""
		if input.replace("\n","").replace(" ","") == "":
			return
		if os.path.isfile(self.path) == False:
			return
		with open(self.path, "a") as myfile:
			tm=time.time()
			st = datetime.datetime.fromtimestamp(tm).strftime(self.tmst)
			myfile.write(st + "\n")
			myfile.write(input)
			myfile.write("\n++++++++++++++++++++++++++++++++++++++++++++\n")
if __name__ == "__main__":
	print("Jen pro import")