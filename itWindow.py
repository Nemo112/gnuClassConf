#!/usr/bin/python
# -*- coding: utf-8 -*-
## \file mnWindow.py
## \brief Hlavní okno aplikace
from Tkinter import *
import ttk
import subprocess
from iTaHand import iTaHand
from ConsSys import ConsSys
import os

if __name__ == "__main__":
	class App:
		""" \brief Třída obsahující metody s prací s oknem
		Okénko obsluhující instalaci a přípravu iTalc
		"""
		def __init__(self,r):
			""" Konstruktor třídy okna
			\param self Ukazatel na objekt
			\param r Ukazatel na Tkinker okno
			"""
			## Ukazatel na okno Tk
			self.root=r
			## Ukazatel na iTalc třídu
			self.it=iTaHand()
			self.root.title("iTalc nastavení")
			self.root.geometry(("%dx%d")%(200,200))
			self.root.wm_iconbitmap('@./gnusk.xbm')
			self.root.protocol("WM_DELETE_WINDOW",self.qquit)
			self.root.resizable(0,0)
		def paintLayout(self):
			""" Metoda vykreslující grafické prvky okna
			Slouží jako komplexní metoda pro vykreslení a je hlavní metodou s práci s oknem
			\param self Ukazatel na objekt
			"""
			group = LabelFrame(self.root, text="iTalc nastavení", padx=5, pady=5)
			group.pack(padx=10, pady=10)
			## Label hláška pro uživatele
			self.vd = StringVar()
			ni=True
			if self.it.tstItalc():
				ld = Label( group, textvariable=self.vd, relief=RAISED, bg= "green", font = "Verdana 10 bold" )
				self.vd.set(" iTalc je v systému ")
			else:
				ld = Label( group, textvariable=self.vd, relief=RAISED, bg= "red", font = "Verdana 10 bold" )
				self.vd.set(" iTalc není v systému ")
			if not os.path.isdir("/NFSROOT/class"):
				ni=False
			ld.pack()
			Button(group,height=1, width=19,text="Instalovat",command=self.ins).pack()
			tx=StringVar()
			if ni == False:
				tx.set("Zdá se, že chybí nejen \n iTalc. Spustě nejdřív \n \"Základní nastavení učebny\".")
			else:
				tx.set("Zdá se, že je základní \n systém nainstalován. \n Zkuste spustit instalaci \n pomocí tlačítka \"Instalovat\"")				
			en = Label( self.root, textvariable=tx, font = "Verdana 10" ).pack()
		def ins(self):
			""" Metoda instalující iTalc
			Instaluje službu, nastaví klienta, připraví klíče a nakopíruje je do klientských stanic
			\param self Ukazatel na objekt
			"""
			self.vd.set("Instaluji")
			self.it.instServ()
			self.it.instClie()
			self.it.genKeys()
			self.it.setCliSc()
			self.it.runIca()
			self.vd.set(" iTalc je v systému ")
			Button(self.root,height=1, width=19,text="Spustit",command=self.iTl).pack()
		def iTl(self):
			""" Metoda spouštějící iTalc
			\param self Ukazatel na objekt
			"""
			subprocess.Popen("italc", shell=True)
		def qquit(self):
			""" Metoda pro ukončení okna
			\param self Ukazatel na objekt
			"""
			self.root.destroy()
	win = Tk()
	pp = App(win)
	pp.paintLayout()
	win.mainloop()
	