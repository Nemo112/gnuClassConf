#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file closeSetup.py
## \brief Grafické prostředí pro nastavení základních vlastností systému

import string
import re
import subprocess
from Tkinter import *
import multiprocessing
from Queue import Empty, Full
import socket
import fcntl
import struct
import urllib2
import shutil
import time
import os
import hashlib
import crypt
import tarfile
from ParConfFl import ParConfFl
from LogWrk import LogWrk
from ConsSys import ConsSys
from ConfSys import ConfSys
from UError import UError
from iTaHand import iTaHand

if __name__ == "__main__":
	class App:
		""" \brief Třída obsahující metody s prací s oknem
		Obsahuje hlavně metody okna skriptu. Ovládání systému 
		z uživatelského úhlu pohledu.
		Za grafické prostředí byl zvolen Tkinker kvůli mobilitě.
		"""
		def __init__(self,r,qii,qoi):
			""" Konstruktor třídy okna
			\param self Ukazatel na objekt
			\param r Ukazatel na Tkinker okno
			\param qii Ukazatel na vstupní frontu pro práci s textovým pole níže
			\param qoi Ukazatel na výstupní frontu pro práci s textovým pole níže
			"""
			## Instance objektu spravující systémové nástroje
			self.sys=ConsSys()
			## Ukazatel na okno Tk
			self.root=r
			self.root.title("Základní nastavení učebny")
			self.root.geometry(("%dx%d")%(700,500))
			self.root.wm_iconbitmap('@./gnusk.xbm')
			self.root.protocol("WM_DELETE_WINDOW",self.qquit)
			self.root.resizable(0,0)
			## Aktivace směrování 
			self.sm=BooleanVar()
			## popis obrázku
			self.v=StringVar(self.root)
			## Počet síťových rozhraní
			self.ethc=len(self.sys.getEths())-1
			if self.ethc == 1:
				## Proměnná obsahující cestu k obrázku topologie
				self.igm=PhotoImage(file="./onesd.gif")
				## Proměnná obsahuje počet rozhraní použitých pro prostředí aplikace
				self.ethCn=1
				self.v.set("Počítač v síti")
				self.sm.set(0)
			else:
				self.igm=PhotoImage(file="./twosd.gif")
				self.ethCn=2
				self.v.set("Počítač jako směrovač")
				self.sm.set(1)
			## Vstupní fronta pro pracovní vlákno
			self.qi=qii
			## Výstupní fronta z pracovního vlákna
			self.qo=qoi
			## Logovací třída
			self.log=LogWrk()			
		def qquit(self):
			""" Metoda pro ukončení okna
			Je nutné vypnout vlákno, které vykonává příkazy na pozadí okna
			\param self Ukazatel na objekt
			"""
			self.qi.put("XXX")
			self.root.destroy()
		def chg(self,s):
			""" Metoda měnící obrázek topologii v okně
			\param s String obsahující výsledek volby uživatele ve scroll listu
			\param self Ukazatel na objekt
			"""
			global igm
			if s == "Počítač v síti":
				self.igm = PhotoImage(file="./onesd.gif")
				self.iml.configure(image=self.igm)
				# najít rozhraní, které směruje
				gws=self.sys.getDefGwInt()
				self.vf.set(gws[0])
				self.etg=gws[0]
				self.sm.set(0)
			if s == "Počítač jako směrovač":
				self.igm = PhotoImage(file="./twosd.gif")
				self.iml.configure(image=self.igm)
				# najít rozhraní, které rozhodně nesměruje
				i = 0
				gws=self.sys.getDefGwInt()
				for gw in gws:
					while gw == self.sys.getEths()[i] or self.sys.getEths()[i] == "lo":
						i += 1
						if i == len(self.sys.getEths()):
							i = 0
							break
				self.vf.set(self.sys.getEths()[i])
				self.etg=self.sys.getEths()[i]
				self.sm.set(1)
		def chge(self,s):
			""" Metoda měnící eth rozhraní konfigurace
			\param s String obsahující výsledek volby uživatele ve scroll listu
			\param self Ukazatel na objekt
			"""
			## Promměnná obsahující zvolené rozhraní pro třídu
			self.etg=s
			if self.etg in self.sys.getDefGwInt():
				self.igm = PhotoImage(file="./onesd.gif")
				self.iml.configure(image=self.igm)
				self.v.set("Počítač v síti")
				self.sm.set(0)
			else:
				self.igm = PhotoImage(file="./twosd.gif")
				self.iml.configure(image=self.igm)
				self.v.set("Počítač jako směrovač")
				self.sm.set(1)
		def CheckTxtF(self,cq):
			""" Metoda menící textové pole podle toho, zdali se něco vyskytne ve výstupní frontě
			\param cq Výstupní fronta, na kterou metoda reaguje a její výstup směřuje do textového pole to
			\param self Ukazatel na objekt
			"""
			try:
				stri = cq.get(0)
				if stri == "NET!":
					self.to.insert('end',"Pozor! Síťové rozhraní")
					self.to.itemconfig('end', {'bg':'orange'}) 
					self.to.insert('end',"se nepovedlo restartovat.")
					self.to.itemconfig('end', {'bg':'orange'}) 
					self.to.insert('end',"Při nejhorším restarujte")
					self.to.itemconfig('end', {'bg':'orange'}) 
					self.to.insert('end',"systém nebo proveďt")
					self.to.itemconfig('end', {'bg':'orange'}) 
					self.to.insert('end',"postup s jiným")
					self.to.itemconfig('end', {'bg':'orange'}) 
					self.to.insert('end',"rozhraním.")
					self.to.itemconfig('end', {'bg':'orange'}) 
				elif stri[-6:] == "ERROR!":
					self.to.insert('end',"Chyba! Zkontrolujte připojení,")
					self.to.itemconfig('end', {'bg':'orange red'}) 
					self.to.insert('end',"místo na disku a systém.")
					self.to.itemconfig('end', {'bg':'orange red'}) 
				elif stri == "TATO OPERACE JE NA DLOUHO!":
					self.to.insert('end',stri)
					self.to.itemconfig('end', {'bg':'orange'}) 
				elif stri == "Hotovo":
					self.to.insert('end',stri)
					self.to.itemconfig('end', {'bg':'lime green'}) 
				elif stri == "Zdá se, že všechno je připraveno":
					self.to.insert('end',stri)
					self.to.itemconfig('end', {'bg':'lime green'})
				elif stri == "SETSDONE":
					self.sets['state'] = 'normal'
				elif stri == "INSDONE":
					self.inse['state'] = 'normal'
				else:
					self.to.insert('end',stri)
				self.to.select_clear(self.to.size()-2)
				self.to.yview(END)
			except Empty:
				pass
			finally:
				self.root.after(100,self.CheckTxtF,cq)
		def stSet(self):
			""" Metoda pro nastavení systému
			\param self Ukazatel na objekt
			"""
			jed = str(np.get())
			dva = str(nn.get())
			tri = str(im.get())
			cty = str(ig.get())
			pet = str(ib.get())
			ses = str(su.get())
			self.qi.put("SET;" + str(self.sm.get()) + ";" + self.etg + ";" + jed + dva + tri + cty + pet + ses)
			self.sets['state'] = 'disabled'
		def stInst(self):
			""" Metoda pro spuštění instalace balíčků pro potřeby třídy
			Posílá do vstupní fronty požadavky na vnější proces, který příkazy postupně spouští
			\param self Ukazatel na objekt
			"""
			self.qi.put("INST")
			self.inse['state'] = 'disabled'
		def swi(self):
			""" Kontrolní metoda pro přepínání checkbuttonů
			\param self Ukazatel na objekt
			"""
			return
			print
			print np.get()
			print nn.get()
			print im.get()
			print ig.get()
			print ib.get()
			print su.get()
		def sme(self):
			""" Metoda pro změnu vlastnosti změrování mezi sítěmi
			\param self Ukazatel na objekt
			"""
			if self.sm.get() == 0:
				self.igm = PhotoImage(file="./onesd.gif")
				self.iml.configure(image=self.igm)
				self.v.set("Počítač v síti")
				self.sm.set(0)
			else:
				self.igm = PhotoImage(file="./twosd.gif")
				self.iml.configure(image=self.igm)
				self.v.set("Počítač jako směrovač")
				self.sm.set(1)
		def paintLayout(self):
			""" Metoda vykreslující grafické prvky okna
			Slouží jako komplexní metoda pro vykreslení a je hlavní metodou s práci s oknem
			\param self Ukazatel na objekt
			"""
			sysq=ConsSys()
			group = LabelFrame(self.root, text="Topologie učebny", padx=5, pady=5)
			group.pack()
			if self.ethc == 1:
				self.v.set("Počítač v síti")
			else:
				self.v.set("Počítač jako směrovač")
			option = OptionMenu(group, self.v, "Počítač v síti", "Počítač jako směrovač", command=self.chg)
			option.pack()
			## Proměnná obsahuje obrázek topologie
			self.iml=Label(group, image=self.igm)
			self.iml.pack()
			
			grsh = LabelFrame(self.root, text="Kontroly", padx=5, pady=5)
			grsh.place(relx=0.01, rely=.37)
			Button(grsh,height=1, width=16,text="    Stav služeb     ",command=sysq.serv).pack()
			Button(grsh,height=1, width=16,text="Nastavení služeb",command=sysq.sets).pack()
			
			grss = LabelFrame(self.root, width=16, text="Součásti nastavení", padx=5, pady=5)
			grss.place(relx=0.01, rely=.54)
			Label(grss,width=24,text="Nasledující možnosti slouží \nk nastavení atributů,\n které se budou \ninstalovat při spuštění\n \"Nastavení služeb systému\"",font=('Ariel',7)).pack()

			"""
			np
			nn
			im
			ig
			ib
			su
			"""
			## s Checkbutton pro nastavení připojení
			self.s=Checkbutton(grss,text="Nastavení připojení",onvalue=True,offvalue=False,variable=np,command=self.swi)
			self.s.pack(anchor=W)
			## p Checkbutton pro nastavení služeb
			self.p=Checkbutton(grss,text="Nastavení služeb",onvalue=True,offvalue=False,variable=nn,command=self.swi)
			self.p.pack(anchor=W)
			## l Checkbutton pro instalaci obrazu
			self.l=Checkbutton(grss,text="Instalace obrazu",onvalue=True,offvalue=False,variable=im,command=self.swi)
			self.l.pack(anchor=W)
			## q Checkbutton pro instalaci gui
			self.q=Checkbutton(grss,text="Instalace gui",onvalue=True,offvalue=False,variable=ig,command=self.swi)
			self.q.pack(anchor=W)
			## c Checkbutton pro instalaci prohlížeče
			self.c=Checkbutton(grss,text="Instalace nástrojů",onvalue=True,offvalue=False,variable=ib,command=self.swi)
			self.c.pack(anchor=W)
			## u Checkbutton pro nastavení uživatelů
			self.u=Checkbutton(grss,text="Nastavení uživatelů",onvalue=True,offvalue=False,variable=su,command=self.swi)
			self.u.pack(anchor=W)
		
			grst = LabelFrame(self.root, text="Stav", padx=5, pady=5)
			grst.place(relx=0.27, rely=.37)
			tx = StringVar()
			vx = StringVar()
			if sysq.isCnt():
				vx.set("Počítač připojen k internetu.")
				lxi=Label(grst,textvariable=vx, height=3, width=30)
			else:
				vx.set("Chybí internet!")
				lxi=Label(grst,font="bold",textvariable=vx, height=3, width=20)
			tx.set("Počet rozhraní: " + str(self.ethc) + "\n systém podle toho \n nastavil předpokládanou \n topologii.")
			lsi=Label(grst,textvariable=tx, height=4, width=30)
			lsi.pack()
			lxi.pack()
			scrollbar = Scrollbar(self.root)
			scrollbar.pack(side=RIGHT, fill=Y)
			## Listbox, který reaguje na pracovní vlákno
			self.to = Listbox(self.root,height=18, width=27, bd=0, yscrollcommand=scrollbar.set)
			self.to.place(relx=0.66, rely=.41)
			self.to.insert('end', "Zatím nic...")
			scrollbar.config(command=self.to.yview)
			Label(self.root,text="Průběh nastavování").place(relx=0.66, rely=.37)
			dnwg=LabelFrame(self.root, text="Rozhraní", padx=5, pady=3)
			dnwg.place(relx=0.27, rely=.68)
			Label(dnwg,text="Pro třídu:").pack(side=LEFT)
			## Proměnná obsahuje string prostředí Tk, které říká, jaké je zvolené rozrhaní pro komunikaci se třídou
			self.vf=StringVar(self.root)
			etf=self.sys.getEths()
			if self.ethCn == 1:
				gws=self.sys.getDefGwInt()
				self.etg=gws[0]
				self.vf.set(gws[0])
			else:
				i=0
				while etf[i] in self.sys.getDefGwInt() or etf[i] == "lo":
					i += 1
					if i == len(etf):
						i = 0
						break
				self.vf.set(etf[i])
				self.etg=etf[i]
			opteth = OptionMenu(dnwg,self.vf, *etf, command=self.chge)
			opteth.pack(side=LEFT)
			# co když uživatel přesto nechce/chce směrovat pro rozhraní
			Label(dnwg,text=" směrování:").pack(side=LEFT)
			Checkbutton(dnwg,onvalue=True,offvalue=False,variable=self.sm,command=self.sme).pack(side=LEFT)

			dnwb=LabelFrame(self.root, text="Instalace a nastavení", padx=5, pady=5)
			dnwb.place(relx=0.27, rely=.79)
			fa=Frame(dnwb)
			Label(fa,height=1, width=21,text="Instalace služeb systému:").pack(side="left")
			# spouštěcí button
			self.inse=Button(fa,height=1, width=6,text="Spustit",command=self.stInst)
			self.inse.pack(side="right")
			fb=Frame(dnwb)
			Label(fb,text="Nastavení služeb systému:").pack(side="left")
			# nastavující button
			self.sets=Button(fb,height=1, width=6,text="Spustit",command=self.stSet)
			self.sets.pack(side="right")
			fa.pack()
			fb.pack()
			self.root.after(100,self.CheckTxtF,self.qo)
	def genOut(qi,qo):
		""" Funkce pro spuštění nového vlákna.
		Funkce vykonává příkazy z fronty qi a výsledky posílá do fronty qo.
		\param qi Proměnná pro vstupní frontu
		\param qi Proměnná pro výstupní frontu
		"""
		sy=ConsSys()
		log=LogWrk()
		while True:
			stri=qi.get(True)
			if stri == "XXX":
				break
			if stri == "INST":
				# instalace prostředků
				try:
					sy.removeFl("./data/update.sh")
					tar = open ("./data/update.sh", 'a')
					tar.write("#!/bin/bash\n")
					tar.write("export DEBIAN_FRONTEND=noninteractive\n")
					tar.write("apt-get update;\n")
					tar.close()
					os.chmod("./data/update.sh",0755)
					qo.put("Kontroluji aktualizace")
					for line in sy.runProcess("./data/update.sh"):
						print line,
					qo.put("Hotovo")
					qo.put("TATO OPERACE JE NA DLOUHO!")
					qo.put("Aktualizuji")
					# upgrade
					sy.removeFl("./data/upgrade.sh")
					tar = open ("./data/upgrade.sh", 'a')
					tar.write("#!/bin/bash\n")
					tar.write("export DEBIAN_FRONTEND=noninteractive;\n")
					tar.write("apt-get upgrade -y --force-yes;\n")
					tar.close()
					os.chmod("./data/upgrade.sh",0755)
					for line in sy.runProcess("./data/upgrade.sh"):
						print line,
						log.write(line)
						if "Get" == line.split(":")[0]:
							qo.put("Získávám " + line.split(" ")[-5].replace("\n",""))
						if "Setting" == line.split(" ")[0]:
							qo.put("Nastavuji " + line.split(" ")[-3].replace("\n",""))
						if "Unpacking" == line.split(" ")[0]:
							qo.put("Rozbaluji " + line.split(" ")[1].replace("\n",""))
					qo.put("Hotovo")
					qo.put("Instaluji balíčky")
					# instalace
					sy.removeFl("./data/insts.sh")
					tar = open ("./data/insts.sh", 'a')
					tar.write("#!/bin/bash\n")
					tar.write("export DEBIAN_FRONTEND=noninteractive;\n")
					tar.write("apt-get install isc-dhcp-server iptables-persistent nfs-kernel-server tftpd-hpa syslinux debootstrap expect apache2 -y;\n")
					tar.close()
					os.chmod("./data/insts.sh",0755)
					for line in sy.runProcess("./data/insts.sh"):
						print line,
						log.write(line)
						if "Get" == line.split(":")[0]:
							qo.put("Získávám " + line.split(" ")[-5].replace("\n",""))
						if "Setting" == line.split(" ")[0]:
							qo.put("Nastavuji " + line.split(" ")[-3].replace("\n",""))
						if "Unpacking" == line.split(" ")[0]:
							qo.put("Rozbaluji " + line.split(" ")[1].replace("\n",""))
					qo.put("Hotovo")
					qo.put("INSDONE")
				except UError,e:
					qo.put(str(e.args) + " ERROR!")
			if stri.split(";")[0] == "SET":
				# bude se routovat?
				rut=int(stri.split(";")[1])
				# rozhraní třídy
				eth=stri.split(";")[2]
				setUNt=ConfSys(eth,rut)
				# parametry nastavování
				tsth=stri.split(";")[3]
				np=int(tsth[0])
				nn=int(tsth[1])
				im=int(tsth[2])
				ig=int(tsth[3])
				ib=int(tsth[4])
				su=int(tsth[5])
				print np
				print nn
				print im
				print ig
				print ib
				print su
				#start
				try:
					if np == 1:
						qo.put("Nastavuji připojení")
						pr=ParConfFl()
						pr.setInterfaces(eth,setUNt.de)
						#print eth + " XXXX " + setUNt.de
						setUNt.setUpNets()
						# restart sítě
						qo.put("Restartuji připojení")
						setUNt.resetNet()
						# povoluji NAT a routování
						qo.put("Nastavuji přepínání")
						setUNt.setUpMasq()
						# stáhnout deboostrapem obraz
				except UError,e:
					qo.put("NET!")
				try:
					if im == 1:
						qo.put("Stahuji obraz systému")
						qo.put("TATO OPERACE JE NA DLOUHO!")
						setUNt.installSysDebs(qo)
						qo.put("Hotovo")
						# přidávám složku pro instalaci dalších aplikací
						# HODNĚ DŮLEŽITÉ, OSTATNÍ METODY NA EXISTENCI SLOŽKY SPOLÉHAJÍ
					sy.makeDir("/NFSROOT/class/addons/")
					if np == 1:
						# nastavit dhcp
						setUNt.setUpDH()
					if nn == 1:
						# nastavit nfs
						setUNt.setUpNFS()
					if np == 1:
						# vkládání záznamů do fstab
						setUNt.setUpFst()
					# nastavit locales v obrazu
					if im == 1:
						qo.put("Připravuji jazyk balíčku")
						setUNt.setUpLoc()
						qo.put("Hotovo")
					if su == 1:
						# nastavit uživatele
						# heslo roota
						qo.put("Nastavuji heslo roota")
						sy.chgPasswd("/NFSROOT/class/etc/shadow",'root','teacher')
						qo.put("Hotovo")
						# založení studenta
						qo.put("Připravuji uživatele student")
						setUNt.createStudent()
						qo.put("Hotovo")
						# editace iTalc
						i=iTaHand()
						i.setUpIcaS()
					if im == 1:
						qo.put("Instaluji základní systém")
						setUNt.installStand()
						qo.put("Hotovo")
					if ig == 1:
						# Kopírování Xorg konfigurace
						qo.put("Kopíruji nastavení Xorg")
						setUNt.copyXorgCo()
						qo.put("Hotovo")
						# instalace XFCE
						qo.put("Připravuji grafické rozhraní")
						qo.put("TATO OPERACE JE NA DLOUHO!")
						setUNt.installXfce(qo)
						qo.put("Hotovo")
						# nastavení klávesnice
						qo.put("Nastavuji klávesnici")
						setUNt.setUpKey()
						qo.put("Hotovo")
					# instalace Iceweaselu
					if im == 1:
						# vytváření obrazů jádra
						qo.put("Připravuji jádro")
						setUNt.createKer(qo)
						qo.put("Hotovo")
					if np == 1:
						# mění IP pro tftpd server
						setUNt.tftpdCon(qo)
					if ib == 1:
						qo.put("Připravuji nástroje")
						setUNt.installIce()
						qo.put("Hotovo")
					if ig == 1:
						#instaluji login screen
						qo.put("Připravuji grafické rozhraní")
						setUNt.installDm(qo)
						qo.put("Hotovo")
					if ig == 1:
						# přidání pozadí
						setUNt.copyXBac()
					if nn == 1:
						# změna hostname
						# vytvořit rc skript, který nastaví hostname na "student<poslední oktet IP>"
						setUNt.setUpHsn()
						setUNt.setUpFw()
					qo.put("SETSDONE")
				except UError,e:
					qo.put(str(e.args) + " ERROR!")
				# restartuji služby
				qo.put("Restartuji služby")
				# zastavení network managera
				try:
					setUNt.resetAllServ()
				except UError,e:
					qo.put("NET!")
				qo.put("Hotovo")
				qo.put("Zdá se, že všechno je připraveno")
	## Proměnná obsahující okno Tk
	win = Tk()
	global np
	## Proměnná pro volbu nastavení připojení - true bude se řešit připojení, jinak ne
	np=BooleanVar()
	np.set(True)
	global nn
	## Proměnná pro volbu nastavení služeb - true budou se řešit služby, jinak ne
	nn=BooleanVar()
	nn.set(True)
	global im
	## Proměnná pro volbu nastavení obrazu - true bude se řešit obraz, jinak ne
	im=BooleanVar()
	im.set(True)
	global ig
	## Proměnná pro volbu nastavení Xek - true budou se řešit Xka, jinak ne
	ig=BooleanVar()
	ig.set(True)
	global ib
	## Proměnná pro volbu nastavení browseru - true bude se řešit browser, jinak ne
	ib=BooleanVar()
	ib.set(True)
	global su
	## Proměnná pro volbu nastavení uživatelů - true bude se řešit uživatele, jinak ne
	su=BooleanVar()
	su.set(True)
	## Vstupní fronta pracovního vlákna
	qi = multiprocessing.Queue()
	qi.cancel_join_thread()
	## Výstupní fronta pracovního vlákna
	qo = multiprocessing.Queue()
	qo.cancel_join_thread()
	## Instance okna, které vykonává celou aplikaci
	pp = App(win,qi,qo)
	pp.paintLayout()
	## Instance procesu, kterému je zaslána vstupní a výstupní fronta
	t=multiprocessing.Process(target=genOut,args=(qi,qo,))
	t.start()
	win.mainloop()
	t.join()