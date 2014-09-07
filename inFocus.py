#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
## \file inFocus.py
## \brief Řeší instalaci a odinstalaci balíčků

from ConsSys import ConsSys
from LogWrk import LogWrk
import os

class inFocus:
	""" \brief Třída obsahující metody pro instalaci programů do obrazu
	"""
	def __init__(self,path="/NFSROOT/class/addons/instFoc/"):
		""" Konstruktor třídy okna
		\param self Ukazatel na objekt
		\param path Cesta k instalačním skriptů
		"""
		## Instance systémových nástrojů
		self.sy=ConsSys()
		## Cesta k instalačním skriptům
		self.path=path
		self.sy.makeDir(path)
		## Logovací třída
		self.log=LogWrk()
	def exCom(self,comm):
		""" Vykonej příkaz z comm
		\param comm Příkaz k vychování
		\param self Ukazatel na objekt
		"""
		name=comm.replace(" ","")
		nm = self.path + name +".sh"
		self.sy.removeFl(nm)
		tar = open (nm, 'a')
		tar.write("#!/bin/bash\n")
		tar.write("export DEBIAN_FRONTEND=noninteractive\n")
		tar.write(comm + "\n")
		tar.close()
		os.chmod(nm,0755)
		tos="chroot /NFSROOT/class /bin/bash -c ./addons/instFoc/" + name + ".sh"
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
	def dpkgConfA(self):
		""" Oprav konfigurace balíčků
		\param self Ukazatel na objekt
		"""
		nm = self.path + "/clearConf.sh"
		self.sy.removeFl(nm)
		tar = open (nm, 'a')
		tar.write("#!/bin/bash\n")
		tar.write("export DEBIAN_FRONTEND=noninteractive\n")
		tar.write("dpkg --configure -a\n")
		tar.write("apt-get autoclean\n")
		tar.write("apt-get install -f\n")
		tar.close()
		os.chmod(nm,0755)
		tos="chroot /NFSROOT/class /bin/bash -c ./addons/instFoc/clearConf.sh"
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
	def aptAutorem(self):
		""" Autoremove balíčků z obrazu
		\param self Ukazatel na objekt
		"""
		nm = self.path + "/autorem.sh"
		self.sy.removeFl(nm)
		tar = open (nm, 'a')
		tar.write("#!/bin/bash\n")
		tar.write("export DEBIAN_FRONTEND=noninteractive\n")
		tar.write("apt-get autoremove -y\n")
		tar.close()
		os.chmod(nm,0755)
		tos="chroot /NFSROOT/class /bin/bash -c ./addons/instFoc/autorem.sh"
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
	def uniXmlCo(self,name):
		""" Upravení installed souboru, kde jsou zapsány instalované účely
		\param self Ukazatel na objekt
		\param name Jméno odinstalovaného účelu
		"""
		ts=""
		for line in open("./focus/installed.cfg"):
			inm=line.replace("\n","")
			if inm==name:
				continue
			else:
				ts = ts + line
		tar = open ("./focus/installed.cfg", 'w')
		tar.write(ts) 
		tar.close()
	def instXmlCo(self,name):
		""" Upravení installed souboru, kde jsou zapsány instalované účely
		\param self Ukazatel na objekt
		\param name Jméno instalovaného účelu
		"""
		ts=""
		for line in open("./focus/installed.cfg"):
			inm=line.replace("\n","")
			if inm==name:
				return
			else:
				ts = ts + line
		ts = ts + "\n" + name
		tar = open ("./focus/installed.cfg", 'w')
		tar.write(ts) 
		tar.close()
	def getLstInst(self):
		""" Přečtení listu instalovaných účelů
		\param self Ukazatel na objekt
		"""
		ts=[]
		for line in open("./focus/installed.cfg"):
			ln=line.replace("\n","").replace(" ","")
			if ln == "":
				continue
			if ln.split(".")[1] == "gml":
				ts.append(ln)
		return ts
if __name__ == "__main__":
	print("Jen pro import")