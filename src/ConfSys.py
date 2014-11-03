#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file ConfSys.py
## \brief Nastavení systému pro potřeby aplikace
from ConsSys import ConsSys
import socket
import time
import shutil
import subprocess
import os
from LogWrk import LogWrk
from ShrFol import ShrFol
from optparse import OptionParser
from ParConfFl import ParConfFl

class ConfSys:
	""" \brief Třída obsahující metody pro nastavení systému
	Obsahuje metody pro nastavení systému.
	"""
	def __init__(self,ethc="eth0",rut=0):
		""" Konstruktor třídy okna
		\param self Ukazatel na objekt
		\param ethc Jaké rozhraní je použito pro třídu
		"""
		## Jaké rozhraní je použito pro třídu
		self.ethc=ethc
		## Instance třídy pro práci se systémem
		self.sy=ConsSys()
		## Rozhraní defaultní brány
		self.de=""
		if rut == 0:
			self.de = ethc
		if self.de == "":
			ets=self.sy.getEths()
			for i in ets:
				if self.sy.compIpByMask(self.sy.getNetmsk(i),self.sy.getDefGW(),self.sy.getEthIp(i)):
					self.de=i
		## Logovací třída
		self.log=LogWrk()
	def getDefGtw(self):
		""" Getter na bránu
		\param self Ukazatel na objekt
		"""
		return self.de
	def setUpNets(self):
		""" Nastavení síťových rozhraní v /etc/network/interfaces
		\param self Ukazatel na objekt
		"""
		eth=self.ethc
		de=self.de
		df=self.sy.getDefGW()
		self.sy.copyLargeFile("/etc/network/interfaces","/etc/network/interfaces_ducked_back")
		wsti = ""
		wsti = wsti + "auto lo\n"
		wsti = wsti + "iface lo inet loopback\n"
		wsti = wsti + "\n"
		wsti = wsti + "auto " + de + "\n"
		wsti = wsti + "iface " + de + " inet static\n"
		wsti = wsti + "\taddress " + self.sy.getEthIp(de) + "\n"
		wsti = wsti + "\tnetwork " + self.sy.getNet(self.sy.getNetmsk(de),self.sy.getEthIp(de)) + "\n"
		wsti = wsti + "\tnetmask " + self.sy.getNetmsk(de) + "\n"
		wsti = wsti + "\tbroadcast " + self.sy.getBro(self.sy.getNetmsk(de),self.sy.getEthIp(de)) + "\n"
		wsti = wsti + "\tdns-nameservers " + self.sy.getDnsSer() + "\n"
		wsti = wsti + "\tgateway " + self.sy.getDefGW() + "\n"
		# eth je rozhraní pro třídu a de pro vnější rozhraní
		tAddress=self.sy.getEthIp(de)
		if eth != self.de:
			wsti = wsti + "\n"
			wsti = wsti + "auto " + eth + "\n"
			wsti = wsti + "iface " + eth + " inet static\n"
			tAddress="192.168.111.1"
			wsti = wsti + "\taddress 192.168.111.1\n"
			wsti = wsti + "\tnetwork 192.168.111.0\n"
			wsti = wsti + "\tnetmask 255.255.255.0\n"
			wsti = wsti + "\tbroadcast 192.168.111.255\n"
		wsti = wsti + "# DUCKED changed\n"
		wsti = wsti + "# " + str(time.time()) + "\n"
		infile = open("/etc/network/interfaces",'w')
		infile.write(wsti)
		infile.close()
	def resetNet(self):
		""" Restart síťových služeb
		\param self Ukazatel na objekt
		"""
		if os.path.isfile("/etc/init.d/network-manager"):
			tos='/etc/init.d/network-manager stop'
			for line in self.sy.runProcess(tos):
				print line,
				self.log.write(line)
		tos='ifdown ' + self.ethc
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
		tos='ifup ' + self.ethc
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
		if self.ethc != self.de:
			tos='ifdown ' + self.de
			for line in self.sy.runProcess(tos):
				print line,
				self.log.write(line)
			tos='ifup ' + self.de
			for line in self.sy.runProcess(tos):
				print line,
				self.log.write(line)
		tos='/etc/init.d/networking restart'
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
	def setUpMasq(self):
		""" Nastavení NAT a maskarády
		\param self Ukazatel na objekt
		"""
		if self.ethc != self.de:
			tos="./masquarate.sh " + self.ethc + " " + self.de
			for line in self.sy.runProcess(tos):
				print line,
				self.log.write(line)
	def setUpDH(self):
		""" Nastavení DHCP
		\param self Ukazatel na objekt
		"""
		pr=ParConfFl()
		if pr.getTftp() == "virtualbox":
			if self.ethc != self.de:
				tfp="tftp://192.168.111.1/pxelinux.0"
			else:
				tfp="tftp://" + self.sy.getEthIp(self.de) + "/pxelinux.0"
		else:
			tfp = pr.getTftp()
		if self.ethc != self.de:
			self.sy.removeFl("/etc/dhcp/class.conf")
			tar = open ("/etc/dhcp/class.conf", 'a')
			tar.write("default-lease-time 600;\n")
			tar.write("max-lease-time 7200;\n")
			tar.write("allow booting;\n")
			tar.write("subnet 192.168.111.0 netmask 255.255.255.0 {\n")
			tar.write("\trange 192.168.111.10 192.168.111.250;\n")
			tar.write("\toption broadcast-address 192.168.111.255;\n")
			tar.write("\toption routers 192.168.111.1;\n")
			tar.write("\toption domain-name-servers " + self.sy.getDnsSer() + ";\n")
			tar.write("\tfilename \"" + tfp + "\";\n")
			tar.write("\tserver-name \"192.168.111.1\";\n")
			tar.write("\toption domain-name \"class\";\n")
			tar.write("\toption root-path \"/NFSROOT/class\";\n")
			tar.write("}\n")
			tar.write("# DUCKED changed\n")
			tar.close()
			os.chmod("/etc/dhcp/class.conf",0644)
			ch=False
			for line in open("/etc/dhcp/dhcpd.conf"):
				if "include \"/etc/dhcp/class.conf\";" in line:
					ch=True
			if ch == False:
				fd=open("/etc/dhcp/dhcpd.conf",'a')
				fd.write("\ninclude \"/etc/dhcp/class.conf\";\n")
				fd.write("# DUCKED changed \n")
		else:
			# hledám první adresu rozsahu
			sp=str(int(self.sy.getNet(self.sy.getNetmsk(self.de),self.sy.getEthIp(self.de)).split(".")[3])+10)
			lr=self.sy.getNet(self.sy.getNetmsk(self.de),self.sy.getEthIp(self.de)).split(".")
			fr=lr[0] + "." + lr[1] + "." + lr[2] + "." + sp
			# hledám poslední adresu rozsahu
			sp=str(int(self.sy.getBro(self.sy.getNetmsk(self.de),self.sy.getEthIp(self.de)).split(".")[3])-10)
			lr=self.sy.getBro(self.sy.getNetmsk(self.de),self.sy.getEthIp(self.de)).split(".")
			br=lr[0] + "." + lr[1] + "." + lr[2] + "." + sp
			# hotovo
			self.sy.removeFl("/etc/dhcp/class.conf")
			tar = open ("/etc/dhcp/class.conf", 'a')
			tar.write("default-lease-time 600;\n")
			tar.write("max-lease-time 7200;\n")
			tar.write("allow booting;\n")
			tar.write("subnet " + self.sy.getNet(self.sy.getNetmsk(self.de),self.sy.getEthIp(self.de)) + " netmask " + self.sy.getNetmsk(self.de) + " {\n")
			tar.write("\trange " + fr + " " + br + ";\n")
			tar.write("\toption broadcast-address " + self.sy.getBro(self.sy.getNetmsk(self.de),self.sy.getEthIp(self.de)) + ";\n")
			tar.write("\toption routers " + self.sy.getDefGW() + ";\n")
			tar.write("\toption domain-name-servers " + self.sy.getDnsSer() + " ;\n")
			tar.write("\tfilename \"" + tfp + "\";\n")
			tar.write("\tserver-name \"" + self.sy.getEthIp(self.de) + "\";\n")
			tar.write("\toption domain-name \"class\";\n")
			tar.write("\toption root-path \"/NFSROOT/class\";\n")
			tar.write("}\n")
			tar.write("# DUCKED changed\n")
			tar.close()
			os.chmod("/etc/dhcp/class.conf",0644)
			ch=False
			for line in open("/etc/dhcp/dhcpd.conf"):
				if "include \"/etc/dhcp/class.conf\";" in line:
					ch=True
			if ch == False:
				fd=open("/etc/dhcp/dhcpd.conf",'a')
				fd.write("\ninclude \"/etc/dhcp/class.conf\";\n")
				fd.write("# DUCKED changed \n")
				fd.close()
	def setUpHsn(self):
		""" Nastavení hostname klienta
		\param self Ukazatel na objekt
		"""
		with open("/NFSROOT/class/etc/rc.local",'r') as cont:
			cnl=cont.read()
		obs=""
		for line in cnl.split("\n"):
			if "/addons/chgHostname.sh;" in line:
				return
			if "exit 0" == line:
				break
			obs = obs + line  + "\n"
		obs = obs + "/addons/chgHostname.sh;\n"
		obs = obs + "exit 0\n"
		tar = open ("/NFSROOT/class/etc/rc.local", 'w')
		tar.write(obs)
		tar.close()
		self.sy.copyLargeFile("./data/chgHostname.sh","/NFSROOT/class/addons/chgHostname.sh")
		os.chmod("/NFSROOT/class/addons/chgHostname.sh",0755)
	def setUpNFS(self):
		""" Nastavení NFS
		\param self Ukazatel na objekt
		"""
		ch=False
		for line in open("/etc/exports"):
			if "/NFSROOT/class *(rw,crossmnt,sync,no_root_squash,no_subtree_check)" in line:
				ch=True
		if ch == False:
			fd=open("/etc/exports",'a')
			fd.write("/NFSROOT/class *(rw,crossmnt,sync,no_root_squash,no_subtree_check)\n")
			fd.write("# DUCKED changed \n")
			fd.close()
	def resetAllServ(self):
		""" Restartuje všechny služby pro aplikaci
		\param self Ukazatel na objekt
		"""
		if os.path.isfile("/etc/init.d/network-manager"):
			tos='/etc/init.d/network-manager stop'
			for line in self.sy.runProcess(tos):
				print line,
				self.log.write(line)
		# síťování
		tos='/etc/init.d/networking restart'
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
		# dhcp
		tos='/etc/init.d/isc-dhcp-server restart'
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
		#tftpd
		tos='/etc/init.d/tftpd-hpa restart'
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
		# nfs
		tos='service nfs-common restart'
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
		tos='service nfs-kernel-server restart'
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
	def createStudent(self):
		""" Vytváří profil studenta
		\param self Ukazatel na objekt
		"""
		self.sy.removeFl("/NFSROOT/class/addons/makeStu.sh")
		tar = open ("/NFSROOT/class/addons/makeStu.sh", 'a')
		tar.write("#!/bin/bash\n")
		tar.write("export LC_ALL=C\n")
		tar.write("groupadd student\n")
		tar.write("useradd student -d /run/shm/home/student -p student -s /bin/bash -g student\n")
		tar.write("chown -R student:student /home/student\n")
		tar.close()
		os.chmod("/NFSROOT/class/addons/makeStu.sh",0755)
		self.sy.extGzTar("./data/dataStCp.tar.gz")
		self.sy.removeFl("/NFSROOT/class/home/student")
		shutil.move("./dataStCp/student","/NFSROOT/class/home/")
		self.sy.removeFl("/NFSROOT/class/etc/rc.local")
		shutil.move("./dataStCp/rc.local","/NFSROOT/class/etc/")
		tos='chroot /NFSROOT/class /bin/bash -c ./addons/makeStu.sh'
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
		self.sy.removeFl("./dataStCp")
		self.sy.chgPasswd("/NFSROOT/class/etc/shadow",'student','student')
		self.copyXBac()
		# kopírování dávky pro dělání linku
		sh=ShrFol()
		sh.intrCli()
	def unstallXfce(self,qo=None):
		""" Odinstaluje xfce
		\param self Ukazatel na objekt
		\param qo Ukazatel na frontu pro výpis v okně
		"""
		self.sy.removeFl("/NFSROOT/class/addons/unstallXfc.sh")
		tar = open ("/NFSROOT/class/addons/unstallXfc.sh", 'a')
		tar.write("#!/bin/bash\n")
		tar.write("export LC_ALL=C\n")
		tar.write("export XKBMODEL=\"pc105\"\n")
		tar.write("export XKBLAYOUT=\"cz\"\n")
		tar.write("export XKBVARIANT=\"qwerty_bksl\"\n")
		tar.write("export XKBOPTIONS=\"\"\n")
		tar.write("export DEBIAN_FRONTEND=noninteractive\n")
		tar.write("apt-get autoremove --purge xfce4 -y\n")
		tar.write("apt-get autoremove --purge slim -y\n")
		tar.close()
		os.chmod("/NFSROOT/class/addons/unstallXfc.sh",0755)
		tos='chroot /NFSROOT/class /bin/bash -c ./addons/unstallXfc.sh'
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
			if qo != None:
				if "Get" == line.split(":")[0]:
					qo.put("Získávám " + line.split(" ")[-5].replace("\n",""))
				if "Setting" == line.split(" ")[0]:
					qo.put("Nastavuji " + line.split(" ")[-3].replace("\n",""))
				if "Unpacking" == line.split(" ")[0]:
					qo.put("Rozbaluji " + line.split(" ")[1].replace("\n",""))
	def installXfce(self,qo=None):
		""" Instaluje xfce
		\param self Ukazatel na objekt
		\param qo Ukazatel na frontu pro výpis v okně
		"""
		self.sy.removeFl("/NFSROOT/class/addons/installXfc.sh")
		tar = open ("/NFSROOT/class/addons/installXfc.sh", 'a')
		tar.write("#!/bin/bash\n")
		tar.write("export LC_ALL=C\n")
		tar.write("export XKBMODEL=\"pc105\"\n")
		tar.write("export XKBLAYOUT=\"cz\"\n")
		tar.write("export XKBVARIANT=\"qwerty_bksl\"\n")
		tar.write("export XKBOPTIONS=\"\"\n")
		tar.write("export DEBIAN_FRONTEND=noninteractive\n")
		tar.write("apt-get install --allow-unauthenticated xfce4 -y --force-yes\n")
		#tar.write("apt-get install --allow-unauthenticated lightdmdm -y\n")
		tar.close()
		os.chmod("/NFSROOT/class/addons/installXfc.sh",0755)
		tos='chroot /NFSROOT/class /bin/bash -c ./addons/installXfc.sh'
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
			if qo != None:
				if "Get" == line.split(":")[0]:
					qo.put("Získávám " + line.split(" ")[-5].replace("\n",""))
				if "Setting" == line.split(" ")[0]:
					qo.put("Nastavuji " + line.split(" ")[-3].replace("\n",""))
				if "Unpacking" == line.split(" ")[0]:
					qo.put("Rozbaluji " + line.split(" ")[1].replace("\n",""))
	def installStand(self,qo=None):
		""" Instaluje standardní systém
		\param self Ukazatel na objekt
		\param qo Ukazatel na frontu pro výpis v okně
		"""
		self.sy.removeFl("/NFSROOT/class/addons/installSta.sh")
		tar = open ("/NFSROOT/class/addons/installSta.sh", 'a')
		tar.write("#!/bin/bash\n")
		tar.write("export DEBIAN_FRONTEND=noninteractive\n")
		tar.write("aptitude install ~pstandard ~pimportant ~prequired -y\n")
		tar.close()
		os.chmod("/NFSROOT/class/addons/installSta.sh",0755)
		tos='chroot /NFSROOT/class /bin/bash -c ./addons/installSta.sh'
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
			if qo != None:
				if "Get" == line.split(":")[0]:
					qo.put("Získávám " + line.split(" ")[-5].replace("\n",""))
				if "Setting" == line.split(" ")[0]:
					qo.put("Nastavuji " + line.split(" ")[-3].replace("\n",""))
				if "Unpacking" == line.split(" ")[0]:
					qo.put("Rozbaluji " + line.split(" ")[1].replace("\n",""))
	def installDm(self,qo=None):
		""" Instaluje login do X
		\param self Ukazatel na objekt
		\param qo Ukazatel na frontu pro výpis v okně
		"""
		# upravit Xwrapper
		f = open("/NFSROOT/class/etc/X11/Xwrapper.config","w")
		# allowed_users=anybody
		f.write("allowed_users=anybody\n")
		f.close()
		# upravit rc.local
		nad="su - student -c startx &"
		with open("/NFSROOT/class/etc/rc.local",'r') as cont:
			cnl=cont.read()
		obs=""
		for line in cnl.split("\n"):
			if nad in line:
				return
			if "exit 0" == line:
				break
			obs = obs + line  + "\n"
		obs = obs + nad + "\n"
		obs = obs + "exit 0\n"
		tar = open ("/NFSROOT/class/etc/rc.local", 'w')
		tar.write(obs)
		tar.close()
	def installSysDebs(self,qo=None):
		""" Instaluje základní systém přes deboostrap
		\param self Ukazatel na objekt
		\param qo Ukazatel na frontu pro výpis v okně
		"""
		self.sy.makeDir("/NFSROOT")
		self.sy.makeDir("/NFSROOT/class")
		for line in self.sy.runProcess("debootstrap wheezy /NFSROOT/class http://ftp.cz.debian.org/debian/"):
			print line,
			self.log.write(line)
			if qo != None:
				if "Retrieving" in line:
					qo.put("Získávám " + line.split(" ")[-1].replace("\n",""))
				if "Unpacking" in line:
					qo.put("Rozbaluji " + line.split(" ")[-1].replace("\n",""))
				if "Configuring" in line:
					qo.put("Nastavuji " + line.split(" ")[-1].replace("\n",""))
		if os.path.isfile("/etc/apt/apt.conf.d/80cacher"):
			self.sy.removeFl("/NFSROOT/class/etc/apt/apt.conf.d/80cacher")
			self.sy.copyLargeFile("/etc/apt/apt.conf.d/80cacher","/NFSROOT/class/etc/apt/apt.conf.d/80cacher")
	def createKer(self,qo=None):
		""" Instaluje základní jádro do základního systému a zapisuje jej do TFTPD serveru
		\param self Ukazatel na objekt
		\param qo Ukazatel na frontu pro výpis v okně
		"""
		self.sy.removeFl("/NFSROOT/class/addons/installImg.sh")
		tar = open ("/NFSROOT/class/addons/installImg.sh", 'a')
		tar.write("#!/bin/bash\n")
		tar.write("export LC_ALL=C\n")
		tar.write("rm /etc/mtab\n")
		tar.write("ln -s /proc/mounts /etc/mtab & \n")
		tar.write("sleep 4\n")
		tar.write("apt-get install --allow-unauthenticated linux-image-`uname -a | awk '{print $3}'` -y --force-yes\n")
		tar.close()
		os.chmod("/NFSROOT/class/addons/installImg.sh",0755)
		tos='chroot /NFSROOT/class /bin/bash -c ./addons/installImg.sh'
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
			if qo != None:
				if "Get" == line.split(":")[0]:
					qo.put("Získávám " + line.split(" ")[-5].replace("\n",""))
				if "Setting" == line.split(" ")[0]:
					qo.put("Nastavuji " + line.split(" ")[-3].replace("\n",""))
				if "Unpacking" == line.split(" ")[0]:
					qo.put("Rozbaluji " + line.split(" ")[1].replace("\n",""))
		# nastavit tftpd
		# kopírování obrazů jádra do zavaděče
		for fln in os.listdir("/NFSROOT/class/boot/"):
			root, ext = os.path.splitext(fln)
			if root.startswith('initrd'):
				intrnam = fln
			if root.startswith('vmlinuz'):
				vmlinuz = fln
		self.sy.removeFl("/srv/tftp/" + vmlinuz)
		self.sy.removeFl("/srv/tftp/" + intrnam)
		self.sy.copyLargeFile("/NFSROOT/class/boot/" + vmlinuz,"/srv/tftp/" + vmlinuz)
		self.sy.copyLargeFile("/NFSROOT/class/boot/" + intrnam,"/srv/tftp/" + intrnam)
		self.sy.removeFl("/srv/tftp/pxelinux.0")
		self.sy.copyLargeFile("/usr/lib/syslinux/pxelinux.0","/srv/tftp/pxelinux.0")
		fl=False
		for line in open("/etc/default/tftpd-hpa"):
			if "DUCKED changed" in line:
				fl=True
		if fl == False:
			tar = open ("/etc/default/tftpd-hpa", 'a')
			tar.write("\n# DUCKED changed\n")
			tar.close()
	def tftpdCon(self,qo=None):
		""" Nastavuje tftp konfiguraci
		\param self Ukazatel na objekt
		"""
		for fln in os.listdir("/NFSROOT/class/boot/"):
			root, ext = os.path.splitext(fln)
			if root.startswith('initrd'):
				intrnam = fln
			if root.startswith('vmlinuz'):
				vmlinuz = fln
		self.sy.makeDir("/srv/tftp/pxelinux.cfg")
		self.sy.removeFl("/srv/tftp/pxelinux.cfg/default")
		tar = open ("/srv/tftp/pxelinux.cfg/default", 'a')
		tar.write("default Debian\n")
		tar.write("prompt 1\n")
		tar.write("timeout 10\n")
		tar.write("label Debian\n")
		tar.write("kernel " + vmlinuz + "\n")
		tar.write("APPEND root=/dev/nfs initrd=" + intrnam + " nfsroot=" + self.sy.getEthIp(self.ethc) + ":/NFSROOT/class ip=dhcp rw\n")
		tar.close()
		os.chmod("/srv/tftp/pxelinux.cfg/default",0777)
	def setUpFst(self):
		""" Nastavuje fstab v obraze
		\param self Ukazatel na objekt
		"""
		self.sy.removeFl("/NFSROOT/class/etc/fstab")
		fd=open("/NFSROOT/class/etc/fstab",'a')
		fd.write("# DUCKED changed \n")
		#fd.write(self.sy.getEthIp(self.ethc)  + ":/NFSROOT/class/etc/X11 /etc/X11 nfs rw,hard,nolock 0 0\n")
		fd.write("#\n")
		fd.write(self.sy.getEthIp(self.ethc)  + ":/NFSROOT/class/  /  nfs defaults 1 1\n")
		fd.write("devpts                  /dev/pts                devpts  gid=5,mode=620  0 0\n")
		fd.write("sysfs                   /sys                    sysfs   defaults \n")
		fd.write("proc                    /proc                   proc    defaults\n")
		fd.write("tmpfs 			/tmp 			tmpfs   mode=1777,nosuid,nodev 0 0\n")
		fd.close()
		os.chmod("/NFSROOT/class/etc/fstab",0644)
	def setUpFw(self):
		""" Nastavuje spuštění firewallu
		\param self Ukazatel na objekt
		"""
		# nakopíruje rules.sh s permit na všechno
		wa="/NFSROOT/class/addons/"
		nm="rules.sh"
		if os.path.isfile(wa + nm):
			self.sy.removeFl(wa + nm)
			self.sy.copyLargeFile("./data/" + nm,wa + nm)
		else:
			self.sy.copyLargeFile("./data/" + nm,wa + nm)
		os.chmod(wa + nm,0755)
		# nakopíruje do obrazu ipTabChe.sh
		nm="ipTabChe.sh"
		if os.path.isfile(wa + nm):
			self.sy.removeFl(wa + nm)
			self.sy.copyLargeFile("./data/" + nm,wa + nm)
		else:
			self.sy.copyLargeFile("./data/" + nm,wa + nm)
		os.chmod(wa + nm,0755)
		# zavede do rc.local odkaz na ipTabChe.sh
		wa= "/addons/"
		with open("/NFSROOT/class/etc/rc.local",'r') as cont:
			cnl=cont.read()
		obs=""
		for line in cnl.split("\n"):
			if wa + nm +" &" in line:
				return
			if "exit 0" == line:
				break
			obs = obs + line  + "\n"
		obs = obs + wa + nm +" &\n"
		obs = obs + "exit 0\n"
		tar = open ("/NFSROOT/class/etc/rc.local", 'w')
		tar.write(obs)
		tar.close()
		# nainstaluje inotify pro změnu souboru
		# NEFUNGUJE KVŮLI NFS
		#self.sy.removeFl("/NFSROOT/class/addons/setupNotify.sh")
		#tar = open ("/NFSROOT/class/addons/setupNotify.sh", 'a')
		#tar.write("#!/bin/bash\n")
		#tar.write("export DEBIAN_FRONTEND=noninteractive\n")
		#tar.write("export LC_ALL=C\n")
		#tar.write("apt-get install --allow-unauthenticated inotify-tools -y --force-yes\n")
		#tar.close()
		#os.chmod("/NFSROOT/class/addons/setupNotify.sh",0755)
		#tos='chroot /NFSROOT/class /bin/bash -c ./addons/setupNotify.sh'
		#for line in self.sy.runProcess(tos):
		#	print line,
		#	self.log.write(line)
	def setUpLoc(self):
		""" Nastavuje locales v obraze
		\param self Ukazatel na objekt
		"""
			# env
		self.sy.removeFl("/NFSROOT/class/etc/environment")
		tar = open ("/NFSROOT/class/etc/environment", 'a')
		tar.write("LC_ALL=cs_CZ.UTF-8\n")
		tar.write("LC_LANG=cs_CZ.UTF-8\n")
		tar.close()
		os.chmod("/NFSROOT/class/etc/environment",0644)
			# loc
		self.sy.removeFl("/NFSROOT/class/etc/default/locale")
		tar = open ("/NFSROOT/class/etc/default/locale", 'a')
		tar.write("LC_ALL=cs_CZ.UTF-8\n")
		tar.write("LC_LANG=cs_CZ.UTF-8\n")
		tar.close()
		os.chmod("/NFSROOT/class/etc/default/locale",0644)
			# locaStu
		self.sy.removeFl("/NFSROOT/class/addons/locaStu.sh")
		tar = open ("/NFSROOT/class/addons/locaStu.sh", 'a')
		tar.write("#!/bin/bash\n")
		tar.write("export DEBIAN_FRONTEND=noninteractive\n")
		tar.write("apt-get install --allow-unauthenticated locales -y --force-yes\n")
		tar.write("localedef -i cs_CZ -f UTF-8 cs_CZ.UTF-8\n")
		tar.write("update-locale cs_CZ.UTF-8\n")
		tar.write("locale-gen\n")
		tar.write("update-locale cs_CZ.UTF-8\n")
		tar.write("localedef -i cs_CZ -f UTF-8 cs_CZ.UTF-8\n")
		tar.close()
		os.chmod("/NFSROOT/class/addons/locaStu.sh",0755)
		tos='chroot /NFSROOT/class /bin/bash -c ./addons/locaStu.sh'
		for line in self.sy.runProcess(tos):
			print line,
	def setUpKey(self):
		""" Nastavuje klávesnici pro X v obraze
		\param self Ukazatel na objekt
		"""
		self.sy.removeFl("/NFSROOT/class/addons/setupXfc.sh")
		tar = open ("/NFSROOT/class/addons/setupXfc.sh", 'a')
		tar.write("#!/bin/bash\n")
		tar.write("export DEBIAN_FRONTEND=noninteractive\n")
		tar.write("export LC_ALL=C\n")
		tar.write("apt-get install --allow-unauthenticated xserver-xorg-input-kbd -y --force-yes\n")
		tar.close()
		os.chmod("/NFSROOT/class/addons/setupXfc.sh",0755)
		tos='chroot /NFSROOT/class /bin/bash -c ./addons/setupXfc.sh'
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
	def installIce(self):
		""" Instaluje Iceweasel do obrazu
		\param self Ukazatel na objekt
		"""
		self.sy.removeFl("/NFSROOT/class/addons/installIce.sh")
		tar = open ("/NFSROOT/class/addons/installIce.sh", 'a')
		tar.write("#!/bin/bash\n")
		tar.write("export LC_ALL=C\n")
		tar.write("export DEBIAN_FRONTEND=noninteractive\n")
		tar.write("apt-get install --allow-unauthenticated iceweasel -y --force-yes\n")
		tar.close()
		os.chmod("/NFSROOT/class/addons/installIce.sh",0755)
		tos='chroot /NFSROOT/class /bin/bash -c ./addons/installIce.sh'
		for line in self.sy.runProcess(tos):
			print line,
			self.log.write(line)
	def copyXorgCo(self):
		""" Kopíruji Xorg konfiguraci
		\param self Ukazatel na objekt
		"""
		# Kopie XORG konfiguračních souborů
		self.sy.extGzTar("./data/dataXorg.tar.gz")
		self.sy.removeFl("/NFSROOT/class/etc/X11")
		shutil.move("./dataXorg/X11","/NFSROOT/class/etc/")
		os.rmdir("./dataXorg")
		# Přidání české klávesy
		self.sy.removeFl("/NFSROOT/class/etc/default/keyboard")
		tar = open ("/NFSROOT/class/etc/default/keyboard", 'a')
		tar.write("# KEYBOARD CONFIGURATION FILE\n")
		tar.write("\n")
		tar.write("# Consult the keyboard(5) manual page.\n")
		tar.write("\n")
		tar.write("XKBMODEL=\"pc105\"\n")
		tar.write("XKBLAYOUT=\"cz\"\n")
		tar.write("XKBVARIANT=\"qwerty_bksl\"\n")
		tar.write("XKBOPTIONS=\"\"\n")
		tar.write("\n")
		tar.write("BACKSPACE=\"guess\"\n")
		os.chmod("/NFSROOT/class/etc/default/keyboard",0644)
		tar.close()
		# Změna klávesy při startu uživatele
		self.sy.removeFl("/NFSROOT/class/home/student/.config/autostart/chanKeyb.desktop")
		tar = open ("/NFSROOT/class/home/student/.config/autostart/chanKeyb.desktop", 'a')
		tar.write("[Desktop Entry]\n")
		tar.write("Type=Application\n")
		tar.write("Name=My Script\n")
		tar.write("Exec=/addons/chgKey.sh\n")
		tar.write("Icon=system-run\n")
		tar.write("X-GNOME-Autostart-enabled=true\n")
		tar.close()
		os.chmod("/NFSROOT/class/home/student/.config/autostart/chanKeyb.desktop",0777)
		# Přidání dávky pro změnu klávesy
		self.sy.removeFl("/NFSROOT/class/addons/chgKey.sh")
		tar = open ("/NFSROOT/class/addons/chgKey.sh", 'a')
		tar.write("#!/bin/bash\n")
		tar.write("setxkbmap cz;\n")
		tar.close()
		os.chmod("/NFSROOT/class/addons/chgKey.sh",0777)
		# Kopie pravidel pro restart a vypínání
		self.sy.removeFl("/NFSROOT/class/etc/polkit-1/localauthority/50-local.d/consolekit.pkla")
		self.sy.makeDir("/NFSROOT/class/etc/polkit-1/localauthority/50-local.d/")
		f=open("/NFSROOT/class/etc/polkit-1/localauthority/50-local.d/consolekit.pkla","a")
		f.write("[restart]\n")
		f.write("Identity=unix-user:*\n")
		f.write("Action=org.freedesktop.consolekit.system.restart\n")
		f.write("ResultAny=yes\n\n")
		f.write("[stop]\n")
		f.write("Identity=unix-user:*\n")
		f.write("Action=org.freedesktop.consolekit.system.stop\n")
		f.write("ResultAny=yes\n")
		f.close()
		os.chmod("/NFSROOT/class/etc/polkit-1/localauthority/50-local.d/consolekit.pkla",0666)
		#
		self.sy.removeFl("/NFSROOT/class/etc/polkit-1/localauthority/50-local.d/udisks.pkla")
		f=open("/NFSROOT/class/etc/polkit-1/localauthority/50-local.d/udisks.pkla","a")
		f.write("[udisks]\n")
		f.write("Identity=unix-user:*\n")
		f.write("Action=org.freedesktop.udisks*\n")
		f.write("ResultAny=yes\n")
		f.close()
		os.chmod("/NFSROOT/class/etc/polkit-1/localauthority/50-local.d/udisks.pkla",0666)
		# Přidání vypínače pro iTalc
		self.sy.removeFl("/NFSROOT/class/usr/bin/gdm-signal")		
		f=open("/NFSROOT/class/usr/bin/gdm-signal","a")
		f.write("#!/bin/bash\n")
		f.write("if [[ \"$1\" == \"-h\" ]];then\n")
		f.write("     xfce4-session-logout --halt;\n")
		f.write("fi\n")
		f.write("if [[ \"$1\" == \"-r\" ]];then\n")
		f.write("     xfce4-session-logout --restart;\n")
		f.write("fi\n")
		f.close()
		os.chmod("/NFSROOT/class/usr/bin/gdm-signal",0755)
		# Přidání restartu pro iTalc
		self.sy.removeFl("/NFSROOT/class/usr/bin/gdm-restart")		
		f=open("/NFSROOT/class/usr/bin/gdm-restart","a")
		f.write("#!/bin/bash\n")
		f.write("xfce4-session-logout --restart;\n")
		f.close()
		os.chmod("/NFSROOT/class/usr/bin/gdm-restart",0755)
	def copyXBac(self):
		""" Kopíruji X pozadi
		\param self Ukazatel na objekt
		"""
		self.sy.extGzTar("./data/bckGrou.tar.gz")
		self.sy.removeFl("/NFSROOT/class/addons/contents/")
		shutil.move("./contents","/NFSROOT/class/addons/")
		self.sy.removeFl("/NFSROOT/class/addons/setupBck.sh")
		tar = open ("/NFSROOT/class/addons/setupBck.sh", 'a')
		tar.write("#!/bin/bash\n")
		tar.write("xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/image-path -s /addons/contents/images/1600x1200.png\n")
		tar.close()
		os.chmod("/NFSROOT/class/addons/setupBck.sh",0755)
		self.sy.removeFl("/NFSROOT/class/home/student/.config/autostart/chgback.desktop")
		tar = open ("/NFSROOT/class/home/student/.config/autostart/chgback.desktop", 'a')
		tar.write("[Desktop Entry]\n")
		tar.write("Type=Application\n")
		tar.write("Name=My Script]\n")
		tar.write("Exec=/addons/setupBck.sh\n")
		tar.write("Icon=system-run\n")
		tar.write("X-GNOME-Autostart-enabled=true\n")
		tar.close()
		os.chmod("/NFSROOT/class/home/student/.config/autostart/chgback.desktop",0777)
