#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file ShrFol.py
## \brief Třída s metodami pro sdílení souborů do obrazu klientských počítačů

from ConsSys import ConsSys
from LogWrk import LogWrk
import os
import subprocess

class ShrFol:
	""" \brief Třída s metodami pro sdílení souborů do obrazu klientských počítačů
	"""
	def __init__(self,pth="./configuration/shared"):
		""" Konstruktor třídy okna
		\param self Ukazatel na objekt
		\param pth Cesta k souboru listu sdílených složek
		"""
		## Cesta ke konfiguračnímu souboru
		self.path=pth
		## Logovací třída
		self.log=LogWrk()
		## Instance třídy pro práci se systémem
		self.sy=ConsSys()
	def shList(self):
		""" Vrací list sdílených složek
		\param self Ukazatel na objekt
		\return List sdílených složek
		"""
		toR=[]
		if os.path.isfile(self.path):
			fl=open(self.path,"r")
			cnt=fl.read()
			for line in cnt.split("\n"):
				tl=line.find("#")
				if tl == -1:
					tr=line
				else:
					tr=line[0:tl]
				if tr.replace(" ","") != "":
					toR.append(tr)
			fl.close()
		else:
			return
		return toR
	def addToList(self,add):
		""" Přidá na list sdílení složku
		\param self Ukazatel na objekt
		\param add String obsahující cestu ke složce
		\return True pokud složka existuje a je přidána, jinak False
		"""
		if add in self.shList():
			return
		if os.path.isfile(self.path):
			if os.path.isdir(add):
				fl=open(self.path,"a")
				fl.write(add + "\n")
				fl.close()
		else:
			return
	def uMntLst(self,dele):
		""" Odebere mount složky a smaže jí
		\param self Ukazatel na objekt
		\param dele String obsahující jméno složky k odstranění
		"""
		nm=dele.split("/")[-1]
		if os.path.isdir("/NFSROOT/class/class_shares/" + nm):
			exe=["umount","/NFSROOT/class/class_shares/" + nm + ""]
			p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			exe=["rm","-r","/NFSROOT/class/class_shares/" + nm + ""]
			p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	def remFrList(self,dele):
		""" Odebere z listu sdílených složek
		\param self Ukazatel na objekt
		\param dele String obsahující jméno složky k odstranění
		"""
		if dele in self.shList():
			if os.path.isfile(self.path):
				fl=open(self.path,"r")
				cnt=fl.read()
				fl.close()
				ts=""
				for ln in cnt.split("\n"):
					if len(ln) > 0 and ln[0] == "#":
						ts = ts + ln + "\n"
						continue
					if dele != ln:
						ts = ts + ln + "\n"
				fl=open(self.path,"w")
				cnt=fl.write(ts)
				fl.close()
		else:
			return
	def genListSh(self):
		""" Vygeneruje dávku pro sdílení složek do obrazu
		\param self Ukazatel na objekt
		"""
		lst=self.shList()
		if not os.path.isdir("/NFSROOT/class/class_shares"):
			os.makedirs("/NFSROOT/class/class_shares")
		tos = "#!/bin/bash\n"
		for it in lst:
			nm = it.split("/")[-1]
			if not os.path.isdir("/NFSROOT/class/class_shares/" + nm):
				os.makedirs("/NFSROOT/class/class_shares/" + nm)
			tos = tos + "mount -o rbind \"" + it + "\" \"/NFSROOT/class/class_shares/" + nm  + "\" " + ";\n"
		tos = tos + "exit 0;\n"
		fl=open("./tmpba/mntGen.sh","w")
		fl.write(tos)
		fl.close()
		os.chmod("./tmpba/mntGen.sh",0755)
	def addShRc(self):
		""" Přidá odkaz na skript sdílející složky do rc.local hostovské stanice
		\param self Ukazatel na objekt
		"""
		with open("/etc/rc.local",'r') as cont:
			cnl=cont.read()
		obs=""
		for line in cnl.split("\n"):
			if "/opt/gnuClassConf/tmpba/mntGen.sh;" in line:
				return
			if "exit 0" == line:
				break
			obs = obs + line  + "\n"
		obs = obs + "/opt/gnuClassConf/tmpba/mntGen.sh;\n"
		obs = obs + "exit 0\n"
		tar = open ("/etc/rc.local", 'w')
		tar.write(obs)
		tar.close()
	def expShrs(self):
		""" Nasdílí složky z ./tmpba/mntGen.sh
		\param self Ukazatel na objekt
		"""
		for line in self.sy.runProcess("./tmpba/mntGen.sh"):
			print line,
			self.log.write(line)
	def intrCli(self):
		""" Připraví klienta pro práci se sdílením
		\param self Ukazatel na objekt
		"""
		# vytvoří složku sdílení pokud neexistuje
		if not os.path.isdir("/NFSROOT/class/class_shares"):
			os.makedirs("/NFSROOT/class/class_shares")
			os.chmod("/NFSROOT/class/class_shares",0755)
		# zkopíruje dávku přidávající odkaz na složku sdílení na plochu
		self.sy.removeFl("/NFSROOT/class/addons/mkLnk.sh")
		self.sy.copyLargeFile("./data/mkLnk.sh","/NFSROOT/class/addons/mkLnk.sh")
		os.chmod("/NFSROOT/class/addons/mkLnk.sh",0755)
		# přidá na ní odkaz do rc.local
		with open("/NFSROOT/class/etc/rc.local",'r') as cont:
			cnl=cont.read()
		obs=""
		for line in cnl.split("\n"):
			if "/addons/mkLnk.sh;" in line:
				return
			if "exit 0" == line:
				break
			obs = obs + line  + "\n"
		obs = obs + "/addons/mkLnk.sh;\n"
		obs = obs + "exit 0\n"
		tar = open ("/NFSROOT/class/etc/rc.local", 'w')
		tar.write(obs)
		tar.close()
if __name__ == "__main__":
	print("Jen pro import")
	#sh=ShrFol()
	#sh.addToList("/prd")
	#sh.addToList("/home")
	#print sh.shList()
	#sh.remFrList("/home")
	#print sh.shList()
	#sh.genListSh()
	#sh.intrCli()
	
