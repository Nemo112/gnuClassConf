#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
## \file testsServices.py
## \brief Grafické prostředí pro konotrolu služeb systému

from Tkinter import *
import subprocess

if __name__ == "__main__":
	class App:
		""" 
		\brief Třída obsahující metody pro práci s oknem.
		Metody mají za úkol zkontrolovat běh vybraných služeb systému.		
		"""
		def __init__(self,r):
			""" Konstruktor třídy okna
			\param self Ukazatel na objekt
			\param r Ukazatel na okno
			"""
			## Proměnná funguje jako vlaječka pro kontrolu všech konfiguračních souborů, pokud dojde k chybě, zůstane na 0
			self.flg=0
			## Ukazatel na okno
			self.root=r
			self.root.title("Testování služeb")
			self.root.geometry(("%dx%d")%(200,200))
			self.root.wm_iconbitmap('@./gnusk.xbm')
			self.root.resizable(0,0)
			## Skupina label objektů
			self.group = LabelFrame(root, text="Služby", padx=5, pady=5)
			self.group.pack(padx=10, pady=10)
		def checsDHCP(self):
			""" Kontrola DHCP serveru
			\param self Ukazatel na objekt
			"""
			vd = StringVar()
			return_code = subprocess.call("service isc-dhcp-server status", shell=True)  
			if return_code == 0:
				ld = Label( self.group, textvariable=vd, relief=RAISED, bg= "green", font = "Verdana 10 bold" )
				vd.set("DCHP server běží")
			else:
				ld = Label( self.group, textvariable=vd, relief=RAISED, bg= "red", font = "Verdana 10 bold" )
				vd.set("DCHP server neběží")
				self.flg=1
			ld.pack()
		def checsTFTPD(self):
			""" Kontrola TFTPD serveru
			\param self Ukazatel na objekt
			"""
			vt = StringVar()
			return_code = subprocess.call("service tftpd-hpa status", shell=True)  
			if return_code == 0:
				lt = Label( self.group, textvariable=vt, relief=RAISED, bg= "green", font = "Verdana 10 bold" )
				vt.set("TFTPD server běží")
			else:
				lt = Label( self.group, textvariable=vt, relief=RAISED, bg= "red", font = "Verdana 10 bold" )
				vt.set("TFTPD server neběží")
				self.flg=1
			lt.pack()
		def checsNFS(self):
			""" Kontrola NFS serveru
			\param self Ukazatel na objekt
			"""
			vf = StringVar()
			return_cc = subprocess.call("service nfs-common status", shell=True)
			return_ck = subprocess.call("service nfs-kernel-server status", shell=True)
			if return_cc == 0 and return_ck==0:
				lf = Label( self.group, textvariable=vf, relief=RAISED, bg= "green", font = "Verdana 10 bold" )
				vf.set("NFS server běží")
			else:
				lf = Label( self.group, textvariable=vf, relief=RAISED, bg= "red", font = "Verdana 10 bold" )
				vf.set("NFS server neběží")
				self.flg=1
			lf.pack()
		def printFotNote(self):
			""" Výpis poznámky na konci okna
			\param self Ukazatel na objekt
			"""
			if self.flg == 0:
				tx=StringVar()
				tx.set("Všechny potřebné služby \n běží, pokud systém \n stále nefunguje, vyzkoušejte \n znovu nastavit služby.")
				en = Label( root, textvariable=tx, font = "Verdana 10" )
			else:
				tx=StringVar()
				tx.set("Některé služby neběží, \n pokuste se je znovu \n nainstalovat")
				en = Label( root, textvariable=tx, font = "Verdana 10" )
			en.pack()

	root = Tk()
	## Aplikace okna
	ap=App(root)
	ap.checsDHCP()
	ap.checsTFTPD()
	ap.checsNFS()
	ap.printFotNote()
	root.mainloop()