if __name__ == "__main__":
	## vstup pro parser konf souboru
	pr=ParConfFl()
	## vnitřní rozhraní pro síť
	ine=pr.getInterfaces()['inti']
	## Parser argumentů a parametrů
	parser = OptionParser(usage="usage: %prog [args]\n Installation and detail configuration for client image and host system")
	parser.add_option("-o", "--show-out-eth", action="store_true", dest="out", default=False, help="Show outer interface")
	parser.add_option("-s", "--setup-services", action="store_true", dest="set", default=False, help="Setting up network services configuration")
	parser.add_option("-n", "--setup-network", action="store_true", dest="net", default=False, help="Setting up network IP and NAT")
	parser.add_option("-c", "--install-x", action="store_true", dest="xin", default=False, help="Install X windows")
	parser.add_option("-b", "--install-browser", action="store_true", dest="bin", default=False, help="Install Iceweasel to image")
	parser.add_option("-k", "--install-kernel", action="store_true", dest="kin", default=False, help="Install kernel to TFTP and clients filesystem")
	parser.add_option("-i", "--inner-interface", action="store", type="string", dest="sf", default="", help="Settting up for interface inside of class")
	## Argumenty a parametry z parseru
	(args, opts) = parser.parse_args()
	if args.sf != "":
		ine=args.sf
	## instance objektu pro práci s klientskou stanicí
	sf=ConfSys(ine)
	if args.out == True:
		print sf.getDefGtw()
	if args.xin == True:
		sf.copyXorgCo()
		sf.installXfce()
		sf.setUpKey()
		sf.copyXBac()
		sf.installDm()
	if args.bin == True:
		sf.installIce()
	if args.kin == True:
		sf.createKer()
		sf.tftpdCon()
	if args.set == True:
		sf.setUpDH()
		sf.setUpNFS()
		sf.setUpHsn()
		sf.setUpFst()
	if args.net == True:
		sf.resetNet()
		sf.setUpMasq()
		