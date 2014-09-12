#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
## \file testsConf.py
## \brief Grafické prostředí pro konotrolu konfigurace systému

from Tkinter import *

class ConfCheck:
	""" 
	\brief Třída obsahující metody pro práci se soubory systému		
	"""
	def check(self,fl):
		""" Projde textový soubor a zkontroluje, zdali obsahuje DUCKED changed - 
		což je poznámka, která naznačuje, že je konfigurační soubor už upraven
		\param self Ukazatel na objekt
		\param fl Textový soubor konfiguračního souboru
		"""
		for line in open(fl):
			if "DUCKED changed" in line:
				return 0
		return 1
if __name__ == "__main__":
	class App:
		""" 
		\brief Třída obsahující metody pro práci s oknem.
		Metody mají za úkol zkontrolovat konfigurační vybraných služeb systému.		
		"""
		def __init__(self,r):
			""" Konstruktor třídy okna
			\param self Ukazatel na objekt
			\param r Ukazatel na okno
			"""
			## Ukazatel na instanci objektu obsahujícím třídu, která konotroluje obsah konfiguračních souborů
			self.cf=ConfCheck()
			## Proměnná funguje jako vlaječka pro kontrolu všech konfiguračních souborů, pokud dojde k chybě, zůstane na 0
			self.flg=0
			## Ukazatel na okno
			self.root=r
			self.root.title("Testování stavu")
			self.root.geometry(("%dx%d")%(210,200))
			self.root.wm_iconbitmap('@./gnusk.xbm')
			self.root.resizable(0,0)
			## Skupina label objektů
			self.group = LabelFrame(self.root, text="Služby", padx=5, pady=5)
			self.group.pack(padx=10, pady=10)
		def checkDHCP(self):
			""" Kontrola DHCP serveru
			\param self Ukazatel na objekt
			"""
			vd = StringVar()
			return_code = self.cf.check('/etc/dhcp/dhcpd.conf')
			if return_code == 0:
				ld = Label( self.group, textvariable=vd, relief=RAISED, bg= "green", font = "Verdana 10 bold" )
				vd.set("DCHP server nastaven")
			else:
				ld = Label( self.group, textvariable=vd, relief=RAISED, bg= "red", font = "Verdana 10 bold" )
				vd.set("DCHP server nenastaven")
				self.flg=1
			ld.pack()
		def checkTFTPD(self):
			""" Kontrola TFTPD serveru
			\param self Ukazatel na objekt
			"""
			vd = StringVar()
			return_code = self.cf.check('/etc/default/tftpd-hpa')
			if return_code == 0:
				ld = Label( self.group, textvariable=vd, relief=RAISED, bg= "green", font = "Verdana 10 bold" )
				vd.set("TFTPD server nastaven")
			else:
				ld = Label( self.group, textvariable=vd, relief=RAISED, bg= "red", font = "Verdana 10 bold" )
				vd.set("TFTPD server nenastaven")
				self.flg=1
			ld.pack()
		def checkNFS(self):
			""" Kontrola NFS serveru
			\param self Ukazatel na objekt
			"""
			vd = StringVar()
			return_code = self.cf.check('/etc/exports')
			if return_code == 0:
				ld = Label( self.group, textvariable=vd, relief=RAISED, bg= "green", font = "Verdana 10 bold" )
				vd.set("NFS server nastaven")
			else:
				ld = Label( self.group, textvariable=vd, relief=RAISED, bg= "red", font = "Verdana 10 bold" )
				vd.set("NFS server nenastaven")
				self.flg=1
			ld.pack()
		def printFotNote(self):
			""" Výpis poznámky na konci okna
			\param self Ukazatel na objekt
			"""
			if self.flg == 0:
				tx=StringVar()
				tx.set("Všechny potřebné služby \n nastaveny, pokud systém \n stále nefunguje, vyzkoušejte \n znovu nastavit služby.")
				en = Label( self.root, textvariable=tx, font = "Verdana 10" )
			else:
				tx=StringVar()
				tx.set("Některé služby nejsou nastaveny, \n pokuste se je znovu \n nainstalovat")
				en = Label( self.root, textvariable=tx, font = "Verdana 10" )

			en.pack()
	## Hlavní instance okna TK
	root = Tk()
	## Vladtní instance třídy okna
	ap=App(root)
	ap.checkDHCP()
	ap.checkTFTPD()
	ap.checkNFS()
	ap.printFotNote()
	root.mainloop()