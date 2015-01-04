#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
## \file logoutDis.py
## \brief Grafický prvek informující uživatele, že odhlášení je vypnuto

import tkMessageBox
from Tkinter import *

if __name__ == "__main__":
	class App:
		""" \brief Třída obsahující metody s prací s oknem
		Okénko pro odhlašování a restartování
		"""
		def __init__(self,r):
			""" Konstruktor třídy okna
			\param self Ukazatel na objekt
			\param r Ukazatel na Tkinker okno
			\param qi Vstupní fronta
			\param qo Výstupní fronta
			"""
			## Ukazatel na okno Tk
			self.root=r
			## Ukazatel na iTalc třídu
			self.root.title("Odhlášení")
			self.root.geometry(("%dx%d")%(200,140))
			self.root.wm_iconbitmap('@/addons/gnusk.xbm')
			self.root.resizable(0,0)
		def paintLayout(self):
			""" Metoda vykreslující grafické prvky okna
			Slouží jako komplexní metoda pro vykreslení a je hlavní metodou s práci s oknem
			\param self Ukazatel na objekt
			"""
			group = LabelFrame(self.root, padx=5, pady=5)
			group.pack(padx=10, pady=10)
			## Label hláška pro uživatele
			self.vd = StringVar()
			self.vd.set("Odhlášení není povoleno, \n pro zničení vaší relace \n restartujte počítač")
			## Label oznamující uživateli stav
			self.ld = Label( group, textvariable=self.vd, relief=RAISED).pack()
			Button(self.root,height=1, width=19,command=self.shut,text="Vypnout").pack()
			Button(self.root,height=1, width=19,command=self.shur,text="Restartovat").pack()
		def shut(self):
			""" Metoda pro vypnutí
			\param self Ukazatel na objekt
			"""
			open("/run/shm/hlt","w").write("1")
		def shur(self):
			""" Metoda pro restartování
			\param self Ukazatel na objekt
			"""
			open("/run/shm/hlt","w").write("2")
	## Hlavní okno
	win = Tk()
	## Vlastní instance okna
	pp = App(win)
	pp.paintLayout()
	win.mainloop()