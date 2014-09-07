#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file ConsSys.py
## \brief Třída, která sprostředkovává přístup k systému
import string
import re
import subprocess
import socket
import struct
from Queue import Empty, Full
import fcntl
import urllib2
import shutil
import os
import tarfile
import hashlib
import crypt

class ConsSys:
	""" 
	\brief Třída obsahující funkce pro práci se systémem.
	Obsahuje ucelenou formu pro práci s prostředky jako ip,
	spouštěče ostatních skriptů a další, ...
	"""
	def erAll(self):
		""" 
		Metoda vymaže obraz a záznam o instalovaném software
		\param self Ukazatel na objekt
		"""
		# smazat obraz
		shutil.rmtree("/NFSROOT/class")
		# přemáznout instalovaný seznam ve focus
		open('./focus/installed.cfg','w').close()
	def updateImg(self):
		""" 
		Metoda aktualizuje obraz třídy
		\param self Ukazatel na objekt
		"""
		self.removeFl("/NFSROOT/class/addons/updateApt.sh")
		tar = open ("/NFSROOT/class/addons/updateApt.sh", 'a')
		tar.write("#!/bin/bash\n")
		tar.write("apt-get update\n")
		tar.write("apt-get upgrade -y\n")
		tar.close()
		os.chmod("/NFSROOT/class/addons/updateApt.sh",0755)
		tos="chroot /NFSROOT/class /bin/bash -c ./addons/updateApt.sh"
		for line in self.runProcess(tos):
			print line,	
	def updateSys(self):
		""" 
		Aktualizace systému
		\param self Ukazatel na objekt
		"""
		for line in self.runProcess("apt-get update"):
			print line,
		for line in self.runProcess("apt-get upgrade -y"):
			print line,
	def serv(self):
		""" 
		Metoda spouštějící skript ukazující služby
		\param self Ukazatel na objekt
		"""
		subprocess.Popen("./testsServices.py", shell=True)
	def sets(self):
		""" Metoda spouštějící skript ukazující nastavení služeb
		\param self Ukazatel na objekt
		"""
		subprocess.Popen("./testsConf.py", shell=True)
	def runProcess(self,exe):
		""" Metoda spouštějící vnější příkazy systému
		\param self Ukazatel na objekt
		\param exe String obsahující příkaz
		\return Yielduje postupně řádek po řádku vykonávaného příkazu
		"""
		exe=exe.split()    
		p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		while(True):
			retcode = p.poll()
			line = p.stdout.readline()
			yield line
			if(retcode is not None):
				break		
	def getEths(self):
		""" Metoda ze systému vytáhne jména eth zařízení a vrátí je v poli
		\param self Ukazatel na objekt
		\return Pole všech eth zařízení
		"""
		p = subprocess.Popen(["ip","link","show"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		k=re.compile("eth[0-9]+")
		r=k.finditer(p.communicate()[0])
		eths=()
		for i in r:
			eths = eths + (i.group(),)
		return eths
	def getEthIp(self,et):
		""" Metoda ze systému vytáhne ip adresy eth zařízení a vrátí je v txt
		\param self Ukazatel na objekt
		\param et String obsahující jméno eth zařízení
		\return String obsahující IP adresu
		"""
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			return socket.inet_ntoa(fcntl.ioctl(
				s.fileno(),
				0x8915,  # SIOCGIFADDR
				struct.pack('256s', et[:15])
			)[20:24])
		except:
			return ""
	def getDefGW(self):
		""" Metoda ze systému vytáhne ip adresy defaultní brány
		\param self Ukazatel na objekt
		\return String obsahující IP adresu brány
		"""
		with open("/proc/net/route") as fh:
			for line in fh:
				fields = line.strip().split()
				if fields[1] != '00000000' or not int(fields[3], 16) & 2:
					continue
				return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
	def getDnsSer(self):
		""" Metoda ze systému vytáhne ip adresy DNS serveru
		\param self Ukazatel na objekt
		\return String obsahující IP adresu DNS serveru
		"""
		with open("/etc/resolv.conf") as ln:
			for line in ln:
				if (line.split(' '))[0] == "nameserver":
					return (line.split(' '))[1].replace("\n","")
	def getNetmsk(self,ifname):
		""" Metoda ze systému vytáhne masku daného rozhraní
		\param self Ukazatel na objekt
		\param ifname Jméno rozhraní
		\return String obsahující masku rozhraní
		"""
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x891b, struct.pack('256s',ifname))[20:24])
		try:
			return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x891b, struct.pack('256s',ifname))[20:24])
		except:
			return ""
	def compIpByMask(self,mask,ipi,ipo):
		""" Metoda porovná dvě IP podle masky a řekne, zdali jsou ze stejné sítě
		\param self Ukazatel na objekt
		\param mask Maska pro porovnání 
		\param ipi První IP pro porovnání
		\param ipo Druhá IP pro porovnání
		\return True pokud platí, False pokud neplatí
		"""
		if mask == "" or ipi == "" or ipo == "":
			return False
		ms=mask.split(".")
		mi=ipi.split(".")
		mp=ipo.split(".")
		for i in range(0, 4):
			if  (int(ms[i]) & int(mi[i])) != (int(ms[i]) & int(mp[i])):
				return False
		return True
	def isCnt(self):
		""" Metoda testuje připojení počítače do sítě
		\param self Ukazatel na objekt
		\return True pokud je počítač připojen, False pokud není
		"""
		try:
			header = {"pragma" : "no-cache"}
			req = urllib2.Request("http://gnuskola.cz", headers=header)
			response=urllib2.urlopen(req,timeout=2)
			return True
		except urllib2.URLError as err:
			return False
	def copyLargeFile(self,src, dest, buffer_size=16000):
		""" Metoda testuje připojení počítače do sítě
		\param self Ukazatel na objekt
		\param src Jméno zdrojového souboru
		\param dest Jméno cílového souboru
		\param buffer_size Velikost kopírovacího bufferu
		"""
		with open(src, 'rb') as fsrc:
			with open(dest, 'wb') as fdest:
				shutil.copyfileobj(fsrc, fdest, buffer_size)
	def getNet(self,mask,sip):
		""" Metoda vrací string obsahující síť podle masky a IP adresy rozhraní
		\param self Ukazatel na objekt
		\param mask Maska sítě zadaná ve stringu
		\param sip Ip adresa sítě
		\return Ip adresa sítě
		"""
		nip = str(int(mask.split(".")[0]) & int(sip.split(".")[0]))
		for i in range(1,4):
			nip = nip + "." + str(int(mask.split(".")[i]) & int(sip.split(".")[i]))
		return nip
	def getBro(self,mask,sip):
		""" Metoda vrací string obsahující broadcast sítě podle masky a IP adresy rozhraní
		\param self Ukazatel na objekt
		\param mask Maska sítě zadaná ve stringu
		\param sip Ip adresa sítě
		\return Ip adresa sítě
		"""
		nip = str((int(mask.split(".")[0]) & int(sip.split(".")[0]))  +  (255-int(mask.split(".")[0])) )
		for i in range(1,4):
			nip = nip + "." + str((int(mask.split(".")[i]) & int(sip.split(".")[i]))   +  (255-int(mask.split(".")[i])) )
		return nip
	def makeDir(self,path):
		""" Metoda vytváří složku podle zadané cesty
		\param self Ukazatel na objekt
		\param path Cesta nové složky
		"""
		try:
			os.makedirs(path)
		except OSError:
			pass
	def removeFl(self,path):
		""" Metoda Smaže soubor podle zadané cesty
		\param self Ukazatel na objekt
		\param path Cesta na soubor
		"""
		try:
			os.remove(path)
		except OSError:
			try:
				shutil.rmtree(path)
			except:
				pass
	def chgPasswd(self,path,name,pasw,salt="class"):
		""" Metoda přepíše heslo uživatele
		\param self Ukazatel na objekt
		\param path Cesta na soubor formátu /etc/shadow
		\param name Jméno uživatele
		\param pasw Heslo uživatele
		\param salt Sůl k heslu
		"""
		tmp = ""
		for line in open(path):
			if line != "": 
				if name == line.split(":")[0]:
					li=line.split(":")
					npa=crypt.crypt(pasw,"$6$" + salt + "$")
					tmp = tmp + li[0] + ":" + npa + ":" + li[2] + ":" + li[3] + ":" + li[4]+ ":" + li[5] + ":" + li[6] + ":" + li[7] + ":" + li[8]
				else:
					tmp = tmp + line
		if tmp[-1] != "\n":
			tmp = tmp + "\n"
		f = open(path,"w")
		f.write(tmp)
		f.close()
	def getDfIlInt(self):
		""" Metoda vrátí vnitřní rozrhaní a vnější rozhraní
		\param self Ukazatel na objekt
		\return Vrací slovník, kde df je jméno vnějšího rozhraní a in je vnitřní rozhraní
		"""
		tor={}
		ets=self.getEths()	
		for i in ets:
			if self.compIpByMask(self.getNetmsk(i),self.getDefGW(),self.getEthIp(i)):
				tor['df']=i
			if self.getEthIp(i) == "192.168.111.1":
				tor['in']=i
		if tor['in'] is None:
			tor['in']=tor['df']
		return tor
	def extGzTar(self,who):
		""" Metoda rozbalí balíček jméno.tar.gz
		\param self Ukazatel na objekt
		\param who Cesta na zdrojový soubor
		"""
		tar = tarfile.open(who)
		tar.extractall()
		tar.close()
if __name__ == "__main__":
	print("Jen pro import")