#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file clImaOs.py
## \brief Čištění systému a obrazu
from ConsSys import ConsSys
import socket
import time
import shutil
import subprocess
import os
from optparse import OptionParser

class clImaOs:
	""" \brief Třída s metodami pro úklid systému
	"""
	def __init__(self):
		""" Konstruktor třídy okna
		\param self Ukazatel na objekt
		"""
		## Instance objektu pro práci se systémem
		self.sy=ConsSys()
	def cleanImage(self):
		""" Čištění obrazu
		\param self Ukazatel na objekt
		"""
		self.sy.removeFl("/NFSROOT/class/addons/cleanApt.sh")
		tar = open ("/NFSROOT/class/addons/cleanApt.sh", 'a')
		tar.write("#!/bin/bash\n")
		tar.write("apt-get autoclean\n")
		tar.write("apt-get clean\n")
		tar.close()
		os.chmod("/NFSROOT/class/addons/cleanApt.sh",0755)
		tos="chroot /NFSROOT/class /bin/bash -c ./addons/cleanApt.sh"
		for line in self.sy.runProcess(tos):
			print line,	
	def cleanSystem(self):
		""" Čištění hostovského systému
		\param self Ukazatel na objekt
		"""
		for line in self.sy.runProcess("apt-get autoclean"):
			print line,

if __name__ == "__main__":
	## Parser argumentů a parametrů
	parser = OptionParser(usage="usage: %prog [args]\n Serve for cleaning up apt")
	parser.add_option("-c", "--clean-image", action="store_true", dest="cleanIm", default=False, help="Clean client image")
	parser.add_option("-C", "--clean-system", action="store_true", dest="cleanSy", default=False, help="Clean host")
	## Argumenty a parametry z parseru
	(args, opts) = parser.parse_args()
	## Instance objektu
	cl=clImaOs()
	if args.cleanSy == True:
		cl.cleanSystem()
	if args.cleanIm == True:
		cl.cleanImage()
	